#-*- coding:utf8 -*-
# Copyright (c) 2019 barriery
# Python release: 3.7.4
"""
This module is used to simulate the page for the course selection and get thml text.
"""

import re
import requests

import sys
sys.path.append('..')
from helper import bylogger

__all__ = ['login']

def get_hidden_items(text):
    ''' get hidden item of html text '''
    item_pattern = re.compile(r'<input type="hidden" name="(.*?)" value="(.*?)"')
    items = re.findall(item_pattern, text)
    return {item[0]: item[1] for item in items}

def login(target, username, password, success=[]):
    session = requests.Session()
    support_target_set = ['http://gsmis.buaa.edu.cn/', 'https://icw.buaa.edu.cn/']
    if (target not in support_target_set):
        sys.stderr.write(bylogger.get_colorful_str("[ERROR] the target(%s) is not supported.\n" % target, "red"))
        return None

    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    response = session.get(target, headers=header)
    text = response.content.decode('utf-8')

    payload = get_hidden_items(text)
    payload['username'] = username
    payload['password'] = password
    
    url = 'https://sso.buaa.edu.cn/login?service=' + target
    response = session.post(url, headers=header, data=payload)
    
    if not response:
        sys.stderr.write(bylogger.get_colorful_str("[ERROR] status code is %d\n" % response.status_code, "red"))
        return None

    #TODO: check if login successful

    success.append(True)
    return session
