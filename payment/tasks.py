from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from account import models as account_models
from payment import models as payment_models
from datetime import datetime
from datetime import timedelta
from celery.schedules import crontab
from django.utils import timezone
from notification import views as notify_views
from django.contrib.postgres.aggregates import ArrayAgg

# @shared_task
# def disablePlanSubcriptions(instance,payment):
#     try:
#         user = account_models.User.objects.get(id=instance,id_plan=payment)    
#     except account_models.User.DoesNotExist:
#         return False
#     user.type_plan = 'Free'
#     user.id_plan = 0
#     user.save()
#     payments = payment_models.PaymentHistory.objects.get(user=user, id=payment)
#     payments.accept = False
#     payments.automatic_payment = False
#     payments.save()
#     if notify_views.planSubcriptionEnd(user,payments.title):
#         return True
#     else:
#         return False

# @periodic_task(run_every=crontab(minute=0, hour=12), name="disablePlanSubcriptions", ignore_result=True)
# def disablePlanSubcriptions():
#     return True


@periodic_task(run_every=crontab(minute=0, hour=12), name="disable_plan_subscriptions", ignore_result=True)
def disable_plan_subscriptions():
    datenow = timezone.now() 
    users = account_models.User.objects.all().exclude(type_plan="Free")
    users = users.aggregate(userid=ArrayAgg('id')) 
    payments = payment_models.PaymentHistory.objects.filter(user__in=users.get('userid')).exclude(accept=False)
    for payment in payments:
        if payment.date_finish < datenow:
            user = account_models.User.objects.get(id=payment.user.id)
            user.type_plan = 'Free'
            user.id_plan = 0
            user.save()
            payment.accept = False
            payment.automatic_payment = False
            payment.save()
            if notify_views.planSubcriptionEnd(user, payment.title):
                print("email send")
            else:
                print("email problems")
    return True