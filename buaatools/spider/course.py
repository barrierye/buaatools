#-*- coding:utf8 -*-
# Copyright (c) 2019 barriery
# Python release: 3.7.0
"""
This module is used to simulate the page for the course selection and get thml text.
"""

import re
import sys
import time
import logging
import hashlib
import requests
import datetime
from uuid import uuid1
import pytz
from icalendar import Calendar, Event

from buaatools.helper import logger
from buaatools.spider import login

__all__ = ['get_signed_response_by_xh',
           'query_courseSize_by_xh',
           'query_name_by_xh',
           'query_course_by_xh',
           'get_willingness_list']

_LOGGER = logging.getLogger(__name__)

LOGIN = {
    'vpn': 'https://gsmis.e2.buaa.edu.cn:443',
    #  'vpn': 'https://gsmis.e.buaa.edu.cn:443',
    'normal': 'http://gsmis.buaa.edu.cn/',
}

HOME = {
    'vpn': 'https://gsmis.e2.buaa.edu.cn/',
    #  'vpn': 'https://gsmis.e.buaa.edu.cn/',
    'normal': 'http://gsmis.buaa.edu.cn/',
}

paramsTable = {
    'api/yuXuanKeApiController.do?pyfaFilter': 'body={"xh":"%s","taskId":"%s","xklcqdszxxid":"%s"}',
    'api/yuXuanKeApiController.do?findKcxxList': 'body={"xh":"%s","pageSize":3000,"pageNum":1,"kcmc":"","xklcqdszxxid":"%s","biaoshi":"1","num":"1"}',
    'api/yuXuanKeApiController.do?getSelectedCourses': 'body={"xh":"%s"}',
    'api/yuXuanKeApiController.do?txSelectedCourses': 'body={"xh":"%s"}',
    'api/xuankeApiController.do?gtasksList': 'body={"xh":"%s"}', # 'obj' -> [0] -> 'id_'(taskId)/'xklcqdszxxid'
    'api/xuankeApiController.do?getUserListByXH': 'body={"xh":"%s"}', # 'obj' -> 'realname'
    'api/xuankeApiController.do?getCalendarTime': 'body={"xh":"%s"}',
    'api/xuankeApiController.do?getFlowChart': 'body={"xh":"%s","xklcqdszxxid":"%s"}',
    'api/xuankeApiController.do?checkXuanKeUser': 'body={"xh":"%s","taskId":"%s","xklcqdszxxid":"%s"}',
    'api/dictionaries.do?getDictionaryData': 'body={"code":"ssxqhjd"}',
    'api/tuiXuanKeApiController.do?getDropCourses': 'body={"xh":"%s"}',
}

def fill_params(params_string, xh, session, vpn=False):
    _LOGGER.debug(f'params_string: {params_string}, xh: {xh}, vpn: {vpn}')
    params_pattern = re.compile(r'"([^"]*?)":"%s"')
    params = params_pattern.findall(params_string)
    text = []
    for param in params:
        _LOGGER.debug(f'query param: {param}')
        if param == 'xh':
            text.append(xh)
            _LOGGER.debug(f'find param: {param}({xh})')
        elif param == 'xklcqdszxxid' or param == 'taskId':
            response = get_signed_response_by_xh('api/xuankeApiController.do?gtasksList', xh, session=session, vpn=vpn)
            if not response:
                return None
            try:
                obj = response.json().get('obj')[0]
                text.append(obj.get(param))
                _LOGGER.debug(f'find param: {param}({obj.get(param)})')
            except:
                try:
                    _LOGGER.error(response.json())
                except:
                    _LOGGER.error('can not parse response to json.')
                exit(1)
        else:
            _LOGGER.error(f'error param: {param}')
            exit(1)
    return params_string % tuple(text)

def get_signed_response_by_xh(api, xh, username=None, password=None, session=None, vpn=False):
    _LOGGER.info(f'api: {api}, vpn: {vpn}')
    opt = 'vpn' if vpn else 'normal'

    # login
    if session is None:
        if username is None or password is None:
            _LOGGER.error('username or password is None.')
            exit(1)
        session, success = login.login(target=LOGIN[opt], username=username, password=password, need_flag=True, vpn=vpn)
        if not success:
            _LOGGER.error('Failed to login.')
            return None
        _LOGGER.info('login success.')
    
    url = HOME[opt] + api
    # here is a stupid authenticate, you can query any info by using different xh after login.
    param_string = paramsTable[api]
    filled_params = fill_params(param_string, xh, session, vpn=vpn)
    _LOGGER.debug(f'filled_params: {filled_params}')
    salt_string = '&key=53C2780372E847AEDB1726F136F7BD79CE12B6CA919B6CF4'
    s = '{' + filled_params + '}' + salt_string
    session.headers['X-BUAA-SIGN'] = hashlib.md5(s.encode()).hexdigest().upper()
    payload = {'body': filled_params[5:]} # {'body': '{"xh":"%s"}'
    _LOGGER.debug(f'payload: {payload}')
    response = session.post(url, data=payload)
    if not response:
        return None

    try:
        if response.json().get('success') is False:
            _LOGGER.error(f"Failed('success': False)")
            return []
        msg = response.json().get('msg')
        if msg != '操作成功' and msg != '操作正常':
            _LOGGER.error(f"Failed('msg': '{msg}').")
            return []
    except:
        try:
            _LOGGER.error(response.json())
        except:
            _LOGGER.error('can not parse response to json.')
        _LOGGER.error(response.content.decode('utf-8'))
        return []
    
    return response

def query_courseSize_by_xh(stage, xh, username=None, password=None, session=None, vpn=False):
    stage_list = {'preparatory': 'api/yuXuanKeApiController.do?findKcxxList',}
    _LOGGER.info(f'stage: {stage}, xh: {xh}, vpn: {vpn}')
    if stage not in stage_list:
        _LOGGER.error('stage(%s) not in-built(%s).'
                % (stage, ', '.join([x for x in stage_list])))
        return None

    response = get_signed_response_by_xh(stage_list[stage], xh, username, password, session, vpn)
    if not response:
        return None

    attributes = response.json().get('attributes')
    total_courses = attributes.get('kclb')
    _LOGGER.info(f'total courses: {len(total_courses)}')

    course_list = Courses()
    key_map = {'kxrs': 'course_size',
               'rklsgzzh': 'teacher',
               'kcmc': 'name',
               'kch': 'course_id',
               'zxf': 'credit',
               'id': 'id_in_system',}
    for item in total_courses:
        course = {human_firendly_key: item[magic_key] \
                for magic_key, human_firendly_key in key_map.items()}
        course_list.append(course)
    return course_list

def query_name_by_xh(stage, xh, username=None, password=None, session=None, vpn=False):
    stage_list = {'preparatory': 'api/xuankeApiController.do?getUserListByXH',
                  'adjustment': 'api/xuankeApiController.do?getUserListByXH',}
    _LOGGER.info(f'stage: {stage}, xh: {xh}, vpn: {vpn}')
    if stage not in stage_list:
        _LOGGER.error('stage(%s) not in-built(%s).'
                % (stage, ', '.join([x for x in stage_list])))
        return None
    
    response = get_signed_response_by_xh(stage_list[stage], xh, username, password, session, vpn)
    if not response:
        return None
    
    obj = response.json().get('obj')
    realname = obj.get('realname')
    
    return realname

def query_course_by_xh(stage, xh, username=None, password=None, session=None,
        begin_date=None, class_period_begin_time=None, vpn=False):
    stage_list = {'preparatory': 'api/yuXuanKeApiController.do?getSelectedCourses',
                  'adjustment': 'api/yuXuanKeApiController.do?txSelectedCourses',
                  'ending': 'api/tuiXuanKeApiController.do?getDropCourses'}
    _LOGGER.info(f'stage: {stage}, xh: {xh}, vpn: {vpn}')
    if stage not in stage_list:
        _LOGGER.error('stage(%s) not in-built(%s).'
                % (stage, ', '.join([x for x in stage_list])))
        return None
    response = get_signed_response_by_xh(stage_list[stage], xh, username, password, session, vpn)
    if not response:
        return None

    attributes = response.json().get('attributes')
    if not attributes:
        _LOGGER.error("Failed to get course list. Maybe the student id not in this system.")
        _LOGGER.debug(response.content.decode('utf-8'))
        return []
    selected_courses = attributes.get('kclb')
    
    course_list = Courses(begin_date=begin_date,
                          class_period_begin_time=class_period_begin_time)
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
        _LOGGER.info('add course(%s)' % ', '.join([course[k] for k in ['name', 'course_id', 'credit']]))
    return course_list

def get_course_willingness(username, password, student_numbers, interval=2, vpn=False):
    ''' student_numbers: ['SY1906000', 'SY1906001', ...] '''
    opt = 'vpn' if vpn else 'normal'
    session, success = login.login(target=LOGIN[opt],
                                   username=username,
                                   password=password,
                                   need_flag=True,
                                   vpn=vpn)
    if not success:
        _LOGGER.error('Failed to login.')
        return None
    _LOGGER.info('login success.')
    course_willingness = {}
    for xh in student_numbers:
        _LOGGER.info(f'query xh[{xh}]...')
        courses = query_course_by_xh(stage='preparatory', xh=xh, session=session, vpn=vpn)
        if not courses:
            _LOGGER.warn(f'xh[{xh}] lookup failed.')
            continue
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
    for course, willingness_value_list in course_willingness.items():
        willingness_value_list.sort()
    return course_willingness

def query_willingness_rank_by_xh(stage, xh, username, password, course_willingness, vpn=False):
    _LOGGER.info(f'stage: {stage}, xh: {xh}, vpn: {vpn}')
    stage_list = ['preparatory']
    if stage not in stage_list:
        _LOGGER.error('stage(%s) not in-built(%s).'
                % (stage, ', '.join([x for x in stage_list])))
        return None
    
    opt = 'vpn' if vpn else 'normal'
    session, success = login.login(target=LOGIN[opt], username=username, password=password, need_flag=True, vpn=vpn)
    if not success:
        _LOGGER.error('login failed.')
        return
    
    courses = query_course_by_xh(stage=stage, xh=xh, session=session, vpn=vpn)
    if not courses:
        _LOGGER.error('query courses failed.')
        return
    
    total_courses = query_courseSize_by_xh(stage=stage, xh=xh, session=session, vpn=vpn)
    if not total_courses:
        _LOGGER.error('query course size failed.')
        return
    
    courses_size = {"%s(%s)"%(c['name'], c['course_id']): int(c['course_size']) for c in total_courses}

    course_id_set = set()
    for c in courses:
        key = "%s(%s)" % (c['name'], c['course_id'])
        if key in course_id_set:
            continue
        course_id_set.add(key)
        csize = courses_size[key]
        willingness_list = course_willingness[key]
        tmp = []
        for v in willingness_list:
            if v >= int(c['willingness_value']):
                tmp.append(v)
        print(f"{key} [my willingness: {c['willingness_value']}] <Number of students with willingness >= you>: {len(tmp)}({len(tmp)+1}/{csize}):")
        print(tmp)
        expect_val = 1 if csize > len(willingness_list) else willingness_list[-csize] + 1
        if len(tmp) > csize:
            print(logger.get_colorful_str(f"WARN: The recommended expectation is {expect_val}. "
                "You need to adjust your willingness or you won't be able to take the course.", 'yellow'))
        else:
            print(logger.get_colorful_str(f"INFO: The recommended expectation is {expect_val}.", 'green'))

class Courses(list):
    def __init__(self, begin_date=None, class_period_begin_time=None):
        # 开学第0周日期
        if begin_date is None:
            begin_date = datetime.datetime(2019, 8, 26, 0, 0, 0, tzinfo=pytz.timezone("Asia/Shanghai"))
        # 每节课时间
        if class_period_begin_time is None:
            class_period_begin_time = [(0, 0), (8, 0), (8, 50), \
                                       (9, 50), (10, 40), (11, 30), \
                                       (14, 00), (14, 50), (15, 50), \
                                       (16, 40), (17, 30), (19, 0), \
                                       (19, 50), (20, 40), (21, 30)]
        self.BEGIN_DATE = begin_date
        self.CLASS_PERIOD_BEGIN_TIME = class_period_begin_time.copy()
        _LOGGER.debug('BEGIN_DATE: %s' % self.BEGIN_DATE.strftime('%Y-%m-%d'))
            
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
            _LOGGER.critical('error type')
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
            _LOGGER.error(f'Miss {student_type} in REQUEST_CREDIT.')
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
