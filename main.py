import traceback
import all_settings as a

from baiduAI import baiduAI
from getImg import getImg
from getMyb import getMyb
from receive import rev_msg
from schedulerJob import sendTianQi, removeList
from send import send_msg
from apscheduler.schedulers.background import BackgroundScheduler


if __name__ == '__main__':
    # 初始化百度AI
    ai = baiduAI()

    # 启动定时任务
    scheduler = BackgroundScheduler()
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
                        if '清空瑟图上限' in rev['raw_message']:
                            a.qq_list = []
                        # 图片
                        elif a.mn in rev['raw_message']:
                            if qq in a.qq_list:
                                msg = '[CQ:at,qq={}] 当日瑟图上限\n＞︿＜'.format(qq)
                                send_msg({'msg_type': 'group', 'number': group, 'msg': msg})
                            else:
                                send_msg({'msg_type': 'group', 'number': group, 'msg': '[CQ:poke,qq={}]'.format(qq)})
                                getImg()
                                send_msg({'msg_type': 'group', 'number': group,
                                          'msg': '[CQ:image,file={},cache=0]'.format('http://120.25.223.76/output.png')})
                                a.qq_list.append(qq)
                        # 转语音
                        elif a.yy in rev['raw_message']:
                            send_msg({'msg_type': 'group', 'number': group, 'msg': '[CQ:poke,qq={}]'.format(qq)})
                            send_msg({'msg_type': 'group', 'number': group, 'msg': '[CQ:tts,text={}]'.format(
                                rev['raw_message'].split(a.yy)[1].replace('\r', '').replace('\n', ''))})
                        # 摸鱼办
                        elif a.myb in rev['raw_message']:
                            send_msg({'msg_type': 'group', 'number': group, 'msg': '[CQ:poke,qq={}]'.format(qq)})
                            msg = getMyb()
                            send_msg({'msg_type': 'group', 'number': group, 'msg': msg})
                        # 百度AI
                        else:
                            msg = rev['raw_message'].replace('[CQ:at,qq={}] '.format(a.robotQQ), '')
                            response = ai.getMsg(qq, msg, a.sessionIds.get(qq, ''))
                            a.sessionIds[qq] = response['result']['session_id']
                            resultMsg = response['result']['responses'][0]['actions'][0]['say']
                            send_msg({'msg_type': 'group', 'number': group, 'msg': resultMsg})
                else:
                    continue
            else:  # rev["post_type"]=="meta_event":
                continue
        except Exception as e:
            traceback.print_exc()
