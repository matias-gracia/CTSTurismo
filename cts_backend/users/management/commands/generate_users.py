from django.core.management.base import BaseCommand
from users.models import CustomUser
from django.utils.crypto import get_random_string

class Command(BaseCommand):
    help = 'Genera usuarios registrados y simula la confirmación del correo'

    def handle(self, *args, **kwargs):
        # Genera 200 usuarios
        for i in range(200):
            username = f'user{i+1}'
            email = f'user{i+1}@example.com'
            password = 'password123'

            if not CustomUser.objects.filter(email=email).exists():
                user = CustomUser.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    is_active=True  # Simula la confirmación del correo
                )
                self.stdout.write(self.style.SUCCESS(f'Usuario creado: {email}'))
            else:
                self.stdout.write(self.style.WARNING(f'El usuario ya existe: {email}'))
