import time
import all_settings as a

from apscheduler.schedulers.background import BackgroundScheduler

from schedulerJob import removeList

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(removeList, 'cron', hour=15, minute=22)
    scheduler.start()
    while True:
        print(a.qq)
        time.sleep(1)
