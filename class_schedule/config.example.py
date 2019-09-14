#-*- coding:utf8 -*-
# Copyright (c) 2019 barriery
# Python release: 3.7.4
"""
This module is used to do some configuration settings.
"""

# Username of the unified authentication account
USERNAME = 'barriery'
# Password of the unified authentication account
PASSWORD = '**************'
# Student ID
XH = 'SY1906***'
# Student type
# Built-in '软件工程-学硕' and '计算机科学与技术学科-学硕', you can configure it yourself if you need other majors.
STUDENT_TYPE = '软件工程-学硕'

REQUEST_CREDIT = {
    '计算机科学与技术学科-学硕': {
        '思想政治理论课程组': {
            '28111103': 1,
            '28111102': 2,
            'total': 3,
        }, '基础及学科理论课程组': {
            r'06112\d{3}': 9,
            'total': 9,
        }, '专业理论课程组': {
            r'061131\d{2}': 4,
            r'061132\d{2}': 0,
            'total': 8,
        }, '学术素养课程组': {
            '12114112': 0,
            '12114113': 0,
            '06114401': 1,
            '12114115': 0,
            'total': 3,
        }, '跨学科课程组': {
            'total': 3,
        }, '综合实践环节': {
            '06116101': 3,
            '00117202': 1,
            '00117201': 1,
            'total': 5,
        }
    }, '软件工程-学硕': {
        '思想政治理论课程组': {
            '28111103': 1,
            '28111102': 2,
            'total': 3,
        }, '基础及学科理论课程组': {
            r'06112\d{3}': 9,
            'total': 9,
        }, '专业理论课程组': {
            r'061131\d{2}': 4,
            r'061132\d{2}': 0,
            'total': 9,
        }, '学术素养课程组': {
            '12114112': 0,
            '12114113': 0,
            '12114115': 0,
            '06114401': 1,
            'total': 3,
        }, '跨学科课程组': {
            'total': 3,
        }, '综合实践环节': {
            '06116102': 3,
            '00117202': 1,
            '00117201': 1,
            'total': 5,
        }
    }
}
