# -*- coding:utf-8 -*-
import traceback

import requests
import re

# UserAgent生成库
from fake_useragent import UserAgent

from tk import tkMain


def getImg():
    # 设置url
    url = 'https://3650000.xyz/api/?'
    # 设置请求头
    headers = {
        'User-Agent': UserAgent().random
    }
    params = {
        'type': 'json'
    }
    imgUrl = ''
    returnUrl = './new/output.png'
    try:
        # 执行请求
        response = requests.get(url=url, headers=headers, params=params, timeout=3)
        text = response.text
        text = text.replace('\\', '')
        findLink = re.compile(r'inews.gtimg.com/newsapp_ls/0/.*?/0')
        imgUrl = re.findall(findLink, text)[0]
    except Exception as e:
        print(e)

    # 图片下载
    try:
        # 执行图片下载
        img = requests.get(url='https://' + imgUrl, headers=headers).content
        # 设置图片保存路径
        img_path = './in/mn.jpg'
        with open(img_path, 'wb') as fp:
            # 保存图片
            fp.write(img)
    except Exception as e:
        traceback.print_exc()
    tkMain()
