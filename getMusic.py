# -*- coding:utf-8 -*-
import json
import traceback

import requests
# UserAgent生成库
from fake_useragent import UserAgent


def getMusic(keywords):
    # 设置url
    url = 'http://120.25.223.76:3000/search?'
    headers = {
        'User-Agent': UserAgent().random
    }
    params = {
        'keywords': keywords
    }
    try:
        # 执行请求
        response = requests.get(url=url, headers=headers, params=params)
        text = response.text
        eva = json.loads(text)
        musicId = eva['result']['songs'][0]['id']
        return musicId
    except Exception as e:
        traceback.print_exc()

if __name__ == '__main__':
    print(getMusic('onelastkiss'))
