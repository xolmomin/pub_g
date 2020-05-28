import os
from celery import Celery, shared_task
from celery.schedules import crontab
from celery.task import periodic_task

app = Celery('tasks', broker='redis://127.0.0.1:6379')


# @periodic_task(run_every=(crontab(minute='1')), name="some_task", ignore_result=True)
@app.task(name='some_task')
def some_task():
    print('123')


@app.task(name='exact_time_run')
def exact_time_run():
    print('hello world')
