#-*- coding:utf8 -*-
# Copyright (c) 2019 barriery
# Python release: 3.7.4
"""
This module is used to simulate the page for the course selection and get thml text.
"""

import re
import hashlib
import requests

__all__ = ['login_and_get_html']

def get_hidden_item(text, item_str):
    ''' get hidden item of html text '''
    item_pattern = re.compile(r'<input type="hidden" name="' + item_str + '" value="(.*?)"')
    item = re.findall(item_pattern, text)[0]
    return item

def login_and_get_html(username, password, xh):
    ''' login and get html text '''
    sen = requests.Session()
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    url = 'http://gsmis.buaa.edu.cn/'
    response = sen.get(url, headers=header)
    text = response.content.decode('utf-8')
    payload = {'username': username,
               'password': password,
               'lt': get_hidden_item(text, 'lt'),
               'execution': get_hidden_item(text, 'execution'),
               '_eventId': get_hidden_item(text, '_eventId')}
    url = 'https://sso.buaa.edu.cn/login?service=http://gsmis.buaa.edu.cn/'
    response = sen.post(url, headers=header, data=payload)

    magic_string = '{body={"xh":"' + xh + '"}}&key=53C2780372E847AEDB1726F136F7BD79CE12B6CA919B6CF4'
    header['X-BUAA-SIGN'] = hashlib.md5(magic_string.encode()).hexdigest().upper()

    url = 'http://gsmis.buaa.edu.cn/api/yuXuanKeApiController.do?getSelectedCourses'
    payload = {'body': '{"xh":"%s"}'%xh}
    response = sen.post(url, headers=header, data=payload)
    selected_courses = response.json().get('attributes').get('kclb')
    course_list = []
    key_map = {'rklsgzzh': 'teacher',
               'kcmc': 'name',
               'qszc': 'week_begin',
               'zzzc': 'week_end',
               'qsjs': 'class_begin',
               'jsjs': 'class_end',
               'kch': 'course_id',
               'skjsbh': 'place',
               'zxf': 'credit',
               'zj': 'weekday',
               'id': 'id_in_system'}
    for item in selected_courses:
        course = {human_firendly_key: item[magic_key] \
                for magic_key, human_firendly_key in key_map.items()}
        course_list.append(course)
    return course_list
