#-*- coding:utf8 -*-
# Copyright (c) 2019 barriery
# Python release: 3.7.0
"""
This module is used to simulate the page for the course selection and get thml text.
"""

import re
import sys
import hashlib
import requests
import datetime
from uuid import uuid1
import pytz
from icalendar import Calendar, Event

from buaatools.helper import logger
from buaatools.spider import login

__all__ = ['query_course_by_xh', 'get_willingness_list']

HOME = 'http://gsmis.buaa.edu.cn/'
HOME_WITH_VPN = 'https://gsmis.e.buaa.edu.cn/'

def query_course_by_xh(stage, xh, username=None, password=None, session=None, debug=False, vpn=False):
    stage_list = {'preparatory': 'api/yuXuanKeApiController.do?getSelectedCourses',
                  'adjustment': 'api/yuXuanKeApiController.do?txSelectedCourses',
                  'ending': 'api/tuiXuanKeApiController.do?getDropCourses'}
    if stage not in stage_list:
        sys.stderr.write(logger.get_colorful_str("[ERROR] stage(%s) not in-built"%stage, "red"))
        return None
    if vpn:
        url = HOME_WITH_VPN + stage_list[stage]
    else:
        url = HOME + stage_list[stage]

    if session is None:
        if username is None or password is None:
            sys.stderr.write(logger.get_colorful_str("[ERROR] username or password is None", "red"))
            return None
        if vpn:
            session, success = login.login_with_vpn(target='https://gsmis.e.buaa.edu.cn:443',
                                                    username=username, 
                                                    password=password, 
                                                    need_flag=True)
        else:
            session, success = login.login(target=HOME, username=username, password=password, need_flag=True)
        if not success:
            sys.stderr.write(logger.get_colorful_str("[ERROR] Failed to login.\n", "red"))
            return None
    
    # here is a stupid authenticate, you can query any info by using different xh after login.
    magic_string = '{body={"xh":"' + xh + '"}}&key=53C2780372E847AEDB1726F136F7BD79CE12B6CA919B6CF4'
    session.headers['X-BUAA-SIGN'] = hashlib.md5(magic_string.encode()).hexdigest().upper()
    payload = {'body': '{"xh":"%s"}'%xh}
    response = session.post(url, data=payload)

    if response.json().get('success') is False:
        sys.stderr.write(logger.get_colorful_str("[ERROR] Failed('success': False).\n", "red"))
        if debug:
            sys.stderr.write(response.content.decode('utf-8'))
        return []
    if response.json().get('msg') == '此学生还没有添加预选课程':
        sys.stderr.write(logger.get_colorful_str("[ERROR] Failed('msg': '此学生还没有添加预选课程').\n", "red"))
        if debug:
            sys.stderr.write(response.content.decode('utf-8'))
        return []
    if response.json().get('msg') == '此学生还没有退选课程':
        sys.stderr.write(logger.get_colorful_str("[ERROR] Failed('msg': '此学生还没有退选课程').\n", "red"))
        if debug:
            sys.stderr.write(response.content.decode('utf-8'))
        return []
    
    attributes = response.json().get('attributes')
    if not attributes:
        sys.stderr.write(logger.get_colorful_str("[ERROR] Failed to get course list. Maybe the student id not in this system.\n", "red"))
        if debug:
            sys.stderr.write(response.content.decode('utf-8'))
        return []
    selected_courses = attributes.get('kclb')
    
    course_list = Courses()
    key_map = {'rklsgzzh': 'teacher',
               'kcmc': 'name',
               'qszc': 'week_begin',
               'zzzc': 'week_end',
               'qsjs': 'class_begin',
               'jsjs': 'class_end',
               'kch': 'course_id',
               'skjsbh': 'place',
               'zxf': 'credit',
               'zj': 'weekday',
               'id': 'id_in_system',
               'yyz': 'willingness_value'}
    for item in selected_courses:
        course = {human_firendly_key: item[magic_key] \
                for magic_key, human_firendly_key in key_map.items()}
        course_list.append(course)
    return course_list

def get_willingness_list(username, password, student_numbers, interval=2):
    ''' student_numbers: ['SY1906000', 'SY1906001', ...] '''
    session = login.login(target='http://gsmis.buaa.edu.cn/',
                          username=username,
                          password=password)
    course_willingness = {}
    for xh in student_numbers:
        print("query xh[%s]..." % xh)
        courses = bycourse.query_course_by_xh(stage='preparatory', xh=xh, session=session)
        courses_id_set = set()
        for course in courses:
            key = "%s(%s)" % (course['name'], course['course_id'])
            
            if key in courses_id_set:
                continue
            courses_id_set.add(key)

            if key in course_willingness:
                course_willingness[key].append(int(course['willingness_value']))
            else:
                course_willingness[key] = [int(course['willingness_value'])]
        time.sleep(interval)
    return course_willingness

class Courses(list):
    # 开学第0周日期
    BEGIN_DATE = datetime.datetime(2019, 8, 26, 0, 0, 0, tzinfo=pytz.timezone("Asia/Shanghai"))
    # 一天各节课开始时间
    CLASS_PERIOD_BEGIN_TIME = [(0, 0), (8, 0), (8, 50), \
                               (9, 50), (10, 40), (11, 30), \
                               (14, 00), (14, 50), (15, 50), \
                               (16, 40), (17, 30), (19, 0), \
                               (19, 50), (20, 40), (21, 30)]
    
    def set_begin_date(self, begin_date):
        self.BEGIN_DATE = begin_date
    
    def set_class_period_begin_time(self, class_period_begin_time):
        self.CLASS_PERIOD_BEGIN_TIME = class_period_begin_time.copy()

    def __check_course(self, request_key, request_value, course):
        ''' check course in request_dict '''
        course_id, course_credit = course
        if isinstance(request_value, int):
            if re.match(request_key, course_id):
                return course_credit
            return 0
        elif isinstance(request_value, dict):
            total_credit = 0
            for item in request_value:
                credit = self.__check_course(item, request_value[item], course)
                if isinstance(request_value[item], int):
                    request_value[item] -= credit
                total_credit += credit
            request_value['total'] -= total_credit
            return total_credit
        else:
            print(logger.get_colorful_str('[ERROR]', 'red') + ' error type.')
            exit(1)

    def __print_info(self, request_key, request_value, loop_deep):
        ''' printf info '''
        backspace = '    '
        info_str = backspace * loop_deep
        if isinstance(request_value, int):
            if request_value > 0:
                if request_key != 'total':
                    print(info_str + logger.get_colorful_str('[WARN]', 'yellow')
                          + ' course(%s) has not been completed yet.' % request_key)
            return request_value <= 0
        finish_flag = True
        for item in request_value:
            finish_flag = self.__print_info(item, request_value[item], loop_deep+1) and finish_flag
        if request_value['total'] > 0:
            print(info_str + logger.get_colorful_str('[WARN]', 'yellow')
                    + ' %s missing %d points.' % (request_key, request_value['total']))
            if request_key == '跨学科课程组':
                print(backspace * loop_deep
                      + logger.get_colorful_str('* This group(跨学科课程组) is special, please check it manually.', 'purple'))
            return False
        elif finish_flag:
            print(info_str + logger.get_colorful_str('[INFO]', 'green')
                  + ' You have filled all the credits in %s(beyond %d points).'%(request_key, -request_value['total']))
            return True
        else:
            print(info_str + logger.get_colorful_str('[WARN]', 'yellow')
                  + ' You have filled all the credits in %s, but there are some items not finished.'%request_key)
            return False

    def check_request_credit(self, student_type, total_request_credit_dict, previous_finished_credit_list=None):
        ''' check request credit '''
        if not total_request_credit_dict.get(student_type):
            print('Miss %s in REQUEST_CREDIT.' % student_type)
            return
        course_set = set()
        for course in self:
            course_set.add((course['course_id'], int(course['credit'])))
        if previous_finished_credit_list is not None:
            for course in previous_finished_credit_list:
                course_set.add((course['course_id'], int(course['credit'])))
        for course in course_set:
            self.__check_course(student_type, total_request_credit_dict[student_type], course)
        self.__print_info(student_type, total_request_credit_dict[student_type], 0)

    def gen_ics_file(self, classbreak, filename=None):
        ''' generate iCalendar file '''
        cal = Calendar()
        cal.add('prodid', '-//barriery Inc//BUAA Class Schedule//CN')
        cal.add('version', '2.0')
        for course in self:
            events = self.__get_events_by_course(course, classbreak)
            for event in events:
                cal.add_component(event)
        if filename is None:
            return cal.to_ical()
        else:
            with open(filename, 'wb') as file:
                file.write(cal.to_ical())

    def __get_events_by_course(self, course, classbreak):
        ''' get events by course '''
        if not course['weekday']:
            # 某些课程（例如英语免修）没有上课周次
            return []

        # zero week is 2019/8/26 00:00:00
        current_day = self.BEGIN_DATE + datetime.timedelta(days = 7 * int(course['week_begin']) + int(course['weekday']) - 1)
        events = []
        if classbreak:
            for class_period in range(int(course['class_begin']), int(course['class_end'])+1):
                hour, minute = self.CLASS_PERIOD_BEGIN_TIME[class_period]
                current_date = current_day \
                             + datetime.timedelta(hours=hour) \
                             + datetime.timedelta(minutes=minute)
                event = Event()
                event.add('uid', str(uuid1()) + '@barriery')
                event.add('summary', course['name'])
                event.add('dtstart', current_date)
                event.add('dtend', current_date + datetime.timedelta(minutes=45))
                event.add('dtstamp', datetime.datetime.now())
                event.add('location', course['place'])
                event.add('description', 'teacher(%s), credit(%s), id(%s)' \
                        % (course['teacher'], course['credit'], course['course_id']))
                event.add('rrule', {
                    'freq': 'weekly',
                    'interval': 1,
                    'count': int(course['week_end']) - int(course['week_begin']) + 1})
                events.append(event)
        else:
            hour, minute = self.CLASS_PERIOD_BEGIN_TIME[int(course['class_begin'])]
            current_begin_date = current_day \
                    + datetime.timedelta(hours=hour) \
                    + datetime.timedelta(minutes=minute)
            hour, minute = self.CLASS_PERIOD_BEGIN_TIME[int(course['class_end'])]
            current_end_date = current_day \
                    + datetime.timedelta(hours=hour) \
                    + datetime.timedelta(minutes=minute+45)
            event = Event()
            event.add('uid', str(uuid1()) + '@barriery')
            event.add('summary', course['name'])
            event.add('dtstart', current_begin_date)
            event.add('dtend', current_end_date)
            event.add('dtstamp', datetime.datetime.now())
            event.add('location', course['place'])
            event.add('description', 'teacher(%s), credit(%s), id(%s)' \
                    % (course['teacher'], course['credit'], course['course_id']))
            event.add('rrule', {
                'freq': 'weekly',
                'interval': 1,
                'count': int(course['week_end']) - int(course['week_begin']) + 1})
            events.append(event)
        return events
