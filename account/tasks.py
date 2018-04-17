from __future__ import absolute_import, unicode_literals
from celery import shared_task
from account import models as account_models
from datetime import datetime
from datetime import timedelta
from celery.schedules import crontab
from django.utils import timezone


@shared_task
def disable_code_recovery_password(instance):
    instance = account_models.User.objects.get(id=instance)
    instance.recovery = ''
    instance.save()
    return True