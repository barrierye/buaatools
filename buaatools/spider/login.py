#-*- coding:utf8 -*-
# Copyright (c) 2019 barriery
# Python release: 3.7.0
"""
This module is used to simulate the page for the course selection and get thml text.
"""

import re
import sys
import logging
import requests

__all__ = ['login']

_LOGGER = logging.getLogger(__name__)

def _get_hidden_items(text):
    ''' get hidden item of html text '''
    item_pattern = re.compile(r'<input type="hidden" name="(.*?)" value="(.*?)"')
    items = re.findall(item_pattern, text)
    return {item[0]: item[1] for item in items}

def login(target, username, password, vpn=False, need_flag=None):
    if vpn is False:
        session = requests.Session()
        support_target_set = ['http://gsmis.buaa.edu.cn/']
        if (target not in support_target_set):
            _LOGGER.error(f'the target({target}) is not supported.')
            session = [session, False] if need_flag else session
            return session

        header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        response = session.get(target, headers=header)
        text = response.content.decode('utf-8')

        payload = _get_hidden_items(text)
        payload['username'] = username
        payload['password'] = password
        
        url = 'https://sso.buaa.edu.cn/login?service=' + target
        response = session.post(url, headers=header, data=payload)
        
        _LOGGER.info(f'status code: {response.status_code}')
        if not response:
            _LOGGER.error(f'status code: {response.status}')
            _LOGGER.debug(response.content.decode('utf-8'))
            session = [session, False] if need_flag else session
            return session

        #TODO: check if login successful

        session = [session, True] if need_flag else session
        return session
    else:
        session = requests.Session()
        support_target_set = ['https://gsmis.e.buaa.edu.cn:443']
        if (target not in support_target_set):
            _LOGGER.error(f'the target({target}) is not supported.')
            session = [session, False] if need_flag else session
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

        _LOGGER.info(f'status code: {response.status_code}')
        if not response:
            _LOGGER.error(f'status code: {response.status_code}')
            _LOGGER.debug(response.content.decode('utf-8'))
            session = [session, False] if need_flag else session
            return session
        
        session = [session, True] if need_flag else session
        return session

