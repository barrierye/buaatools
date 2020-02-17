#-*- coding:utf8 -*-
# Copyright (c) 2019 barriery
# Python release: 3.7.4
"""
This module is used to do some configuration settings.
"""
import datetime
import pytz

#########################
# general configuration #
#########################
# Username of the unified authentication account
USERNAME = 'username'
# Password of the unified authentication account
PASSWORD = 'password'
# Student ID
XH = 'SYxxxxxx'
# VPN
VPN = True


####################################
# configuration for class_schedule #
####################################
# Date of zero week of the current semester
BEGIN_DATE = datetime.datetime(2020, 2, 17, 0, 0, 0, tzinfo=pytz.timezone("Asia/Shanghai"))
# Stage: ['preparatory', 'adjustment', 'ending']
STAGE = 'preparatory'
# Whether to add breaks during class
CLASSBREAK = False
# Student type.
STUDENT_TYPE = '软件工程（硕士）'
# Training program. You can configure it yourself if you need other majors.
# Built-in list: ['软件工程（硕士）', '计算机科学与技术（硕士）', '计算机技术（全日制专硕）']
REQUEST_CREDIT = {
    '计算机技术（全日制专硕）': {
        '思想政治理论课程组': {
            '28111103': 1,
            '28111102': 2,
            'total': 3,
        }, '基础及学科理论课程组': {
            '数学模块': {
                '09112191': 0,
                '09112293': 0,
                '09112294': 0,
                'total': 3,
            }, '计算机模块': {
                '06112306': 0,
                '06112302': 0,
                '06112305': 0,
                '06112304': 0,
                '06112301': 0,
                'total': 9,
            }, 'total': 12,
        }, '专业理论课程组': {
            '计科专硕模块': {
                '06113103': 0,
                '06112303': 0,
                '06113102': 0,
                'total': 2,
            }, '计算机学院专业课模块': {
                r'061132\d{2}': 2,
                'total': 2,
            }, 'total': 4,
        }, '学术素养课程组': {
            '英语模块': {
                '12114112': 0,
                '12114113': 0,
                '12114115': 0,
                'total': 2,
            }, '00114401': 1,
            'total': 3,
        }, '综合实践环节': {
            '06116101': 3,
            '06116902': 3,
            '00117201': 1,
            'total': 7,
            }, 'total': 29,
    }, '计算机科学与技术（硕士）': {
        '思想政治理论课程组': {
            '28111103': 1,
            '28111102': 2,
            'total': 3,
        }, '基础及学科理论课程组': {
            r'06112\d{3}': 9,
            'total': 9,
        }, '专业理论课程组': {
            '计科学硕模块': {
                r'061131\d{2}': 4,
                'total': 4,
            }, r'061132\d{2}': 0,
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
        }, 'total': 31,
    }, '软件工程（硕士）': {
        '思想政治理论课程组': {
            '28111103': 1,
            '28111102': 2,
            'total': 3,
        }, '基础及学科理论课程组': {
            r'06112\d{3}': 9,
            'total': 9,
        }, '专业理论课程组': {
            '必修4分模块': {
                r'061131\d{2}': 4,
                'total': 4,
            }, r'061132\d{2}': 0,
            'total': 8,
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
        }, 'total': 31
    }
}

############################
# previous finished course #
############################
PREVIOUS_FINISHED_CREDIT_LIST = [{
        'name': '算法设计与分析',
        'course_id': '06112301',
        'credit': 3,
    }, {
        'name': '程序设计语言原理',
        'course_id': '06112305',
        'credit': 3,
    }, {
        'name': '高性能计算机体系结构和设计',
        'course_id': '06113104',
        'credit': 2,
    }, {
        'name': '机器学习',
        'course_id': '06113112',
        'credit': 2,
    }, {
        'name': '高等并行计算机体系结构',
        'course_id': '06113218',
        'credit': 2,
    }, {
       'name': '软件技术基础',
        'course_id': '07112407',
        'credit': 2,
    }, {
       'name': '学术英语（硕）',
        'course_id': '12114112',
        'credit': 2,
    }, {
       'name': '中国特色社会主义理论与实践研究',
        'course_id': '28111102',
        'credit': 2,
    },
]
