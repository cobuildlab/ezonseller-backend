from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from account import models as account_models
from payment import models as payment_models
from datetime import datetime, date
from datetime import timedelta
from calendar import isleap
from celery.schedules import crontab
from django.utils import timezone
from notification import views as notify_views
from django.contrib.postgres.aggregates import ArrayAgg
import stripe
import math
from ezonseller import settings


def add_years(d, years):
    new_year = d.year + years
    try:
        return d.replace(year=new_year)
    except ValueError:
        if d.month == 2 and d.day == 29 and isleap(d.year) and not isleap(new_year):
            return d.replace(year=new_year, day=28)
        raise


def extract_date(date):
    number = date[0:1]
    string = date[2:]
    months = {'1': 5, '3': 15, '6': 30}
    years = {'1': 1, '2': 2, '3': 3}
    now = datetime.now()
    if string == 'month':
        mount = months[number]
        end_date = now + timedelta(6 * mount)
    if string == 'year':
        year = years[number]
        end_date = add_years(now, year)
    return end_date


@shared_task
def execute_payment(payment_info):
    """
    Execute the pending payment
    - If user is not active, does not do anything
    :param payment_info:
    :return:
    """
    stripe.api_key = settings.STRIPE_SECRET_API_KEY
    user = account_models.User.objects.get(id=payment_info.user.id)
    plan = payment_models.PlanSubscription.objects.get(id=payment_info.id_plan)
    card = payment_models.CreditCard.objects.get(id=payment_info.id_card)

    if user.is_active == False:
        raise ValueError("Inactives user don't suppose to pay")

    if user.attemptPayment == 0:
        notify_views.payment_failure(user, plan, 0)
        print("email has send user disable")
        user.is_active = False
        user.attemptPayment = -1
        user.save()
        return "user is disable"
    try:
        # Charge current PaymentHistory
        charge = stripe.Charge.create(
            amount=math.ceil(int(str(plan.cost).replace(".", ''))),  # amount in cents
            currency="usd",
            customer=user.customer_id,
            card=card.card_id,
            description=plan.description
        )
        # Update payment info
        payment_id = charge.get('id')
        payment_info.paymentId = payment_id
        payment_info.save()

        user.attemptPayment = 5
        user.save()

        if notify_views.payment_automatic(user, card, plan, payment_id):
            print("the email has been send")
        else:
            print("the email not sent")

        return "The payment is correct"
    except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught
        body = e.json_body
        err = body['error']
        message = "payment problem " + str(err['message'])
        print(message)
    except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
        print(str(e))
        pass
    except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        print(str(e))
        pass
    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        print(str(e))
        pass
    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        print(str(e))
        pass
    except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        print(str(e))
        pass
    except Exception as e:
        message = "payment problem " + str(e)
        print(message)

    if notify_views.payment_failure(user, plan, user.attemptPayment):
        print("email has send payment failure")
    else:
        print("email has send payment failure")

    rest = user.attemptPayment - 1
    user.attemptPayment = rest
    user.is_active = False
    user.save()

    return "The payment can not be made"


@periodic_task(run_every=crontab(minute=0, hour=12), name="automatic_payment", ignore_result=True)
def automatic_payment():
    date_now = timezone.now()
    payments = payment_models.PaymentHistory.objects.exclude(accept=False).exclude(automatic_payment=False).exclude(
        user_id__is_active=False).exclude(paymentId__iexact='')
    for payment in payments:
        date_start = payment.date_start + timedelta(days=payment.days_free)
        if date_start <= date_now:
            execute_payment.apply_async(args=[payment])
    return True


@periodic_task(run_every=crontab(minute=30, hour=12), name="disable_plan_subscriptions", ignore_result=True)
def disable_plan_subscriptions():
    date_now = timezone.now()
    users = account_models.User.objects.all().exclude(type_plan="Free").exclude(is_superuser=True)
    users = users.aggregate(userid=ArrayAgg('id'))
    payments = payment_models.PaymentHistory.objects.filter(user__in=users.get('userid')). \
        exclude(accept=False).exclude(automatic_payment=True)
    for payment in payments:
        if payment.date_finish <= date_now:
            user = account_models.User.objects.get(id=payment.user.id)
            user.type_plan = 'Free'
            user.id_plan = 0
            user.save()
            payment.accept = False
            payment.automatic_payment = False
            payment.save()
            if notify_views.plan_subscription_end(user, payment.title):
                print("email send")
            else:
                print("email problems")
    return True


@shared_task
def create_payment_history(payment_info):
    """

    :param payment_info: payment with expired date = date_now + 1 day
    :return:
    """
    # Add date now 1 day
    date_start = datetime.now() + timedelta(days = 1)
    user = account_models.User.objects.get(id=payment_info.user.id)
    plan = payment_models.PlanSubscription.objects.get(id=payment_info.id_plan)
    card = payment_models.CreditCard.objects.get(id=payment_info.id_card)
    plan_finish = extract_date(plan.duration) + timedelta(days =1)

    try:
        payment_models.PaymentHistory.objects.create(
            user=user,
            id_plan=plan.id,
            paymentId="",
            title=plan.title,
            cost=plan.cost,
            image=plan.image,
            description=plan.description,
            id_card=card.id,
            name=card.first_name + card.last_name,
            number_card=card.number_card,
            cod_security=card.cod_security,
            date_expiration=card.date_expiration,
            date_start=date_start,
            date_finish=plan_finish,
            accept=True,
            unlimited_search=plan.unlimited_search,
            number_search=plan.number_search,
            automatic_payment=plan.automatic_payment,
        )
        payment_info.renovate = True
        payment_info.accept = False
        payment_info.save()

        return True

    except Exception as e:
        print(e)

        return False


@periodic_task(run_every=crontab(minute=0, hour=12), name="check_payment_history", ignore_result=True)
def check_payment_history():
    payments = payment_models.PaymentHistory.objects.exclude(accept=False).exclude(automatic_payment=False).exclude(
        user_id__is_active=False).exclude(renovate=True).exclude(paymentId__exact='').exclude(user_id__is_active=False)
    date_now = timezone.now() + timedelta(days = 1)
    for payment in payments:
       if payment.date_finish <= date_now:
           create_payment_history.apply_async(args=[payment])
    return True