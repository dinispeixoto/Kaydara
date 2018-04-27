from apscheduler.schedulers.background import BackgroundScheduler
from src.NLP import ReminderNLP
from datetime import datetime, timedelta

import time, os

# Init scheduler, running in background and configuring its storage
def init_scheduler():
    global scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore('sqlalchemy', url = os.environ['DATABASE_URL'])
    scheduler.start()

# Schedule a reminder
def schedule_remind(date, user, description):
    scheduler.add_job(ReminderNLP.send_reminder, 'date', run_date = date, args=[user, description])
