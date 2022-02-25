import time
import datetime
from zhdate import ZhDate


def getMyb():
    t1 = time.strftime('%Y-%m-%d %H:%M:%S')
    print(t1)
    YYmmdd = time.strftime('%Y%m%d')
    HHMM = int(time.strftime('%H%M'))
    msg1 = '上午' if HHMM < 1200 else '中午' if HHMM < 1400 else '下午' if HHMM < 1730 else '晚上'
    msg1 = time.strftime('%m月%d日') + msg1

    now = int(time.time())
    print(now)
    xb = int(time.mktime(time.strptime(YYmmdd + ' 180000', '%Y%m%d %H%M%S')))
    hour = int((xb - now) / (60 * 60))
    minute = int((xb - now) % (60 * 60) / 60)
    msg2 = str(hour) + '小时' + str(minute) + '分钟' if hour > 0 else str(minute) + '分钟'

    week = int(time.strftime('%w'))
    msg3 = 6 - week

    res = str(t1)+'\n'
    res += '【摸鱼办】提醒您: {}好,摸鱼人!工作再累，一定不要忘记摸鱼哦！' \
          '有事没事起身去茶水间，去厕所，去廊道走走别老在工位上坐着，钱是老板的,但命是自己的。\n'.format(msg1)
    res += '距离下班还有: {}\n'.format(msg2)
    res += '距离周末还有: {}天\n'.format(msg3)
    res += '距离元旦还有: {}天\n'.format(getDifferDayBySolar(1, 1))
    res += '距离春节还有: {}天\n'.format(getDifferDayByLunar(1, 1))
    res += '距离清明还有: {}天\n'.format(getDifferDayBySolar(4, 4))
    res += '距离劳动节还有: {}天\n'.format(getDifferDayBySolar(5, 1))
    res += '距离端午节还有: {}天\n'.format(getDifferDayByLunar(5, 5))
    res += '距离中秋节还有: {}天\n'.format(getDifferDayByLunar(8, 15))
    res += '距离国庆节还有: {}天\n'.format(getDifferDayBySolar(10, 1))
    res += '上班是帮老板赚钱，摸鱼是赚老板的钱！最后，祝愿天下所有摸鱼人，都能愉快的渡过每一天！！！！'

    return res

# 根据阳历查相差天数
def getDifferDayBySolar(m, d):
    d1 = datetime.date.today()
    d2 = datetime.date(d1.year, m, d)
    d3 = d2 if d1 <= d2 else datetime.date(d1.year+1, m, d)
    interval = d3 - d1
    return interval.days

# 根据阴历查相差天数
def getDifferDayByLunar(m, d):
    d1 = datetime.datetime.today()
    d2 = ZhDate(d1.year, m, d).to_datetime()
    d3 = d2 if d1 <= d2 else datetime.datetime(d1.year+1, m, d)
    interval = d3 - d1
    return interval.days
