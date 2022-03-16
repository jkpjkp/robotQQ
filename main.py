import time
import traceback
import all_settings as a
import pypinyin
import random

from baiduAI import baiduAI
from cyjl import getAnyIdiomWord, getAllIdiomDetail, getAnyIdiomDetail
from getImg import getImg
from getMusic import getMusic
from getMyb import getMyb
from receive import rev_msg
from schedulerJob import sendTianQi, removeList
from send import send_msg
from apscheduler.schedulers.background import BackgroundScheduler


def cyjlFail(group, raw_message):
    msg = raw_message + '\n回答错误，再好好想想吧'
    send_msg({'msg_type': 'group', 'number': group, 'msg': msg})
    time.sleep(0.5)
    send_msg({'msg_type': 'group', 'number': group,
              'msg': a.cyNow['word'] + '\n' + a.cyNow['pinyin'] + '\n起源：' + a.cyNow['derivation'] + '\n解释：' + a.cyNow['explanation']})


def cyjl(qq, group, raw_message):
    # 退出成语接龙
    if a.tc == raw_message:
        a.cyjlType = False
        msg = '已退出成语接龙'
        send_msg({'msg_type': 'group', 'number': group, 'msg': msg})
    elif len(raw_message) == 4:
        # 拼音是否正确
        flag1 = a.lastPinYin == pypinyin.lazy_pinyin(raw_message)[0]
        if not flag1:
            cyjlFail(group, raw_message)
            return 0
        # 是否在成语库
        flag2 = False
        allIdiomDetail = getAllIdiomDetail()
        for idiom in allIdiomDetail:
            if raw_message == idiom['word']:
                flag2 = True
                break
        if not flag2:
            cyjlFail(group, raw_message)
            return 0
        # 回答正确
        else:
            accordList = []
            for idiom in allIdiomDetail:
                if pypinyin.lazy_pinyin(idiom['word'])[0] == pypinyin.lazy_pinyin(raw_message[-1])[0]:
                    accordList.append(idiom)
            listLength = len(accordList)
            if listLength == 0:
                send_msg({'msg_type': 'group', 'number': group, 'msg': '你赢了'})
                a.cyjlType = False
                send_msg({'msg_type': 'group', 'number': group, 'msg': '已退出成语接龙'})
            else:
                i = random.randint(0, listLength - 1)
                send_msg({'msg_type': 'group', 'number': group, 'msg': accordList[i]['word']})
                a.cyNow = accordList[i]
                a.lastPinYin = pypinyin.lazy_pinyin(accordList[i]['word'])[-1]
    else:
        msg = '[CQ:at,qq={}]正在进行成语接龙，当前成语\"{}\"，要结束请说退出'.format(qq, a.cyNow['word'])
        send_msg({'msg_type': 'group', 'number': group, 'msg': msg})


if __name__ == '__main__':
    # 初始化百度AI
    ai = baiduAI()

    # 启动定时任务
    scheduler = BackgroundScheduler(timezone="Asia/Shanghai")
    scheduler.add_job(sendTianQi, 'cron', args=[ai], hour=8, minute=0)
    scheduler.add_job(removeList, 'cron', hour=0, minute=0)
    scheduler.start()

    while True:
        try:
            rev = rev_msg()
            # 没有会话
            if 'message_id' not in rev:
                continue
            # 存在会话
            msgId = rev['message_id']
            if len(a.id_list) >= 50:
                a.id_list = []
            if msgId not in a.id_list:
                a.id_list.append(msgId)
                print(rev)
            else:
                continue

            if rev["post_type"] == "message":
                if rev["message_type"] == "group":  # 群聊
                    group = rev['group_id']
                    if "[CQ:at,qq={}]".format(a.robotQQ) in rev["raw_message"]:
                        qq = rev['sender']['user_id']
                        raw_message = rev['raw_message'].replace('[CQ:at,qq={}] '.format(a.robotQQ), '')
                        # 成语接龙进行中
                        if a.cyjlType == True:
                            cyjl(qq, group, raw_message)
                        # 开始成语接龙
                        elif a.cyjl == raw_message:
                            a.cyNow = getAnyIdiomDetail()
                            a.lastPinYin = pypinyin.lazy_pinyin(a.cyNow['word'])[-1]
                            msg = '开始成语接龙，我先来'
                            send_msg({'msg_type': 'group', 'number': group, 'msg': msg})
                            time.sleep(0.5)
                            send_msg({'msg_type': 'group', 'number': group, 'msg': a.cyNow['word']})
                            a.cyjlType = True
                        # 幻影坦克
                        elif a.mn == raw_message:
                            if qq in a.qq_list:
                                msg = '[CQ:at,qq={}]鸡儿给你掰断[CQ:face,id=123]'.format(qq)
                                send_msg({'msg_type': 'group', 'number': group, 'msg': msg})
                            else:
                                send_msg({'msg_type': 'group', 'number': group, 'msg': '[CQ:poke,qq={}]'.format(qq)})
                                getImg()
                                send_msg({'msg_type': 'group', 'number': group,
                                          'msg': '[CQ:image,file={},cache=0]'.format(
                                              'http://120.25.223.76/output.png')})
                                a.qq_list.append(qq)
                        # 网易云
                        elif a.wyy in raw_message:
                            send_msg({'msg_type': 'group', 'number': group, 'msg': '[CQ:poke,qq={}]'.format(qq)})
                            msg = raw_message.replace(a.wyy, '')
                            musicId = getMusic(msg)
                            send_msg({'msg_type': 'group', 'number': group,
                                      'msg': '[CQ:music,type=163,id={}]'.format(musicId)})
                        # 摸鱼办
                        elif a.myb == raw_message:
                            send_msg({'msg_type': 'group', 'number': group, 'msg': '[CQ:poke,qq={}]'.format(qq)})
                            msg = getMyb()
                            send_msg({'msg_type': 'group', 'number': group, 'msg': msg})
                        # 百度AI
                        else:
                            response = ai.getMsg(qq, raw_message, a.sessionIds.get(qq, ''))
                            a.sessionIds[qq] = response['result']['session_id']
                            resultMsg = response['result']['responses'][0]['actions'][0]['say']
                            send_msg({'msg_type': 'group', 'number': group, 'msg': resultMsg})
                else:
                    continue
            else:  # rev["post_type"]=="meta_event":
                continue
        except Exception as e:
            traceback.print_exc()
