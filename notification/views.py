from django.shortcuts import render
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string

# Create your views here.

def recoverpassword(user):
    try:
        to = user.email
        data = {"msg": 'your new password is'}
        subject, from_email = msg, settings.EMAIL_HOST_USER
        text_content = render_to_string("email/notify.html", data)
        html_content = render_to_string("email/notify.html", data)
        send = EmailMultiAlternatives(subject, text_content, from_email, [to])
        send.attach_alternative(html_content, "text/html")
        send.send()
    except:
        pass