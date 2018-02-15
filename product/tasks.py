from __future__ import absolute_import, unicode_literals
from celery.decorators import periodic_task
from celery import shared_task
from product import models as product_models
from datetime import datetime
from datetime import timedelta
from celery.schedules import crontab
from django.utils import timezone
from django.contrib.postgres.aggregates import ArrayAgg


# @periodic_task(run_every=crontab(minute=0, hour=12), name="verify_status_amazon_account", ignore_result=True)
# def verify_status_amazon_account():
#     product_models.AmazonAssociates.objects.all().update(limit=10)
#     return True

# @shared_task
# def verifyStatusAmazonAccount(instance,country):
#     print(instance)
#     print(country)
#     amazon = product_models.AmazonAssociates.objects.get(user=instance, country=country)
#     amazon.limit = 10
#     amazon.save()
#     return True