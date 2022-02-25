from send import send_msg
import all_settings as a


def sendTianQi(ai):
    msg = '南昌天气'
    response = ai.getMsg(a.robotQQ, msg, '')
    resultMsg = response['result']['responses'][0]['actions'][0]['say']
    send_msg({'msg_type': 'group', 'number': a.myGroup, 'msg': resultMsg})


def removeList():
    a.qq_list = []
