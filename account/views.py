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
            return Response({'message': 'The username dont be empty'}, status=STATUS['400'])

        if not password:
            return Response({'message': 'The password dont be empty'}, status=STATUS['400'])

        user = authenticate(username=username, password=password)
        if not user:
            user_find = account_models.User.objects.get(username=username)
            if not user_find.is_active:
                return Response({'message':'Inactive user, confirm your account to gain access to the system'}, status=STATUS['401'])
            return Response({'message': 'User or pass invalid'}, status=STATUS['400'])
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
        return Response({'username': user.username,}, status=STATUS['201'])


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
            return Response({'message': 'The email not exit'}, status=STATUS['400'])

        if notify_views.recover_password(user):
            return Response({'message': 'The email has been send'})
        return Response({'message': 'The email cannot be sent'}, status=STATUS['500'])
    
    
class RecoverPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        code = request.data.get('code')
        password = request.data.get('password')

        if not code:
            return Response({'message':'You need to send the code'}, status=STATUS['400'])
        
        if not password:
            return Response({'message':'You need to send the password'}, status=STATUS['400'])
        try:
            user = account_models.User.objects.get(recovery = str(code))
        except account_models.User.DoesNotExist:
            return Response({'message': 'Invalid code, please write the correct code'}, status=STATUS['400'])
        
        user.password= make_password(password)
        user.recovery=''
        user.save()
        return Response({'message':'The password has been change successfully'})


class ChangePasswordView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request):
        user = request.user
        serializer = validations.UserChangePasswordSerializers(user, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user.auth_token.delete()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'message': 'The password has been change successfully', 'token': token.key})

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
class example(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        user = account_models.User.objects.get(username='element')
        print(user.pk)
        data = {'current_site' : get_current_site(request),
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user)}
        print(data)
        print (type(data['uid']))
        return Response({})

class activate(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request,):
        uidb64 = self.request.GET.get('uidb64')
        token = self.request.GET.get('token')
        print(uidb64)
        print(token)
        print(type(uidb64), type(token))
        x = uidb64.strip("b")
        x = x[1:3]
        x = str.encode(x)
        print(x)
        uid = force_text(urlsafe_base64_decode(x))
        print(uid)
        print(type(int(uid)))
        user =account_models.User.objects.get(pk=uid)
        print(user)
        if user is not None and account_activation_token.check_token(user, token):
            print('entro')
            #user.is_active = True
            #user.save()
            #login(request, user)
            # return redirect('home')
            #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        #else:
            #return HttpResponse('Activation link is invalid!')
        #    print('no entro')
        return Response({})