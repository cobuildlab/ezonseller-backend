from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.hashers import make_password
from account import models as accounts_models
from notification import  models as notification_models
import re


class UserSerializers(serializers.ModelSerializer):
    username = serializers.CharField(required=True, min_length=6, max_length=12)
    email = serializers.CharField(required=False, max_length=50)
    first_name = serializers.CharField(min_length=3, max_length=30)
    last_name = serializers.CharField(min_length=3, max_length=30)
    password = serializers.CharField(default="", write_only=True, min_length=6, max_length=12)

    class Meta:
        model = accounts_models.User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'myPayPal', 'photo', 'type')
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'read_only': True}
        }

    def validate_username(self, username):
        if self.context["request"].method != 'PUT':
            if accounts_models.User.objects.filter(username__iexact=username).exists():
                raise serializers.ValidationError(_("El nombre de usuario ya fue registrado"))
        return username
    
    def create(self, validated_data):
        password = validated_data.get('password')
        validated_data['password'] = make_password(password)
        user = accounts_models.User(**validated_data)
        user.is_active = False
        user.save()
        return user

    def update(self, instance, validated_data):

        if validated_data.get('first_name'):
            instance.first_name = validated_data.get('first_name')
        if validated_data.get('last_name'):
            instance.last_name = validated_data.get('last_name')
        if validated_data.get('username'):
            if validated_data.get('username') == instance.username:
                instance.username = validated_data.get('username')    
            elif accounts_models.User.objects.filter(username__iexact=validated_data.get('username')).exists():
                raise serializers.ValidationError({'message': [_("El nombre de usuario ya fue registrado")]})
            instance.username = validated_data.get('username')
        if validated_data.get('myPayPal'):
            instance.myPayPal = validated_data.get('myPayPal')
        if 'photo' in validated_data.keys() and validated_data.get('photo'):
            instance.photo = validated_data.get('photo')
        instance.save()    
        return instance


class UserCreateSerializers(UserSerializers):

    def validate_password(self, password):
        if not re.match(r'(?=.*[A-Za-z]+)(?=.*\d+)', password):
            raise serializers.ValidationError(_(u"the password requires characters and number"))
        return password

    def validate_username(self, username):
        if accounts_models.User.objects.filter(username=username).exists():
            raise serializers.ValidationError(u"the username already exist, please try with another username")
        return username

    def validate_email(self, email):
        if not re.search('(\w+[.|\w])*@(\w+[.])*\w+', email):
            raise serializers.ValidationError(_(u"the email must be in the format name@email.com"))
        if accounts_models.User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(_(u"the email already exist, please try with another email"))
        return email




class UserRecoverPasswordSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,min_length=6, max_length=12)

    class Meta:
        model = accounts_models.User
        fields = ('password',)

    def validate_password(self, password):
        if not re.match(r'(?=.*[A-Za-z]+)(?=.*\d+)', password):
            raise serializers.ValidationError(_(u"the password requires characters and number"))
        return password

    def update(self, instance, validated_data):
        if validated_data.get('password'):
            instance.password = make_password(validated_data.get('password'))
            instance.recovery = ''
            instance.is_active = True
        instance.save()
        return instance


class UserChangePasswordSerializers(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=6, max_length=12)

    class Meta:
        model = accounts_models.User
        fields = ('old_password', 'new_password')

    def validate_old_password(self, old_password):
        # password=self.context['request'].user
        if not self.context['request'].user.check_password(old_password):
            raise serializers.ValidationError(_(u"the password does not match"))
        return old_password

    def validate_new_password(self, new_password):
        if not re.match(r'(?=.*[A-Za-z]+)(?=.*\d+)', new_password):
            raise serializers.ValidationError(_(u"the password requires characters and number"))
        return new_password

    def update(self, instance, validated_data):
        if validated_data.get('new_password'):
            instance.password = make_password(validated_data.get('new_password'))
        instance.save()
        return instance


class ContactSupportValidations(serializers.ModelSerializer):
    title = serializers.CharField(required=True, max_length=40)
    message = serializers.CharField(required=True, max_length=2000)
    email = serializers.CharField(required=True, max_length=50)

    class Meta:
        model = notification_models.ContactSupport
        fields = ('id', 'title', 'message', 'email',)

    def validate_email(self, email):
        if not re.search('(\w+[.|\w])*@(\w+[.])*\w+', email):
            raise serializers.ValidationError(_(u"the email must be in the format name@email.com"))
        return email

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        contact = notification_models.ContactSupport.objects.create(**validated_data)
        return contact