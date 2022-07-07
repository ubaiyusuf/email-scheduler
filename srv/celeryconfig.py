from celery.schedules import crontab


CELERY_IMPORTS = ('srv.controllers.check_schedule')
CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'UTC+8'

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
    'schedule-check': {
        'task': 'srv.controllers.check_schedule.print_hello',
        # Every minute
        'schedule': crontab(minute="*"),
    }
}