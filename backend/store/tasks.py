from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_order_confirmation_email(order_id, user_email):
    subject = 'Order Confirmation'
    message = f'Your order #{order_id} has been placed successfully.'
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )
    return f"Email sent to {user_email} for order {order_id}"