from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from payment.pagination import PaymentHistoryPagination
from payment.models import PlanSubscription, PlanSubscriptionList, TermsCondition, CreditCard, PaymentHistory
from payment import serializers
from payment import validations
from account.models import User
from datetime import datetime
from datetime import timedelta
from  calendar import isleap
from rest_framework.decorators import detail_route, list_route

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

    def post(self, request):
        plan_id = request.data.get('id_plan')
        card_id = request.data.get('id_card')
        accept = request.data.get('accept')
        if accept == 'False':
            return Response({'message': 'You must accept the terms and conditions'}, status=STATUS['400'])
        try:
            plan = PlanSubscription.objects.get(id=plan_id)
        except PlanSubscription.DoesNotExist:
            return Response({'message': 'the plan does not exist'}, status=STATUS['400'])
        try:
            user = User.objects.get(username=request.user)
            card = CreditCard.objects.get(user=user, id=card_id)
        except CreditCard.DoesNotExist:
            return Response(
                {'message': 'the credit card with you buy this plan dont belong a your account, or not exist'},
                status=STATUS['400']
            )
        plan_finish = extract_date(plan.duration)

        payment = PaymentHistory.objects.create(
            user=user,
            title=plan.title,
            cost=plan.cost,
            name=card.name,
            number_card=card.number_card,
            cod_security=card.cod_security,
            date_expiration=card.date_expiration,
            date_start=datetime.now(),
            date_finish=plan_finish,
            accept=True
        )
        serializer = serializers.PaymentHistorySerializer(payment, many=False)
        return Response(serializer.data, status=STATUS['201'])

    def put(self, request):
        return Response({})


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
        serializer = validations.CreditCardCreateValidations(data=request.data,
                                                      context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=STATUS['201'])

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = validations.CreditCardValidations(instance, data=request.data, 
        context={'request': request})
        serializer.is_valid(raise_exception=True)
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
    serializer_class = serializers.PaymentHistorySerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PaymentHistoryPagination

    def get_queryset(self):
        queryset = PaymentHistory.objects.all()
        return queryset


