#-*- coding:utf8 -*-
# Copyright (c) 2019 barriery
# Python release: 3.7.4
"""
This module is used to check the remaining credits.
"""

import re

def request_credit(student_type, global_request_credit_dict, course_list):
    ''' check credit '''
    request = global_request_credit_dict.get(student_type)
    if not request:
        print('Miss %s in REQUEST_CREDIT.' % student_type)
        return
    course_set = set()
    for course in course_list:
        course_set.add((course['course_id'], int(course['credit'])))
    for course_id, course_credit in course_set:
        for course_group in request:
            for course_id_pattern in request[course_group]:
                if course_id_pattern == 'total':
                    continue
                if re.match(course_id_pattern, course_id):
                    request[course_group][course_id_pattern] -= course_credit
                    request[course_group]['total'] -= course_credit
                    break
    for course_group, request_list in request.items():
        if request_list['total'] > 0:
            print('[WARN] %s missing %d points.' % (course_group, request_list['total']))
            if course_group == '跨学科课程组':
                print('- This group is special. Please confirm it manually.')
        for item, credit in request_list.items():
            if item == 'total':
                continue
            if credit > 0:
                print('- %s in %s missing %d points.'%(item, course_group, credit))
