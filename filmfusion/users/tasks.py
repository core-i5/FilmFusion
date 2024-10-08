from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_otp_email(email, otp):
    subject = 'Your OTP Code'
    message = f'Your OTP code is {otp}. It will expire in 2 minutes.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
