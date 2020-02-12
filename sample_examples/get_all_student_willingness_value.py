#-*- coding:utf8 -*-
# Copyright (c) 2019 barriery
# Python release: 3.7.4
import time
import logging

import config
from buaatools.spider import login, course

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M', level=logging.INFO)

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
    session = login.login(target='https://gsmis.e2.buaa.edu.cn:443',
                          username=username, password=password, vpn=vpn)
    courses = course.query_course_by_xh(stage='preparatory', xh=xh, session=session, vpn=vpn)
    course_id_set = set()
    for c in courses:
        key = "%s(%s)" % (c['name'], c['course_id'])
        if key in course_id_set:
            continue
        course_id_set.add(key)
        willingness_list = willingness_value_list[key]
        tmp = []
        for i, v in enumerate(willingness_list):
            if v >= int(c['willingness_value']):
                tmp.append(int(c['willingness_value']))
        print(f"{key} [my willingness: {c['willingness_value']}] <Number of students with willingness >= you>: {len(tmp)}")
        print(tmp)

if __name__ == '__main__':
    VPN = True
    STUDENT_NUMBERS = [] # ['SY1906101', 'SY1906102', 'SY1906117', 'SY1906118']
    with open('全日制硕士收录记录.csv') as f:
        for line in f:
            xh = line.split(',')[2]
            STUDENT_NUMBERS.append(xh)
    willingness_value_list = course.get_willingness_list(username=config.USERNAME, password=config.PASSWORD,
                                                         student_numbers=STUDENT_NUMBERS,
                                                         interval=1, vpn=VPN)
    write_willingness_file(willingness_value_list, 'willingness_value_list.txt')
    query_my_willingness_rank(config.USERNAME, config.PASSWORD, config.XH, willingness_value_list, vpn=VPN)
