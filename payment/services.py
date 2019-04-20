from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from payment.pagination import PaymentHistoryPaginations
from payment.models import PlanSubscription, PlanSubscriptionList, \
    TermsCondition, CreditCard, PaymentHistory, CancelSubscription, \
    CancelSubscriptionEdition, CancelSubscriptionList
from django.core import serializers
from payment import validations
from account.models import User
from datetime import datetime
from datetime import timedelta
from calendar import isleap
from ezonseller import settings
# from payment import tasks
from notification import views as notify_views
import stripe
import math
from account import models as account_models
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect


def getAllPlan(request):
    plan = serializers.serialize('json', PlanSubscription.objects.all())
    return HttpResponse(plan, status=status.HTTP_200_OK)


def getPlan(request, id):
    plan = serializers.serialize('json', PlanSubscription.objects.filter(id=id))
    return HttpResponse(plan, status=status.HTTP_200_OK)
