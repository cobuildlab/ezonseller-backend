from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.hashers import make_password
from account import models as accounts_models
import re


class UserSerializers(serializers.ModelSerializer):
    username = serializers.CharField(required=True, min_length=6, max_length=12)
    email = serializers.CharField(required=True, max_length=50)
    first_name = serializers.CharField(min_length=3, max_length=30)
    last_name = serializers.CharField(min_length=3, max_length=30)
    password = serializers.CharField(required=True, write_only=True, min_length=6, max_length=12)
    photo = serializers.SerializerMethodField('get_photo_url')

    class Meta:
        model = accounts_models.User
        fields = '__all__'

    def get_photo_url(self, medal):
        request = self.context.get('request')
        photo = medal.photo.url
        return request.build_absolute_uri(photo)

    def create(self, validated_data):
        user = accounts_models.User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        return user


class UserCreateSerializers(UserSerializers):

    def validate_username(self, username):
        if accounts_models.User.objects.filter(username=username).exists():
            raise serializers.ValidationError(u"the username already exist, please try with another username")
        return username

    def validate_password(self, password):
        if not re.match(r'(?=.*[A-Za-z]+)(?=.*\d+)', password):
            raise serializers.ValidationError(_(u"the password requires characters and number"))
        return password

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