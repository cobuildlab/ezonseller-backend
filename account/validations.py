from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
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

