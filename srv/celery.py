from celery import Celery
from celery.schedules import crontab

app = Celery()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute='*'),
        test.s('Happy Mondays!'),
    )

@app.task
def test(arg):
    print(arg)

