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
from payment import serializers
from payment import validations
from account.models import User
from datetime import datetime
from datetime import timedelta
from calendar import isleap
from ezonseller import settings
#from payment import tasks
from notification import views as notify_views
import stripe
import math


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
        return Response(serializer.data, status=status.HTTP_200_OK)


class PurchasePlanView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    """
    def paymentPlanPaypal(self, plan, card):
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
    """
    def paymentPlanStripe(self, plan: PlanSubscription, card: CreditCard, user: User):
        stripe.api_key = settings.STRIPE_SECRET_API_KEY
        
        try:
            charge = stripe.Charge.create(
                amount=math.ceil(int(str(plan.cost).replace(".", ''))),  # amount in cents
                currency="usd",
                customer=user.customer_id,
                card=card.card_id,
                description=plan.description
            )
            return {'payment_id': charge.get('id')}
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body['error']
            print("Status is: %s" % e.http_status)
            print("Type is: %s" % err['type'])
            print("Code is: %s" % err['code'])
            # param is '' in this case
            print("Param is: %s" % err['param'])
            print("Message is: %s" % err['message'])
            return None
        except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
            pass
        except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
            pass
        except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
            pass
        except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
            pass
        except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
            pass
        except Exception as e:
            return None
        return None

    def post(self, request):
        plan_id = request.data.get('id_plan')
        card_id = request.data.get('id_card')
        accept = request.data.get('accept')
        user = request.user
        if not plan_id:
            return Response({'message': 'the plan id cant be empty'}, status=status.HTTP_400_BAD_REQUEST)
        if not card_id:
            return Response({'message': 'the credit card id cant be empty'}, status=status.HTTP_400_BAD_REQUEST)
        if not accept:
            return Response({'message': 'the accept term and coditions cant be empty'},
                            status=status.HTTP_400_BAD_REQUEST)
        if accept == 'False':
            return Response({'message': 'You must accept the terms and conditions'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            plan = PlanSubscription.objects.get(id=plan_id)
        except PlanSubscription.DoesNotExist:
            return Response({'message': 'the plan does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            card = CreditCard.objects.get(user=request.user, id=card_id)
        except CreditCard.DoesNotExist:
            return Response(
                {'message': 'the credit card with you buy this plan dont belong a your account, or not exist'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if user.type_plan == "Free" or user.type_plan == "free":
            payment = self.paymentPlanStripe(plan, card, user)
        else:
            return Response({"message": "You already have an active plan and your account"},
                            status=status.HTTP_400_BAD_REQUEST)
        if not payment:
            return Response({'message': 'payment could not be made, please notify your bank distributor'},
                            status=status.HTTP_400_BAD_REQUEST)
        user.type_plan = plan.title
        user.id_plan = plan.id
        user.save()
        plan_finish = extract_date(plan.duration)
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
            unlimited_search=plan.unlimited_search,
            number_search=plan.number_search,
            automatic_payment=plan.automatic_payment
        )
        #expire = plan_finish
        #tasks.disablePlanSubcriptions.apply_async(args=[user.id,payment.id], eta=expire)
        if notify_views.payment_notification(user, card, plan, payment.get('payment_id')):
            print("the email has been send")
        else:
            print("the email not sent") 
        serializer_data = serializers.PaymentHistorySerializer(payment, many=False)
        serializer = serializer_data.data
        serializer['message'] = 'the purchase of the plan has been successful'
        return Response(serializer, status=status.HTTP_201_CREATED)


class CancelSubscriptionView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        query = CancelSubscriptionEdition.objects.all()
        serializer = serializers.CancelSubscriptionSerializers(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        user = User.objects.get(id=request.user.id)
        if not data.get('id_plan'):
            return Response({'message': 'the request with the plan id cant be empty'},
                            status=status.HTTP_400_BAD_REQUEST)
        if not data.get('option'):
            return Response({'message': 'the reason to cancel the plan cant be empty'},
                            status=status.HTTP_400_BAD_REQUEST)
        if not data.get('reason'):
            reason = 'null'
        else:
            reason = data.get('reason')
        try:
            plan = PlanSubscription.objects.get(id=data.get('id_plan'))
        except PlanSubscription.DoesNotExist:
            return Response({'message': 'the plan does not exist'},
                            status=status.HTTP_400_BAD_REQUEST)
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
        if notify_views.cancel_subscription(user, plan.title):
            print("the email has been send")
        else:
            print("the email not sent")
        data = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'type_plan': user.type_plan,
            'message': 'the cancel subscription of plan has been accept successfully',
        }
        return Response(data, status=status.HTTP_201_CREATED)


class CreditCardViewSet(viewsets.ModelViewSet):
    queryset = CreditCard.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.CreditCardSerializers
    http_method_names = ['get', 'put', 'delete', 'post']

    def list(self, request, *args, **kwargs):
        queryset = CreditCard.objects.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def stripe_costumer_card(self, card_id: int, user: User):
        stripe.api_key = settings.STRIPE_SECRET_API_KEY
        card = CreditCard.objects.get(id=card_id)
        if not card.card_id:
            try:
                token = stripe.Token.create(
                    card={
                        "number": card.number_card,
                        "exp_month": int(str(card.date_expiration)[5:7]),
                        "exp_year": int(str(card.date_expiration)[0:4]),
                        "cvc": card.cod_security
                    },
                )
                card.card_id = token.get('card').get('id')
                card.save()
            except stripe.error.CardError as e:
                # Since it's a decline, stripe.error.CardError will be caught
                body = e.json_body
                err = body['error']
                print("Status is: %s" % e.http_status)
                print("Type is: %s" % err['type'])
                print("Code is: %s" % err['code'])
                # param is '' in this case
                print("Param is: %s" % err['param'])
                print("Message is: %s" % err['message'])
                return False
            if not user.customer_id:
                costumer = stripe.Customer.create(
                    description="Customer for "+ user.first_name + user.last_name,
                    email=user.email,
                    source=token.get('id')
                )
                user.customer_id = costumer.get('id')
                user.save()
                return True
            else:
                print("entro")
                costumer = stripe.Customer.retrieve(user.customer_id)
                costumer.sources.create(source=token.get('id'))
                return True
        return False

    def create(self, request, *args, **kwargs):
        context = {'request': request}
        serializer_data = validations.CreditCardCreateValidations(data=request.data, context=context)
        #serializer_data.is_valid(raise_exception=True)
        if serializer_data.is_valid() is False:
            errors_msg = []
            errors_keys = list(serializer_data.errors.keys())
            for i in errors_keys:
                errors_msg.append(str(i) + ": " + str(serializer_data.errors[i][0]))
            error_msg = "".join(errors_msg)
            return Response({'message': errors_msg[0]}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer_data)
        serializer = serializer_data.data
        stripe_card = self.stripe_costumer_card(serializer.get('id'), request.user)
        if not stripe_card:
            card = CreditCard.objects.get(id=serializer.get('id'))
            card.delete()
            return Response({"message": "cant not save the credit card please contact your bank"},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer['message'] = 'the credit card has been saved successfully'
        return Response(serializer, status=status.HTTP_201_CREATED)

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
            return Response({'message': errors_msg[0]}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_update(serializer)
        response_data = serializer.data
        response_data['message'] = 'the information of your credit card has been updated successfully'
        return Response(response_data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'The credit card has deleted form your account'}, status=status.HTTP_200_OK)


class PlanView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request):
        queryset = PlanSubscription.objects.all()
        serializer = serializers.PlanSubscriptionSerializers(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlanViewDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        queryset = PlanSubscription.objects.get(id=pk)
        serializer = serializers.PlanSubscriptionSerializers(queryset, many=False).data
        return Response(serializer, status=status.HTTP_200_OK)


class PaymentHistoryView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        paginator = PageNumberPagination()
        queryset = PaymentHistory.objects.filter(user=request.user).order_by('-id')
        context = paginator.paginate_queryset(queryset, request)
        serializer = serializers.PaymentHistorySerializer(context, many=True)
        return paginator.get_paginated_response(serializer.data)
