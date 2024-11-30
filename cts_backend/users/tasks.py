from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_confirmation_email(subject, message, recipient_list):
    if not subject or not message or not recipient_list:
        raise ValueError("Todos los parámetros (subject, message, recipient_list) son obligatorios")
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=False,
    )
    return f"Correo enviado a {recipient_list}"

