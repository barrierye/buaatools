#-*- coding:utf8 -*-
# Copyright (c) 2019 barriery
# Python release: 3.7.0
"""
This module is used to simulate the page for the course selection and get thml text.
"""

import re
import hashlib
import requests

import sys
from buaatools.helper import bylogger
from buaatools.spider import bylogin

__all__ = ['query_course_by_xh', 'check_request_credit']

HOME = 'http://gsmis.buaa.edu.cn/'
HOME_WITH_VPN = 'https://gsmis.e.buaa.edu.cn/'

def query_course_by_xh(stage, xh, username=None, password=None, session=None, debug=False, vpn=False):
    stage_list = {'preparatory': 'api/yuXuanKeApiController.do?getSelectedCourses',
                  'adjustment': 'api/yuXuanKeApiController.do?txSelectedCourses',
                  'ending': 'api/tuiXuanKeApiController.do?getDropCourses'}
    if stage not in stage_list:
        sys.stderr.write(bylogger.get_colorful_str("[ERROR] stage(%s) not in-built"%stage, "red"))
        return []
    home = HOME
    if vpn:
        home = HOME_WITH_VPN
    url = home + stage_list[stage]

    if session is None:
        if username is None or password is None:
            sys.stderr.write(bylogger.get_colorful_str("[ERROR] username or password is None", "red"))
            return []
        session, success = bylogin.login(target=home, username=username, password=password, need_flag=True)
        if not success:
            sys.stderr.write(bylogger.get_colorful_str("[ERROR] Failed to login.\n", "red"))
            return []
    
    # here is a stupid authenticate, you can query any info by using different xh after login.
    magic_string = '{body={"xh":"' + xh + '"}}&key=53C2780372E847AEDB1726F136F7BD79CE12B6CA919B6CF4'
    session.headers['X-BUAA-SIGN'] = hashlib.md5(magic_string.encode()).hexdigest().upper()
    payload = {'body': '{"xh":"%s"}'%xh}
    response = session.post(url, data=payload)

    if response.json().get('success') is False:
        sys.stderr.write(bylogger.get_colorful_str("[ERROR] Failed('success': False).\n", "red"))
        if debug:
            sys.stderr.write(response.content.decode('utf-8'))
        return []
    if response.json().get('msg') == '此学生还没有添加预选课程':
        sys.stderr.write(bylogger.get_colorful_str("[ERROR] Failed('msg': '此学生还没有添加预选课程').\n", "red"))
        if debug:
            sys.stderr.write(response.content.decode('utf-8'))
        return []
    if response.json().get('msg') == '此学生还没有退选课程':
        sys.stderr.write(bylogger.get_colorful_str("[ERROR] Failed('msg': '此学生还没有退选课程').\n", "red"))
        if debug:
            sys.stderr.write(response.content.decode('utf-8'))
        return []
    
    attributes = response.json().get('attributes')
    if not attributes:
        sys.stderr.write(bylogger.get_colorful_str("[ERROR] Failed to get course list. Maybe the student id not in this system.\n", "red"))
        if debug:
            sys.stderr.write(response.content.decode('utf-8'))
        return []
    selected_courses = attributes.get('kclb')
    
    course_list = []
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

def check_course(request_key, request_value, course):
    ''' check course in request_dict '''
    course_id, course_credit = course
    if isinstance(request_value, int):
        if re.match(request_key, course_id):
            return course_credit
        return 0
    elif isinstance(request_value, dict):
        total_credit = 0
        for item in request_value:
            credit = check_course(item, request_value[item], course)
            if isinstance(request_value[item], int):
                request_value[item] -= credit
            total_credit += credit
        request_value['total'] -= total_credit
        return total_credit
    else:
        print(bylogger.get_colorful_str('[ERROR]', 'red') + ' error type.')
        exit(1)

def print_info(request_key, request_value, loop_deep):
    ''' printf info '''
    backspace = '    '
    info_str = backspace * loop_deep
    if isinstance(request_value, int):
        if request_value > 0:
            if request_key != 'total':
                print(info_str + bylogger.get_colorful_str('[WARN]', 'yellow')
                      + ' course(%s) has not been completed yet.' % request_key)
        return request_value <= 0
    finish_flag = True
    for item in request_value:
        finish_flag = print_info(item, request_value[item], loop_deep+1) and finish_flag
    if request_value['total'] > 0:
        print(info_str + bylogger.get_colorful_str('[WARN]', 'yellow')
              + ' %s missing %d points.' % (request_key, request_value['total']))
        if request_key == '跨学科课程组':
            print(backspace * loop_deep
                  + bylogger.get_colorful_str('* This group(跨学科课程组) is special, please check it manually.', 'purple'))
        return False
    elif finish_flag:
        print(info_str + bylogger.get_colorful_str('[INFO]', 'green')
              + ' You have filled all the credits in %s(beyond %d points).'%(request_key, -request_value['total']))
        return True
    else:
        print(info_str + bylogger.get_colorful_str('[WARN]', 'yellow')
              + ' You have filled all the credits in %s, but there are some items not finished.'%request_key)
        return False

def check_request_credit(student_type, total_request_credit_dict, course_list):
    ''' check request credit '''
    if not total_request_credit_dict.get(student_type):
        print('Miss %s in REQUEST_CREDIT.' % student_type)
        return
    course_set = set()
    for course in course_list:
        course_set.add((course['course_id'], int(course['credit'])))
    for course in course_set:
        check_course(student_type, total_request_credit_dict[student_type], course)
    print_info(student_type, total_request_credit_dict[student_type], 0)
