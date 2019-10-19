#-*- coding:utf8 -*-
# Copyright (c) 2019 barriery
# Python release: 3.7.0

import platform

__all__ = ['get_colorful_str']

def get_colorful_str(string, color):
    ''' get colorful str '''
    if platform.system() == "Windows":
        return string
    color_map = {'black': '30',
                 'red': '31',
                 'green': '32',
                 'yellow': '33',
                 'blue': '34',
                 'purple': '35',
                 'cyan': '36',
                 'white': '37'}
    color_number = color_map.get(color)
    if not color_number:
        return string
    return "\033[1;%sm%s\033[0m" % (color_number, string)
