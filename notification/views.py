from django.shortcuts import render
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from ezonseller.settings import EMAIL_HOST_USER
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from account.tokens import account_activation_token
import string
import random


def pass_generator(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def recover_password(user, request):
    try:
        current_site = get_current_site(request)
        new_code = pass_generator(20)
        to = user.email
        data = {
            "msg": 'Your new password', 
            'code': new_code,
            'username': user.username,
            "domain": 'ezonseller.herokuapp.com',
        }
        subject, from_email = data['msg'], EMAIL_HOST_USER
        text_content = render_to_string("email/recovery_password.html", data)
        html_content = render_to_string("email/recovery_password.html", data)
        send = EmailMultiAlternatives(subject, text_content, from_email, [to],
                                      headers={'From': 'Ezonseller <'+from_email+'>',
                                      'Reply-to': 'Ezonseller <'+from_email+'>'})
        send.attach_alternative(html_content, "text/html")
        send.send()
        user.recovery = new_code
        user.save()
        return True
    except:
        return False


def activate_account(user, request):
    try:
        current_site = get_current_site(request)
        to = user.email
        data = {'domain': 'ezonseller.herokuapp.com',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'username': user.username,
                'msg': 'Account verification'
                }
        subject, from_email = data['msg'], EMAIL_HOST_USER
        text_content = render_to_string("email/user_verification.html", data)
        html_content = render_to_string("email/user_verification.html", data)
        send = EmailMultiAlternatives(subject, text_content, from_email, [to],
                                    headers={'From': 'Ezonseller <'+from_email+'>',
                                    'Reply-to': 'Ezonseller <'+from_email+'>'})
        send.attach_alternative(html_content, "text/html")
        send.send()
        return True
    except:
        return False


def support_notify(user, request):
    try:
        current_site = get_current_site(request)
        to = user.email
        data = {
            'domain': current_site.domain,
            "msg": 'Your new password',
            'username': user.username,
        }
        subject, from_email = data['msg'], EMAIL_HOST_USER
        text_content = render_to_string("email/contact_support.html", data)
        html_content = render_to_string("email/contact_support.html", data)
        send = EmailMultiAlternatives(subject, text_content, from_email, [to],
                                headers={'From': 'Ezonseller <'+from_email+'>',
                                'Reply-to': 'Ezonseller <'+from_email+'>'})
        send.attach_alternative(html_content, "text/html")
        send.send()
        return True
    except:
        return False