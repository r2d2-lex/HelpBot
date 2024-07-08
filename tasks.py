import asyncio
import logging

from crawler.habr import news_update, delete_old_news
from celery import Celery
from celery.schedules import crontab

celery_app = Celery('tasks', broker='redis://redis:6379/0')


@celery_app.task
def update_news_task():
    try:
        asyncio.run(news_update())
    except RuntimeError as err:
        logging.info(f'ERROR!: {err}')


@celery_app.task
def delete_old_news_task():
    try:
        asyncio.run(delete_old_news())
    except RuntimeError as err:
        logging.info(f'ERROR!: {err}')


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour='*/24'), update_news_task.s(), )
    sender.add_periodic_task(crontab(hour='*/23'), delete_old_news_task.s(), )
