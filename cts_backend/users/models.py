from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Campos adicionales
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)

    # Campo para marcar al ganador
    is_winner = models.BooleanField(default=False)

    # Campo de nombre de usuario no único
    username = models.CharField(max_length=150, blank=True, null=True)

    # Define el campo único para la autenticación
    USERNAME_FIELD = 'email'  # Autenticación basada en correo electrónico
    REQUIRED_FIELDS = ['username']  # Campos requeridos al crear un superusuario

    def __str__(self):
        return self.email  # Representa al usuario por su correo electrónico

