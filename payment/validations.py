from rest_framework import serializers
from account.models import User
from payment.models import PlanSubscription, PlanSubscriptionList, TermsCondition, CreditCard, PaymentHistory
from django.utils.translation import ugettext_lazy as _
import re


class CreditCardValidations(serializers.ModelSerializer):
    name = serializers.CharField()
    type_card = serializers.CharField()
    number_card = serializers.CharField()
    cod_security = serializers.CharField()
    date_creation = serializers.DateField()
    date_expiration = serializers.DateField()

    class Meta:
        model = CreditCard
        fields = ('name', 'type_card', 'number_card', 'cod_security',
                  'data_creation', 'date_expiration')

    def validate(self, attrs):
        if not attrs.get('name'):
            raise serializers.ValidationError({'message': [_('The name of credit card is required')]})
        if not attrs.get('type_card'):
            raise serializers.ValidationError({'message': [_('The type of card is required')]})
        if not attrs.get('number_card'):
            raise serializers.ValidationError({'message': [_('The number card is required')]})
        if not attrs.get('cod_security'):
            raise serializers.ValidationError({'message': [_('The security code is required')]})
        if not attrs.get('date_creation'):
            raise serializers.ValidationError({'message': [_('the date of creation is required')]})
        if not attrs.get('date_expiration'):
            raise serializers.ValidationError({'message': [_('the date of creation is required')]})
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        card = CreditCard.objects.create(**validated_data)
        return card


class CreditCardCreateValidations(CreditCardValidations):

    def validated_number_card(self, number_card):
        if not re.match(r'[0-9]',number_card):
            raise serializers.ValidationError({'message': [_('the credit card can only have numbers')]})
        return number_card
