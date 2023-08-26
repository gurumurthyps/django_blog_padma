from django.core.mail import send_mail

import uuid
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.html import strip_tags


import socket

def send_forgot_password_mail(email,token,protocol,socket,port):


    # try:
    #     HOSTNAME = socket.gethostname()
    # except:
    #     HOSTNAME = 'localhost'
    url=f'{protocol}://{socket}:{port}/change_password/{token}/'
    subject='Your Forgot Password Link'
    message_html = render_to_string('change_password_template.html', {'url': url})

    # Create a plain text version of the email (optional)
    message_text = strip_tags(message_html)
    email_from=settings.EMAIL_HOST_USER
    recepient_list=[email]
    kindle=send_mail(subject,message_text,email_from, recepient_list,html_message=message_html)
    print(kindle)
    return True