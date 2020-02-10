#-*- coding:utf8 -*-
# Copyright (c) 2019 barriery
# Python release: 3.7.0
"""
This module is used to simulate the page for the course selection and get thml text.
"""

import re
import requests

import sys
from buaatools.helper import logger

__all__ = ['login', 'login_with_vpn']

def _get_hidden_items(text):
    ''' get hidden item of html text '''
    item_pattern = re.compile(r'<input type="hidden" name="(.*?)" value="(.*?)"')
    items = re.findall(item_pattern, text)
    return {item[0]: item[1] for item in items}

def login_with_vpn(target, username, password, need_flag=None):
    session = requests.Session()
    support_target_set = ['https://gsmis.e.buaa.edu.cn:443']
    if (target not in support_target_set):
        sys.stderr.write(logger.get_colorful_str("[ERROR] the target(%s) is not supported.\n" % target, "red"))
        if need_flag:
            session = [session, False]
        return session

    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    url = 'https://e.buaa.edu.cn/users/sign_in'
    response = session.get(url, headers=header)
    text = response.content.decode('utf-8')

    payload = _get_hidden_items(text)
    payload['user[login]'] = username
    payload['user[password]'] = password
    payload['user[dymatice_code]'] = 'unknown'
    response = session.post(url, headers=header, data=payload)

    response = session.get(target)

    if not response:
        sys.stderr.write("[ERROR] status code is %d\n" % response.status_code)
        if need_flag:
            session = [session, False]
        return session
    if need_flag:
        session = [session, True]
    return session

def login(target, username, password, need_flag=None):
    session = requests.Session()
    support_target_set = ['http://gsmis.buaa.edu.cn/']
    if (target not in support_target_set):
        sys.stderr.write(logger.get_colorful_str("[ERROR] the target(%s) is not supported.\n" % target, "red"))
        if need_flag:
            session = [session, False]
        return session

    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    response = session.get(target, headers=header)
    text = response.content.decode('utf-8')

    payload = _get_hidden_items(text)
    payload['username'] = username
    payload['password'] = password
    
    url = 'https://sso.buaa.edu.cn/login?service=' + target
    response = session.post(url, headers=header, data=payload)
    
    if not response:
        sys.stderr.write(logger.get_colorful_str("[ERROR] status code is %d\n" % response.status_code, "red"))
        if need_flag:
            session = [session, False]
        return session

    #TODO: check if login successful

    if need_flag:
        session = [session, True]

    return session
