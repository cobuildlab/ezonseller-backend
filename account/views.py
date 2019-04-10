from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.response import Response
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework import viewsets
from account import models as account_models
from notification import views as notify_views
from datetime import datetime
from datetime import timedelta
from account import validations
from account import serializers
from account import permissions as accounts_permissions
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.db.models import Q
from account.tokens import account_activation_token
from rest_framework.decorators import detail_route
from account.tasks import disable_code_recovery_password
import re
import base64
import requests
import json
from ezonseller import settings
from account.service import create_card, serialize_credit_card

class Login(APIView):
    """
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')

        if not username:
            return Response({'message': 'The username dont be empty'}, status=status.HTTP_400_BAD_REQUEST)

        if not password:
            return Response({'message': 'The password dont be empty'}, status=status.HTTP_400_BAD_REQUEST)

        # if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", username):
        try:
            user = account_models.User.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except account_models.User.DoesNotExist:
            return Response({'message': 'the user not exist'}, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_active:
            return Response({'message': 'Inactive user, confirm your account to gain access to the system'},
                            status=status.HTTP_401_UNAUTHORIZED)
        if not user.check_password(password):
            print(user.failedAttempts)
            user.failedAttempts = user.failedAttempts - 1
            user.save()
            if user.failedAttempts == 0:
                if notify_views.accountSecurityBlock(user):
                    print("email has been send")
                    user.failedAttempts = 5
                    user.is_active = False
                    user.save()
                    return Response({'message': 'Your account is blocked, check your email to unlock the account'},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'message': 'the email cant not send'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'Invalid password, please enter the correct password'},
                            status=status.HTTP_400_BAD_REQUEST)
        # else:
        #    user = authenticate(username=username, password=password)
        # if not user:
        #    try:
        #        user_find = account_models.User.objects.get(username=username)
        #    except account_models.User.DoesNotExist:
        #        return Response({'message': 'the user not exist'}, status=status.HTTP_400_BAD_REQUEST)
        #    if not user_find.is_active:
        #        return Response({'message': 'Inactive user, confirm your account to gain access to the system'},
        #                        status=status.HTTP_401_UNAUTHORIZED)
        #    else:
        #        band = False
        user.failedAttempts = 5
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'Token': token.key, 'id': user.id, 'type_plan': user.type_plan, 'last_login': user.last_login},
                        status=status.HTTP_200_OK)


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
                return Response({'message': 'The user not exist'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user = account_models.User.objects.get(username=user_logout)
            except account_models.User.DoesNotExist:
                return Response({'message': 'The user not exist'}, status=status.HTTP_400_BAD_REQUEST)
        user.last_login = datetime.now()
        user.save()
        user.auth_token.delete()
        return Response({'message': 'The user has disconnected from the system'}, status=status.HTTP_200_OK)


class RegisterView(APIView):
    """
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        user = request.data.get('user')
        if not user['callback']:
            return Response({"message": "reCAPTCHA field cant not be empty"}, status=status.HTTP_400_BAD_REQUEST)
        recaptcha_response = user['callback']
        r = requests.post(settings.RECAPTCHA_CAPTCHA_URL, {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        })

        if not json.loads(r.content.decode())['success']:
            return Response({'message': 'Invalid reCAPTCHA. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = validations.UserCreateSerializers(data=user)

        if user_serializer.is_valid() is False:
            errors_msg = []
            errors_keys = list(user_serializer.errors.keys())
            for i in errors_keys:
                errors_msg.append(str(i) + ": " + str(user_serializer.errors[i][0]))
            error_msg = "".join(errors_msg)
            return Response({'message': errors_msg[0]}, status=status.HTTP_400_BAD_REQUEST)

        user = user_serializer.save()

        serialize_card = serialize_credit_card(request,user)

        if 'message' in serialize_card:
            error_serialize_card = serialize_card['message']
            return Response({'message': error_serialize_card}, status=status.HTTP_400_BAD_REQUEST)

        created_card  = create_card(serialize_card,user)

        if 'message' in created_card:
            error_create_card = created_card['message']
            return Response({'message': error_create_card}, status=status.HTTP_400_BAD_REQUEST)


        if notify_views.activate_account(user, request):
            return Response({'username': user.username, 'message': 'The email has been send'},
                        status=status.HTTP_201_CREATED)
        else:
            user.delete()
            return Response({'message': 'The email cannot be sent and account not created'},
                            status=status.HTTP_400_BAD_REQUEST)


class RequestRecoverPassword(APIView):
    """
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'message': 'The email cant be empty'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = account_models.User.objects.get(email=email)
        except account_models.User.DoesNotExist:
            return Response({'message': 'The email not exist in database'}, status=status.HTTP_400_BAD_REQUEST)
        if notify_views.recover_password(user, request):
            expire = datetime.now() + timedelta(minutes=10)
            disable_code_recovery_password.apply_async(args=[user.id], eta=expire)
            return Response({'message': 'The email has been send'}, status=status.HTTP_200_OK)
        return Response({'message': 'The email cannot be sent'}, status=status.HTTP_400_BAD_REQUEST)


class RecoverPasswordView(APIView):
    """
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        code = request.data.get('code')
        password = request.data.get('password')
        if not code:
            return Response({'message': 'You need to send the code'}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({'message': 'You need to send the password'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = account_models.User.objects.get(recovery=str(code))
        except account_models.User.DoesNotExist:
            return Response({'message': 'Invalid code, please write the correct code'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = validations.UserRecoverPasswordSerializers(user, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'The password has been change successfully'}, status=status.HTTP_200_OK)


class ActivateAccountView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        uidb = data.get('uidb64')
        token = data.get('token')
        if not uidb:
            return Response({'message': 'The uidb is required, cant be empty'}, status=status.HTTP_400_BAD_REQUEST)
        if not token:
            return Response({'message': 'the token is required, cant be empty'}, status=status.HTTP_400_BAD_REQUEST)
        if not re.search("(b')", uidb):
            return Response({'message': 'the uidb64 is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        decode = uidb.strip("b")
        count = len(decode) - 1
        decode = decode[1:count]
        decode = str.encode(decode)
        uid = force_text(urlsafe_base64_decode(decode))
        try:
            user = account_models.User.objects.get(pk=uid)
        except account_models.User.DoesNotExist:
            return Response({'message': 'The user not exist'}, status=status.HTTP_400_BAD_REQUEST)
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Thank you for your email confirmation. Now you can login your account.'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Activation link is invalid!'}, status=status.HTTP_400_BAD_REQUEST)


class ContactSupportView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user_data = request.user
        serializer = validations.ContactSupportValidations(data=request.data, context={'request': request})
        # serializer.is_valid(raise_exception=True)
        if serializer.is_valid() is False:
            errors_msg = []
            errors_keys = list(serializer.errors.keys())
            for i in errors_keys:
                errors_msg.append(str(i) + ": " + str(serializer.errors[i][0]))
            error_msg = "".join(errors_msg)
            return Response({'message': errors_msg[0]}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        user = account_models.User.objects.get(username=user_data)
        if notify_views.support_notify(user, request):
            return Response({'message': 'Your message has been send successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'Your request cannot be sent'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = account_models.User.objects.all()
    serializer_class = serializers.ProfileUserSerializers
    permission_classes = (accounts_permissions.IsOwnerOrReadOnly, permissions.IsAuthenticated)
    http_method_names = ['get', 'put', 'delete', 'post']

    def list(self, request, *args, **kwargs):
        queryset = account_models.User.objects.get(username=request.user)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = validations.UserSerializers(instance, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response_data = serializer.data
        response_data['message'] = 'Your profile has been updated successfully'
        return Response(response_data, status=status.HTTP_200_OK)

    @detail_route(methods=['post'],
                  permission_classes=(permissions.IsAuthenticated, accounts_permissions.IsOwnerOrReadOnly))
    def uploadImage(self, request, pk=None):
        user = account_models.User.objects.get(username=request.user)
        if not request.data.get('photo'):
            return Response({'message': 'the image cant be empty'}, status=status.HTTP_400_BAD_REQUEST)
        user.photo = request.data.get('photo')
        user.save()
        image = open(settings.MEDIA_ROOT + '/' + str(user.photo), 'rb')  # open binary file in read mode
        image_read = image.read()
        # image_64_encode = base64.encodebytes(image_read)
        image_64_encode = base64.b64encode(image_read).decode('ascii')
        # image_64_encode = base64.b64encode(image_read)
        print(image_64_encode)
        user.photo64 = image_64_encode
        user.save()
        serializer_data = serializers.ProfileUserSerializers(user, many=False)
        serializer = serializer_data.data
        serializer['message'] = 'The profile image has been change successfully'
        return Response(serializer, status=status.HTTP_200_OK)

    @detail_route(methods=['put'],
                  permission_classes=(permissions.IsAuthenticated, accounts_permissions.IsOwnerOrReadOnly))
    def changePassword(self, request, pk=None):
        user = request.user
        serializer = validations.UserChangePasswordSerializers(user, data=request.data, context={'request': request})
        # serializer.is_valid(raise_exception=True)
        if serializer.is_valid() is False:
            errors_msg = []
            errors_keys = list(serializer.errors.keys())
            for i in errors_keys:
                errors_msg.append(str(i) + ": " + str(serializer.errors[i][0]))
            error_msg = "".join(errors_msg)
            return Response({'message': errors_msg[0][14:]}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        user.auth_token.delete()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'message': 'The password has been change successfully',
                         'token': token.key,
                         'id': request.user.id}, status=status.HTTP_200_OK)


class CertFileView(APIView):
    """
    View to provide cert validation
    """

    def get(self, request):
        return Response(render_to_string('cert'), status=status.HTTP_200_OK)
