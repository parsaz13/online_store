from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_order_confirmation_email(user_email, order_id):
    subject = "Order Confirmation"
    message = f"Your order #{order_id} has been placed successfully."
    send_mail(subject, message, "no-reply@onlinestore.com", [user_email])