from django.shortcuts import render
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from ezonseller.settings import EMAIL_HOST_USER
import string
import random


def pass_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def recover_password(user):
    try:
        new_password = pass_generator(8)
        to = user.email
        data = {"msg": 'Your new password', 'password': new_password, 'username': user.username}
        subject, from_email = data['msg'], EMAIL_HOST_USER
        text_content = render_to_string("email/recovery_password.html", data)
        html_content = render_to_string("email/recovery_password.html", data)
        send = EmailMultiAlternatives(subject, text_content, from_email, [to])
        send.attach_alternative(html_content, "text/html")
        send.send()
        user.set_password(new_password)
        user.save()
        return True
    except:
        return False
