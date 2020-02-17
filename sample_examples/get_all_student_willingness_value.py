#-*- coding:utf8 -*-
# Copyright (c) 2019 barriery
# Python release: 3.7.4
import time
import logging

import config
from buaatools.helper import logger
from buaatools.spider import login, course

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M', level=logging.INFO)

_LOGGER = logging.getLogger(__name__)

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

def query_my_willingness_rank(username, password, xh, willingness_value_list, vpn=False):
    session, success = login.login(target='https://gsmis.e2.buaa.edu.cn:443',
                          username=username, password=password, need_flag=True, vpn=vpn)
    if not success:
        return
    
    courses = course.query_course_by_xh(stage='preparatory', xh=xh, session=session, vpn=vpn)
    if not courses:
        return
    
    total_courses = course.query_courseSize_by_xh(stage='preparatory', xh=xh, session=session, vpn=vpn)
    if not total_courses:
        return
    
    courses_size = {"%s(%s)"%(c['name'], c['course_id']): int(c['course_size']) for c in total_courses}

    course_id_set = set()
    for c in courses:
        key = "%s(%s)" % (c['name'], c['course_id'])
        if key in course_id_set:
            continue
        course_id_set.add(key)
        csize = courses_size[key]
        willingness_list = willingness_value_list[key]
        tmp = []
        for v in willingness_list:
            if v >= int(c['willingness_value']):
                tmp.append(v)
        print(f"{key} [my willingness: {c['willingness_value']}] <Number of students with willingness >= you>({len(tmp)}/{csize}):")
        print(tmp)
        print(logger.get_colorful_str(f"INFO: The recommended expectation is {tmp[-(csize-1)]}", 'green'))
        if len(tmp) > csize:
            print(logger.get_colorful_str("WARN: You need to adjust your willingness or you won't be able to take the course.", 'yellow'))

def get_student_numbers():
    #  student_numbers = ['SY1906108', 'SY1906117', 'SY1906118']
    student_numbers = []
    with open('全日制硕士收录记录.csv') as f:
        for line in f:
            xh = line.split(',')[2]
            student_numbers.append(xh)
    return student_numbers

if __name__ == '__main__':
    filename = 'willingness_value_list.txt'
    mode = 'offline'
    _LOGGER.info(f'mode: {mode}, filename: {filename}')
    if mode == 'online':
        willingness_value_list = course.get_willingness_list(username=config.USERNAME, password=config.PASSWORD,
                                                             student_numbers=get_student_numbers(),
                                                             interval=1, vpn=config.VPN)
        write_willingness_file(willingness_value_list, filename)
    elif mode == 'offline':
        willingness_value_list = read_willingness_file(filename)
    query_my_willingness_rank(config.USERNAME, config.PASSWORD, config.XH, willingness_value_list, vpn=config.VPN)
