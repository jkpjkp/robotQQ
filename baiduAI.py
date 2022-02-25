import json
import time

import requests
import random


class baiduAI:
    def __init__(self):
        # 鉴权Token
        self.accessToken = ''
        # 机器人ID
        self.serviceId = 'S65310'
        # token类错误编码
        self.tokenError = [100, 110, 111]

    def makeError(self, code):
        if code in self.tokenError:
            self.getToken()
        else:
            time.sleep(2)

    def getToken(self):
        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials' \
               '&client_id=ovqNi1SkbrSzWbr3ckTf7XXz' \
               '&client_secret=L3smYfk0GDvuPzdf6GpbN2aY0s7jtd7f'
        response = requests.get(host)
        self.accessToken = response.json().get('access_token', '')

    def getMsg(self, qq, msg, sessionId):
        if '' == self.accessToken:
            self.getToken()

        url = 'https://aip.baidubce.com/rpc/2.0/unit/service/v3/chat?access_token=' + self.accessToken
        post_data = {
            'version': '3.0',
            'service_id': self.serviceId,
            'session_id': sessionId,
            'log_id': str(random.random()),
            'request': {
                'terminal_id': qq,
                'query': msg
            }
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(post_data), headers=headers).json()
        print(response)
        if 0 != response.get('error_code', ''):
            print('AI-ERROR = ' + response.get('error_code'))
            self.makeError(response.get('error_code'))
            self.getMsg(qq, msg, sessionId)
        return response
