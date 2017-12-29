from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.contrib.auth import authenticate
from account import models as account_models
from notification import views as notify_views
from datetime import datetime
from account import validations

#status-code-response
STATUS = {
    "200":status.HTTP_200_OK,
    "201":status.HTTP_201_CREATED,
    "202":status.HTTP_202_ACCEPTED,
    "204":status.HTTP_204_NO_CONTENT,
    "400":status.HTTP_400_BAD_REQUEST,
    "401":status.HTTP_401_UNAUTHORIZED,
    "404":status.HTTP_404_NOT_FOUND,
    "500":status.HTTP_500_INTERNAL_SERVER_ERROR
}


class Login(APIView):
    """
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')

        if not username:
            return Response({'message': 'the username dont be empty'}, status=STATUS['400'])

        if not password:
            return Response({'message': 'the password dont be empty'}, status=STATUS['400'])

        user = authenticate(username=username, password=password)
        if not user:
            return Response({'message': 'user or pass invalid'}, status=STATUS['400'])


        token, created = Token.objects.get_or_create(user=user)
        return Response({'Token': token.key, 'last_login': user.last_login})


class Logout(APIView):
    """
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, ):
        try:
            user = account_models.User.objects.get(username=request.data.get('username'))
        except account_models.User.DoesNotExist:
            return Response({'response': 'The user not exist'}, status=STATUS['400'])
        user.last_login = datetime.now()
        user.save()
        user.auth_token.delete()
        return Response({'message': 'The user has disconnected from the system'})


class RegisterView(APIView):
    """
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        user_serializer = validations.UserCreateSerializers(data=request.data)
        if user_serializer.is_valid() is False:
            errors_msg = []
            errors_keys = list(user_serializer.errors.keys())
            for i in errors_keys:
                errors_msg.append(str(i) + ": " + str(user_serializer.errors[i][0]))
            error_msg = "".join(errors_msg)
            return Response(errors_msg[0], status=status.HTTP_400_BAD_REQUEST)
        user = user_serializer.save()
        return Response({'username': user.username}, status=STATUS['201'])


class RecoverPasswordView(APIView):
    """
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'message': 'the email cant be empty'}, status=STATUS['400'])
        try:
            user = account_models.User.objects.get(email=email)
        except account_models.User.DoesNotExist:
            return Response({'message': 'the email not exit'}, status=STATUS['400'])

        if notify_views.recover_password(user):
            return Response({'message': 'the email has been send'})
        return Response({'message': 'the email cannot be sent'}, status=STATUS['500'])


class ChangePasswordView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request):
        user = request.user
        serializer = validations.UserChangePasswordSerializers(user, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user.auth_token.delete()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'message': 'the password has been change successfully', 'token': token.key})