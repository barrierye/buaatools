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

def write_course_willingness(course_willingness, filename):
    with open(filename, 'w') as f:
        for course, willingness_value_list in course_willingness.items():
            willingness_value_list.sort()
            f.write("[%s] : %s\n" % (course, str(willingness_value_list)))

def read_course_willingness(filename):
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

def get_student_numbers():
    #  student_numbers = ['SY1906108', 'SY1906117', 'SY1906118']
    student_numbers = []
    with open('全日制硕士收录记录.csv') as f:
        for line in f:
            xh = line.split(',')[2]
            student_numbers.append(xh)
    return student_numbers

if __name__ == '__main__':
    mode = 'offline'
    filename = 'course_willingness.txt'
    _LOGGER.info(f'mode: {mode}, filename: {filename}')

    # get course_willingness
    if mode == 'online':
        course_willingness = course.get_course_willingness(username=config.USERNAME,
                                                           password=config.PASSWORD,
                                                           student_numbers=get_student_numbers(),
                                                           interval=1,
                                                           vpn=config.VPN)
        write_course_willingness(course_willingness, filename)
    elif mode == 'offline':
        course_willingness = read_course_willingness(filename)
    
    # query willingess rank
    course.query_willingness_rank_by_xh(stage=config.STAGE,
                                        xh=config.XH,
                                        username=config.USERNAME,
                                        password=config.PASSWORD,
                                        course_willingness=course_willingness,
                                        vpn=config.VPN)
