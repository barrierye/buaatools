#-*- coding:utf8 -*-
# Copyright (c) 2019 barriery
# Python release: 3.7.4
"""
This module is used to check the remaining credits.
"""

import re

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
        print('[ERROR] error type.')
        exit(1)

def print_info(request_key, request_value, loop_deep):
    ''' printf info '''
    if isinstance(request_value, int):
        return
    backspace = '  '
    if request_value['total'] > 0:
        info_str = backspace * loop_deep
        if loop_deep:
            info_str += '- '
        print(info_str + '%s missing %d points.' % (request_key, request_value['total']))
        if request_key == '跨学科课程组':
            print(backspace * loop_deep + '[INFO] This group is special, please confirm it manually.')
    for item in request_value:
        print_info(item, request_value[item], loop_deep+1)

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
