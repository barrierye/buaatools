#-*- coding:utf8 -*-
# Copyright (c) 2019 barriery
# Python release: 3.7.4
"""
module docstring: TODO
"""
import time

import sys
sys.path.append('..')

import config
from spider import bylogin, bycourse

def get_willingness_list(username, password, student_numbers):
    ''' student_numbers: ['SY1906000', 'SY1906001', ...] '''
    session = bylogin.login(target='http://gsmis.buaa.edu.cn/',
                          username=username,
                          password=password)
    course_willingness = {}
    for xh in student_numbers:
        print("query xh[%s]..." % xh)
        courses = bycourse.query_pre_selected_course_by_xh(xh=xh, session=session)
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
        time.sleep(2)
    return course_willingness

def write_willingness_file(course_willingness, filename):
    with open(filename, 'w') as f:
        for course, willingness_value_list in course_willingness.items():
            willingness_value_list.sort()
            f.write("[%s] : %s\n" % (course, str(willingness_value_list)))

def read_willingness_file(filename):
    course_willingness = {}
    with open(filename, 'r') as f:
        for line in f.readlines():
            key = line.split(':')[0]
            key = key.split('[')[1].split(']')[0]
            willingness_list = line.split(':')[1]
            willingness_list = willingness_list.split('[')[1].split(']')[0]
            willingness_list = [int(x.strip()) for x in willingness_list.split(',')]
            course_willingness[key] = willingness_list
    return course_willingness

def query_my_willingness_rank(username, password, xh, willingness_value_list):
    session = bylogin.login(target='http://gsmis.buaa.edu.cn/',
                            username=username, password=password)
    courses = bycourse.query_pre_selected_course_by_xh(xh=xh, session=session)
    course_id_set = set()
    for course in courses:
        key = "%s(%s)" % (course['name'], course['course_id'])
        if key in course_id_set:
            continue
        course_id_set.add(key)
        print("%s [%s] <Number of students with the same willingness as you>:" % (key, course['willingness_value']))
        willingness_list = willingness_value_list[key]
        willingness_list.reverse()
        for i, v in enumerate(willingness_list):
            if v <= int(course['willingness_value']):
                print("%d" % i)
                if v < int(course['willingness_value']):
                    break
        print("------------------------------------------")

if __name__ == '__main__':
    STUDENT_NUMBERS = ['SY1906000', 'SY1906001']
    willingness_value_list = get_willingness_list(config.USERNAME,
                                                  config.PASSWORD,
                                                  STUDENT_NUMBERS)
    write_willingness_file(willingness_value_list, 'willingness_value_list.txt')
    #  willingness_value_list = read_willingness_file('willingness_value_list.txt')
    query_my_willingness_rank(config.USERNAME, config.PASSWORD, config.XH, willingness_value_list)
