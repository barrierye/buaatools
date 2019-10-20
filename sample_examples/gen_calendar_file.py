#-*- coding:utf8 -*-
# Copyright (c) 2019 barriery
# Python release: 3.7.0

import config
from buaatools.spider import course

if __name__ == '__main__':
    courses_obj = course.query_course_by_xh(stage=config.STAGE,
                                            xh=config.XH,
                                            username=config.USERNAME,
                                            password=config.PASSWORD,
                                            debug=False)
    if courses_obj:
        courses_obj.gen_ics_file(classbreak=config.CLASSBREAK,
                                 filename='curriculum.ics')
        courses_obj.check_request_credit(student_type=config.STUDENT_TYPE,
                                         total_request_credit_dict=config.REQUEST_CREDIT)
