from django.core.mail import send_mail

import uuid
from django.conf import settings

def send_forgot_password_mail(email,token):

    subject='Your Forgot Password Link'
    message=f'Click on the link'
    email_from=settings.EMAIL_HOST_USER
    recepient_list=[email]
    kindle=send_mail(subject,message,email_from, recepient_list)
    print(kindle)
    return True