import schedule
import time
from threading import Thread

class Scheduler:
    def __init__(self):
        self.jobs = []

    def schedule_backup(self, interval, job_func, *args):
        job = schedule.every(interval).seconds.do(job_func, *args)
        self.jobs.append(job)

    def start(self):
        def run_continuously():
            while True:
                schedule.run_pending()
                time.sleep(1)
        
        thread = Thread(target=run_continuously)
        thread.daemon = True
        thread.start()
