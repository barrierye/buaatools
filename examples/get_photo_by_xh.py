#-*- coding:utf8 -*-
# Copyright (c) 2019 barriery
# Python release: 3.7.0

import logging

import config
from buaatools.spider import course, login

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M', level=logging.INFO)

if __name__ == '__main__':
    img = course.query_photo_by_xh(stage=config.STAGE,
                                   xh=config.XH,
                                   username=config.USERNAME,
                                   password=config.PASSWORD,
                                   vpn=config.VPN)
    filename = './data/pic.png'
    with open(filename, 'wb') as f:
        f.write(img)
