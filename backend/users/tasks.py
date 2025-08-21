from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_login_otp_email(to_email: str, otp: int):
    subject = "Your login code"
    message = f"Your one-time login code is: {otp}\nThis code expires in 5 minutes."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [to_email], fail_silently=False)