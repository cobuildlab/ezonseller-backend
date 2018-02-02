from rest_framework import serializers
from account.models import User
from payment.models import PlanSubscription, PlanSubscriptionList, TermsCondition, CreditCard, PaymentHistory
from django.utils.translation import ugettext_lazy as _
import re


class CreditCardValidations(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True, max_length=50)
    last_name = serializers.CharField(required=True, max_length=50)
    type_card = serializers.CharField(required=True, max_length=20)
    number_card = serializers.CharField(required=True, min_length=6, max_length=20)
    cod_security = serializers.CharField(required=True, max_length=4)
    date_expiration = serializers.DateField()

    class Meta:
        model = CreditCard
        fields = ('id', 'first_name', 'last_name', 'type_card', 'number_card', 'cod_security',
                  'date_expiration')

    def validate_number_card(self, number_card):
        if self.context["request"].method != 'PUT':
            if not re.match(r'^[-+]?[0-9]+$',number_card):
                raise serializers.ValidationError('the credit card can only have numbers')
        return number_card
    
    def validate_cod_security(self, cod_security):
        if self.context["request"].method != 'PUT':
            if not re.match(r'^[-+]?[0-9]+$',cod_security):
                raise serializers.ValidationError('the security code can only have numbers')
        return cod_security

    def validate(self, attrs):
        if not attrs.get('first_name'):
            raise serializers.ValidationError({'message': [_('The first_name of credit card is required')]})
        if not attrs.get('last_name'):
            raise serializers.ValidationError({'message': [_('The last_name of credit card is required')]})
        if not attrs.get('type_card'):
            raise serializers.ValidationError({'message': [_('The type of card is required')]})
        if not attrs.get('number_card'):
            raise serializers.ValidationError({'message': [_('The number card is required')]})
        if not attrs.get('cod_security'):
            raise serializers.ValidationError({'message': [_('The security code is required')]})
        if not attrs.get('date_expiration'):
            raise serializers.ValidationError({'message': [_('the date of creation is required')]})
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        card = CreditCard.objects.create(**validated_data)
        return card

    def update(self, instance, validated_data):
        if validated_data.get('first_name'):
           instance.name = validated_data.get('first_name')
        if validated_data.get('last_name'):
           instance.name = validated_data.get('last_name')
        if validated_data.get('type_card'):
            instance.type_card = validated_data.get('type_card')
        if validated_data.get('number_card'):
            if validated_data.get('number_card') == instance.number_card:
                instance.number_card = validated_data.get('number_card')
            elif CreditCard.objects.filter(number_card=validated_data.get('number_card')).exists():
                raise serializers.ValidationError({'message':[_('the number of credit card exists please try with another number')]})
            instance.number_card = validated_data.get('number_card')    
        if validated_data.get('cod_security'):
            instance.cod_security = validated_data.get('cod_security')
        if validated_data.get('date_expiration'):
            instance.date_expiration = validated_data.get('date_expiration')
        instance.save()
        return instance


class CreditCardCreateValidations(CreditCardValidations):

    def validate_number_card(self, number_card):
        if not re.match(r'^[-+]?[0-9]+$',number_card):
            raise serializers.ValidationError('the credit card can only have numbers')
        if CreditCard.objects.filter(number_card=number_card).exists():
            raise serializers.ValidationError('the number of credit card exists please try with another number')
        return number_card

    def validate_cod_security(self, cod_security):
        if not re.match(r'^[-+]?[0-9]+$',cod_security):
            raise serializers.ValidationError('the security code can only have numbers')
        return cod_security

