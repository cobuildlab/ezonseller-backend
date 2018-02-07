from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from payment.pagination import PaymentHistoryPaginations
from payment.models import PlanSubscription, PlanSubscriptionList, \
    TermsCondition, CreditCard, PaymentHistory, CancelSubscription, \
    CancelSubscriptionEdition, CancelSubscriptionList
from payment import serializers
from payment import validations
from account.models import User
from datetime import datetime
from datetime import timedelta
from calendar import isleap
from payment.pagination import paginate
import paypalrestsdk
from ezonseller import settings
from payment import tasks
import re
from rest_framework.decorators import detail_route, list_route
from notification import views as notify_views

STATUS = {
    "200": status.HTTP_200_OK,
    "201": status.HTTP_201_CREATED,
    "202": status.HTTP_202_ACCEPTED,
    "204": status.HTTP_204_NO_CONTENT,
    "400": status.HTTP_400_BAD_REQUEST,
    "401": status.HTTP_401_UNAUTHORIZED,
    "404": status.HTTP_404_NOT_FOUND,
    "500": status.HTTP_500_INTERNAL_SERVER_ERROR
}


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
    mounths = {'1': 5, '3': 15, '6': 30}
    years = {'1': 1, '2': 2, '3': 3}
    now = datetime.now()
    if string == 'mounth':
        mount = mounths[number]
        endDate = now + timedelta(6*mount)
    if string == 'year':
        year = years[number]
        endDate = add_years(now, year)
    return endDate


class TermsConditionView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        queryset = TermsCondition.objects.get(id=1)
        serializer = serializers.TermsConditionSerializers(queryset)
        return Response(serializer.data)


class PurchasePlanView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def paymentPlan(self, plan, card):
        mounth = str(card.date_expiration)
        year = mounth
        paypalrestsdk.configure({
            'mode': settings.PAYPAL_MODE,
            'client_id': settings.PAYPAL_CLIENT_ID,
            'client_secret': settings.PAYPAL_CLIENT_SECRECT})
        data = {
            "intent": "sale",
            "payer": {
                "payment_method": "credit_card",
                "funding_instruments": [
                    {
                        "credit_card": {
                            "number": str(card.number_card),
                            "type": str(card.type_card),
                            "expire_month": mounth[5:7],
                            "expire_year": year[0:4],
                            "cvv2": str(card.cod_security),
                            "first_name":card.first_name,
                            "last_name": card.last_name
                        }
                    }
                ]
            },
            "transactions": [
                {
                    "amount": {
                        "total": str(plan.cost),
                        "currency": "USD"
                    },
                    "description": str(plan.description[0:126])
                }
            ]
        }
        payment = paypalrestsdk.Payment(data)
        if payment.create():
            print("Payment created successfully")
            return {'payment_id': payment.id}
        else:
            print(payment.error)
            return None
        return None

    def post(self, request):
        plan_id = request.data.get('id_plan')
        card_id = request.data.get('id_card')
        accept = request.data.get('accept')
        automatic = request.data.get('automatic')
        if not plan_id:
            return Response({'message': 'the plan id cant be empty'}, status=STATUS['400'])
        if not card_id:
            return Response({'message': 'the credit card id cant be empty'}, status=STATUS['400'])
        if not accept:
            return Response({'message': 'the accept term and coditions cant be empty'}, status=STATUS['400'])
        if not automatic:
            return Response({'message': 'the payment automatic cant be empty'}, status=STATUS['400'])
        
        if accept == 'False':
            return Response({'message': 'You must accept the terms and conditions'}, status=STATUS['400'])
        if not automatic == 'True' and not automatic == "False":
            return Response({'message': 'this field only contains true or false'},status=STATUS['400'])
        try:
            plan = PlanSubscription.objects.get(id=plan_id)
        except PlanSubscription.DoesNotExist:
            return Response({'message': 'the plan does not exist'}, status=STATUS['400'])
        try:
            card = CreditCard.objects.get(user=request.user, id=card_id)
        except CreditCard.DoesNotExist:
            return Response(
                {'message': 'the credit card with you buy this plan dont belong a your account, or not exist'},
                status=STATUS['400']
            )

        payment = self.paymentPlan(plan, card)
        if not payment:
            return Response({'message': 'payment could not be made, please notify your bank distributor'},
                            status=STATUS['400'])

        user = User.objects.get(username=request.user)
        user.type_plan = plan.title
        user.id_plan = plan.id
        user.save()
        plan_finish = extract_date(plan.duration)
        numberpayment = payment.get('payment_id')
        payment = PaymentHistory.objects.create(
            user=user,
            id_plan=plan.id,
            paymentId=payment.get('payment_id'),
            title=plan.title,
            cost=plan.cost,
            image=plan.image,
            description=plan.description,
            id_card=card.id,
            name=card.first_name + card.last_name,
            number_card=card.number_card,
            cod_security=card.cod_security,
            date_expiration=card.date_expiration,
            date_start=datetime.now(),
            date_finish=plan_finish,
            accept=True,
            automatic_payment=automatic 
        )
        expire = plan_finish
        tasks.disablePlanSubcriptions.apply_async(args=[user.id,payment.id], eta=expire)
        if notify_views.payment_notification(user,card,plan,numberpayment):
            print("the email has been send")
        else:
            print("the email not sent") 
        serializer_data = serializers.PaymentHistorySerializer(payment, many=False)
        serializer = serializer_data.data
        serializer['message'] = 'the purchase of the plan has been successful'
        return Response(serializer, status=STATUS['201'])


class CancelSubscriptionView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        query = CancelSubscriptionEdition.objects.all()
        serializer = serializers.CancelSubscriptionSerializers(query, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        user = User.objects.get(id=request.user.id)
        if not data.get('id_plan'):
            return Response({'message': 'the request with the plan id cant be empty'}, status=STATUS['400'])
        if not data.get('option'):
            return Response({'message': 'the reason to cancel the plan cant be empty'}, status=STATUS['400'])
        if not data.get('reason'):
            reason = 'null'
        else:
            reason = data.get('reason')
        try:
            plan = PlanSubscription.objects.get(id=data.get('id_plan'))
        except PlanSubscription.DoesNotExist:
            return Response({'message': 'the plan does not exist'}, status=STATUS['400'])
        user.type_plan = 'Free'
        user.id_plan = 0
        user.save()
        payments = PaymentHistory.objects.filter(user=user, id_plan=plan.id).order_by('-id')[:1]
        user_payment = payments[0]
        user_payment.accept = False
        user_payment.automatic_payment = False
        user_payment.save()
        cancel = CancelSubscription.objects.get_or_create(
            user=user,
            plan=plan,
            option=data.get('option'),
            reason=reason,
        )
        return Response({'message': 'the cancel subscription of plan has been accept successfully'})


class CreditCardViewSet(viewsets.ModelViewSet):
    queryset = CreditCard.objects.all()
    serializer_class = serializers.CreditCardSerializers
    http_method_names = ['get', 'put', 'delete', 'post']

    def list(self, request, *args, **kwargs):
        queryset = CreditCard.objects.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        context = {'request': request}
        serializer_data = validations.CreditCardCreateValidations(data=request.data,
                                                      context=context)
        #serializer_data.is_valid(raise_exception=True)
        if serializer_data.is_valid() is False:
            errors_msg = []
            errors_keys = list(serializer_data.errors.keys())
            for i in errors_keys:
                errors_msg.append(str(i) + ": " + str(serializer_data.errors[i][0]))
            error_msg = "".join(errors_msg)
            return Response({'message': errors_msg[0]}, status=STATUS['400'])
        self.perform_create(serializer_data)
        serializer = serializer_data.data
        serializer['message'] = 'the credit card has been saved successfully'
        return Response(serializer, status=STATUS['201'])

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = validations.CreditCardValidations(instance, data=request.data, 
        context={'request': request})
        #serializer.is_valid(raise_exception=True)
        if serializer.is_valid() is False:
            errors_msg = []
            errors_keys = list(serializer.errors.keys())
            for i in errors_keys:
                errors_msg.append(str(i) + ": " + str(serializer.errors[i][0]))
            error_msg = "".join(errors_msg)
            return Response({'message': errors_msg[0]}, status=STATUS['400'])
        self.perform_update(serializer)
        response_data = serializer.data
        response_data['message'] = 'the information of your credit card has been updated successfully'
        return Response(response_data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'The credit card has deleted form your account'})


class PlanView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request):
        queryset = PlanSubscription.objects.all()
        serializer = serializers.PlanSubscriptionSerializers(queryset, many=True)
        return Response(serializer.data)


class PaymentHistoryView(ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        paginator = PageNumberPagination()
        queryset = PaymentHistory.objects.filter(user=request.user).order_by('id')
        context = paginator.paginate_queryset(queryset, request)
        serializer = serializers.PaymentHistorySerializer(context, many=True)
        return paginator.get_paginated_response(serializer.data)


