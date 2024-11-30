import os
import django
from django.core.mail import send_mail

# Configuración del entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cts_backend.settings")
django.setup()

# Enviar correo de prueba
send_mail(
    subject="Correo de prueba",
    message="Este es un mensaje enviado desde Django.",
    from_email="matiasgraciadelpino@gmail.com",  # Cambia esto por tu correo configurado
    recipient_list=["matias_gracia@hotmail.com"],
    fail_silently=False,
)
print("Correo enviado correctamente.")

