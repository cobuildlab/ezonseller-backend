from __future__ import absolute_import, unicode_literals
from celery import shared_task
from account import models as account_models
from payment import models as payment_models
from datetime import datetime
from datetime import timedelta
from celery.schedules import crontab
from django.utils import timezone
from notification import views as notify_views

@shared_task
def disablePlanSubcriptions(instance,payment):
    try:
        user = account_models.User.objects.get(id=instance,id_plan=payment)    
    except account_models.User.DoesNotExist:
        return False
    user.type_plan = 'Free'
    user.id_plan = 0
    user.save()
    payments = payment_models.PaymentHistory.objects.get(user=user, id=payment)
    payments.accept = False
    payments.automatic_payment = False
    payments.save()
    if notify_views.planSubcriptionEnd(user,payments.title):
        return True
    else:
        return False
