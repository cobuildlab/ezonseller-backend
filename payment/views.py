from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from payment.models import PlanSubscription, PlanSubscriptionList, TermsCondition, CreditCard, PaymentHistory
from payment import serializers
from payment import validations
from account.models import User
from datetime import datetime
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


class TermsConditionView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        queryset = TermsCondition.objects.get(id=1)
        serializer = serializers.TermsConditionSerializers(queryset)
        return Response(serializer.data)


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
        serializer = validations.AmazonKeyValidations(data=request.data,
                                                      context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=STATUS['201'])

    def update(self, request, *args, **kwargs):
        #partial = kwargs.pop('partial', False)
        data = request.data
        instance = self.get_object()
        if not data.get('associate_tag'):
            return Response({'message': 'the amazon associate username cant be empty'}, status=STATUS['400'])
        if not data.get('access_key_id'):
            return Response({'message': 'The amazon access key is required'}, status=STATUS['400'])
        if not data.get('secrect_access_key'):
            return Response({'message': 'The amazon secrect key is required'}, status=STATUS['400'])
        try:
            amazon = AmazonAssociates.objects.get(associate_tag=data.get('associate_tag'))
        except AmazonAssociates.DoesNotExist:
            return Response({'message': 'the amazon associate username not exit'}, status=STATUS['400'])
        amazon.access_key_id=data.get('access_key_id')
        amazon.secrect_access_key = data.get('secrect_access_key')
        amazon.save()
        serializer = self.get_serializer(amazon)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'The credit card has deleted form your account'})