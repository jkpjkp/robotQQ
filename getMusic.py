# -*- coding:utf-8 -*-
import json
import traceback

import requests


def getMusic(keywords):
    # 设置url
    url = 'http://120.25.223.76:3000/search?'
    params = {
        'keywords': keywords
    }
    try:
        # 执行请求
        response = requests.get(url=url, params=params)
        text = response.text
        eva = json.loads(text)
        musicId = eva['result']['songs'][0]['id']
        return musicId
    except Exception as e:
        traceback.print_exc()
