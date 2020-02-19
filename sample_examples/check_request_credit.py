#-*- coding:utf8 -*-
# Copyright (c) 2019 barriery
# Python release: 3.7.0

import logging

import config
from buaatools.spider import course

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M', level=logging.INFO)

if __name__ == '__main__':
    courses_obj = course.query_course_by_xh(stage=config.STAGE,
                                            xh=config.XH,
                                            username=config.USERNAME,
                                            password=config.PASSWORD,
                                            begin_date=config.BEGIN_DATE,
                                            vpn=config.VPN)
    if courses_obj:
        courses_obj.check_request_credit(student_type=config.STUDENT_TYPE,
                                         total_request_credit_dict=config.REQUEST_CREDIT,
                                         previous_finished_credit_list=config.PREVIOUS_FINISHED_CREDIT_LIST)
