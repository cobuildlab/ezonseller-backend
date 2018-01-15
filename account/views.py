from django.shortcuts import render
from django.contrib.auth.hashers import make_password
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
from notification import  models as notification_models
from notification import views as notify_views
from datetime import datetime
from account import validations
from account import serializers
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from account.tokens import account_activation_token
from rest_framework.decorators import detail_route, list_route
import re
#status-code-response
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


class Login(APIView):
    """
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        band = True
        data = request.data
        username = data.get('username')
        password = data.get('password')

        if not username:
            return Response({'message': 'The username dont be empty'}, status=STATUS['400'])

        if not password:
            return Response({'message': 'The password dont be empty'}, status=STATUS['400'])
        
        if re.search('(\w+[.|\w])*@(\w+[.])*\w+', username):
            try:
                user = account_models.User.objects.get(email=username)
            except account_models.User.DoesNotExist:
                return Response({'message': 'the user not exist'}, status=STATUS['400'])
            if not user.check_password(password):
                band = False
        else:
            user = authenticate(username=username, password=password)
        if not user:
            try:
                user_find = account_models.User.objects.get(username=username)
            except account_models.User.DoesNotExist:
                return Response({'message': 'the user not exist'}, status=STATUS['400'])
            if not user_find.is_active:
                return Response({'message': 'Inactive user, confirm your account to gain access to the system'}, status=STATUS['401'])
            else:
                band = False
        if not band:
            return Response({'message': 'User or pass invalid'}, status=STATUS['400'])
        token, created = Token.objects.get_or_create(user=user)
        return Response({'Token': token.key, 'id': user.id, 'last_login': user.last_login})
        

class Logout(APIView):
    """
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, ):
        user_logout = request.data.get('username')
        if re.search('(\w+[.|\w])*@(\w+[.])*\w+', user_logout):
            try:
                user = account_models.User.objects.get(email=user_logout)
            except account_models.User.DoesNotExist:
                return Response({'message': 'The user not exist'}, status=STATUS['400'])
        else:
            try:
                user = account_models.User.objects.get(username=user_logout)
            except account_models.User.DoesNotExist:
                return Response({'message': 'The user not exist'}, status=STATUS['400'])
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
            return Response({'message': errors_msg[0]}, status=STATUS['400'])
        user = user_serializer.save()
        if notify_views.activate_account(user, request):
            return Response({'username': user.username, 'message': 'The email has been send'}, status=STATUS['201'])
        else:
            user.delete()
            return Response({'message': 'The email cannot be sent and account not created'}, status=STATUS['500'])


class RequestRecoverPassword(APIView):
    """
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'message': 'The email cant be empty'}, status=STATUS['400'])
        try:
            user = account_models.User.objects.get(email=email)
        except account_models.User.DoesNotExist:
            return Response({'message': 'The email not exist in database'}, status=STATUS['400'])

        if notify_views.recover_password(user, request):
            return Response({'message': 'The email has been send'})
        return Response({'message': 'The email cannot be sent'}, status=STATUS['500'])
    
    
class RecoverPasswordView(APIView):
    """
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):

        code = request.data.get('code')
        password = request.data.get('password')

        if not code:
            return Response({'message': 'You need to send the code'}, status=STATUS['400'])
        
        if not password:
            return Response({'message': 'You need to send the password'}, status=STATUS['400'])
        try:
            user = account_models.User.objects.get(recovery = str(code))
        except account_models.User.DoesNotExist:
            return Response({'message': 'Invalid code, please write the correct code'}, status=STATUS['400'])

        serializer = validations.UserRecoverPasswordSerializers(user, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'The password has been change successfully'})


class ActivateAccountView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):

        uidb = self.request.GET.get('uidb64')
        token = self.request.GET.get('token')
        if not uidb:
            return Response({'message': 'The uidb is required, cant be empty'}, status=STATUS['400'])
        if not token:
            return Response({'message': 'the token is required, cant be empty'}, status=STATUS['400'])
        decode = uidb.strip("b")
        count = len(decode)-1
        decode = decode[1:count]
        decode = str.encode(decode)
        uid = force_text(urlsafe_base64_decode(decode))
        try:
            user = account_models.User.objects.get(pk=uid)
        except account_models.User.DoesNotExist:
            return Response({'message': 'The user not exist'}, status=STATUS['400'])
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Thank you for your email confirmation. Now you can login your account.'})
        else:
            return Response({'message': 'Activation link is invalid!'}, status=STATUS['400'])


class ContacSupportView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user_data = request.user
        serializer = validations.ContactSupportValidations(data=request.data,
                                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = account_models.User.objects.get(username=user_data)
        if notify_views.support_notify(user, request):
            return Response({'message': 'Your message has been send successfully'})
        return Response({'message': 'Your request cannot be sent'}, status=STATUS['500'])


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = account_models.User.objects.all()
    serializer_class = serializers.ProfileUserSerializers
    http_method_names = ['get', 'put', 'delete', 'post']

    def list(self, request, *args, **kwargs):
        queryset = account_models.User.objects.get(username=request.user)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = validations.UserSerializers(instance, data=request.data, 
        context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response_data = serializer.data
        response_data['message'] = 'Your profile has been updated successfully'
        return Response(response_data)
    
    @detail_route(methods=['put'], permission_classes=(permissions.IsAuthenticated,))
    def changePassword(self, request, pk=None):
        user = request.user
        serializer = validations.UserChangePasswordSerializers(user, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user.auth_token.delete()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'message': 'The password has been change successfully',
                         'token': token.key,
                         'id': request.user.id})