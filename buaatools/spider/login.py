#-*- coding:utf8 -*-
# Copyright (c) 2019 barriery
# Python release: 3.7.0
"""
This module is used to simulate the page for the course selection and get thml text.
"""

import re
import sys
import time
import random
import logging
import requests

__all__ = ['login']

_LOGGER = logging.getLogger(__name__)

def _get_hidden_items(text):
    ''' get hidden item of html text '''
    item_pattern = re.compile(r'<input type="hidden" name="(.*?)" value="(.*?)"')
    items = re.findall(item_pattern, text)
    return {item[0]: item[1] for item in items}

def _get_default_header(browser_type=None):
    types = ['Chrome', 'IE', 'iOS', 'Android', 'Firefox', 'Opera', 'Safari']
    browser_type = random.choice(types) if browser_type is None else 'Chrome'
    header = None
    if browser_type == 'Chrome':
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit'
                                '/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
    elif 'IE': # Internet Explorer 10
        header = {'User-Agent': 'Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; Trident/5.0)'}
    elif 'iOS': # iPhone6
        header = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit'
                                '/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25'}
    elif 'Android': # Android KitKat
        header = {'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit'
                                '/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36'}
    elif 'Firefox': # Mac Firefox 33
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0'}
    elif 'Opera': # Opera 12.14
        header = {'User-Agent': 'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14'}
    elif 'Safari': # Mac Safari 7
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14'
                                ' (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'}
    return header

def login(target, username, password, vpn=False, need_flag=None):
    if vpn is False:
        session = requests.Session()
        support_target_set = ['http://gsmis.buaa.edu.cn/']
        if (target not in support_target_set):
            _LOGGER.error(f'the target({target}) is not supported.')
            session = [session, False] if need_flag else session
            return session

        header = _get_default_header()
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

        # TODO: check if login success
        '''
        if '请输入您的密码' in response.content.decode('utf-8'):
            _LOGGER.info('fail to login, try to login again.')
            url = 'https://sso.buaa.edu.cn/login?service=https://gsmis.buaa.edu.cn/'
            response = session.get(url, headers=header)
            jsessionid = response.cookies['JSESSIONID']
            url = f'https://sso.buaa.edu.cn/login;jsessionid={jsessionid}?service=https://gsmis.buaa.edu.cn/'
            text = response.content.decode('utf-8')
            payload = _get_hidden_items(text)
            payload['username'] = username
            payload['password'] = password
            response = session.post(url, data=payload)

            _LOGGER.info(f'url: {url}, status code: {response.status_code}')
            if not response:
                _LOGGER.debug(response.content.decode('utf-8'))
                session = [session, False] if need_flag else session
                return session
        '''
        session = [session, True] if need_flag else session
        return session
    else:
        session = requests.Session()
        support_target_set = ['https://gsmis.e.buaa.edu.cn:443', 'https://gsmis.e2.buaa.edu.cn:443']
        if (target not in support_target_set):
            _LOGGER.error(f'the target({target}) is not supported.')
            session = [session, False] if need_flag else session
            return session

        header = _get_default_header()
        #  {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        url = 'https://e2.buaa.edu.cn/users/sign_in'
        #  url = 'https://e.buaa.edu.cn/users/sign_in'

        response = session.get(url, headers=header)
        text = response.content.decode('utf-8')

        payload = _get_hidden_items(text)
        payload['user[login]'] = username
        payload['user[password]'] = password
        payload['user[dymatice_code]'] = 'unknown'
        response = session.post(url, headers=header, data=payload)
        _LOGGER.debug(f'url: {url}, status code: {response.status_code}')
        if not response:
            _LOGGER.debug(response.content.decode('utf-8'))
            session = [session, False] if need_flag else session
            return session

        response = session.get(target)
        _LOGGER.info(f'url: {target}, status code: {response.status_code}')
        if not response:
            _LOGGER.debug(response.content.decode('utf-8'))
            session = [session, False] if need_flag else session
            return session
       
        if '请输入您的密码' in response.content.decode('utf-8'):
            _LOGGER.info('fail to login, try to login again.')
            url = 'https://sso-443.e2.buaa.edu.cn/login?service=https://gsmis.e2.buaa.edu.cn/'
            # url = target
            response = session.get(url, headers=header)
            jsessionid = response.cookies['JSESSIONID']
            url = f'https://sso-443.e2.buaa.edu.cn/login;jsessionid={jsessionid}?service=https://gsmis.e2.buaa.edu.cn/'
            text = response.content.decode('utf-8')
            payload = _get_hidden_items(text)
            payload['username'] = username
            payload['password'] = password
            response = session.post(url, data=payload)

            _LOGGER.info(f'url: {url}, status code: {response.status_code}')
            if not response:
                _LOGGER.debug(response.content.decode('utf-8'))
                session = [session, False] if need_flag else session
                return session
            # TODO
            if '请输入您的密码' in response.content.decode('utf-8'):
                _LOGGER.error('fail to login.')
        
        session = [session, True] if need_flag else session
        return session

