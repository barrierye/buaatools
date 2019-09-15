#-*- coding:utf8 -*-
# Copyright (c) 2019 barriery
# Python release: 3.7.4
"""
This module is used to check the remaining credits.
"""

import re
import platform

__all__ = ['check_request_credit']

def get_colorful_str(string, color):
    ''' get colorful str '''
    if platform.system() == "Windows":
        return string
    color_map = {'black': '30',
                 'red': '31',
                 'green': '32',
                 'yellow': '33',
                 'blue': '34',
                 'purple': '35',
                 'cyan': '36',
                 'white': 37}
    color_string = color_map.get(color)
    if not color_string:
        return string
    return '\033[1;' + color_string + 'm' + string + '\033[0m'

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
        print(get_colorful_str('[ERROR]', 'red') + ' error type.')
        exit(1)

def print_info(request_key, request_value, loop_deep):
    ''' printf info '''
    backspace = '    '
    info_str = backspace * loop_deep
    if isinstance(request_value, int):
        if request_value > 0:
            if request_key != 'total':
                print(info_str + get_colorful_str('[WARN]', 'yellow')
                      + ' course(%s) has not been completed yet.' % request_key)
        return request_value <= 0
    finish_flag = True
    for item in request_value:
        finish_flag = print_info(item, request_value[item], loop_deep+1) and finish_flag
    if request_value['total'] > 0:
        print(info_str + get_colorful_str('[WARN]', 'yellow')
              + ' %s missing %d points.' % (request_key, request_value['total']))
        if request_key == '跨学科课程组':
            print(backspace * loop_deep
                  + get_colorful_str('* This group(跨学科课程组) is special, please check it manually.', 'purple'))
        return False
    elif finish_flag:
        print(info_str + get_colorful_str('[INFO]', 'green')
              + ' You have filled all the credits in %s.'%request_key)
        return True
    else:
        print(info_str + get_colorful_str('[WARN]', 'yellow')
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
