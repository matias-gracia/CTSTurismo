from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from .models import CustomUser
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from django.conf import settings
from .tasks import send_confirmation_email
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes
from .tokens import account_activation_token
from django.shortcuts import redirect
from random import choice
from django.core.mail import send_mail
from .serializers import CustomUserSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import ListAPIView
import random

serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

# Vista para registrar un nuevo usuario
class RegisterView(APIView):
    def post(self, request):
        data = request.data
        required_fields = ['username', 'email']
        for field in required_fields:
            if not data.get(field):
                return Response({'error': f'El campo {field} es obligatorio.'}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(email=data['email']).exists():
            return Response({'error': 'El correo electrónico ya está en uso.'}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create(
            username=data['username'],  # Ahora no único
            email=data['email'],
            is_active=False,  # Inactivo hasta verificar el correo
        )

        # Generación del token y UIDB64
        token = account_activation_token.make_token(user)
        print(f"Token generado: {token}")
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        confirmation_url = f"http://127.0.0.1:8080/create-password?uidb64={uidb64}&token={token}"

        # Agrega estos print para depuración
        print(f"Token generado: {token}")
        print(f"UIDB64 generado: {uidb64}")
        print(f"Enlace de confirmación: {confirmation_url}")

        # Envío del correo
        send_confirmation_email.delay(
            "Confirma tu correo electrónico",
            f"Por favor verifica tu correo haciendo clic en el enlace: {confirmation_url}",
            [data['email']],
        )

        return Response({'message': 'Correo de verificación enviado.'}, status=status.HTTP_201_CREATED)


# Vista para validar un correo electrónico
class VerifyEmailView(APIView):
    def get(self, request):
        uidb64 = request.query_params.get('uidb64')
        token = request.query_params.get('token')

        if not uidb64 or not token:
            return Response({'error': 'Faltan parámetros en la solicitud.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Decodificar el UID para obtener el usuario
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
            print(f"Usuario encontrado: {user.username}")

            # Validar el token
            if account_activation_token.check_token(user, token):
                print(f"Token válido. Activando usuario: {user.username}")
                
                # Activa automáticamente al usuario
                user.is_active = True
                user.save()

                # Redirige al formulario de creación de contraseña
                return redirect(f"http://127.0.0.1:8080/create-password?uidb64={uidb64}&token={token}")
            else:
                return Response({'error': 'Token inválido o expirado.'}, status=status.HTTP_400_BAD_REQUEST)

        except CustomUser.DoesNotExist:
            return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)



# Vista para establecer una nueva contraseña
class SetPasswordView(APIView):
    def post(self, request):
        uidb64 = request.data.get('uidb64')
        token = request.data.get('token')
        new_password = request.data.get('password')

        print(f"Token recibido: {token}")
        print(f"UIDB64 recibido: {uidb64}")

        if not uidb64 or not token or not new_password:
            return Response({'error': 'Todos los campos son obligatorios.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
            print(f"Usuario encontrado: {user.username}")

            # Depuración: compara el token generado con el recibido
            print(f"Token esperado: {account_activation_token.make_token(user)}")

            # Verifica el token
            if account_activation_token.check_token(user, token):
                print("Token válido")
                user.password = make_password(new_password)
                user.is_active = True  # Asegura que el usuario esté activado
                user.save()
                return Response({'message': 'Contraseña establecida exitosamente.'}, status=status.HTTP_200_OK)

            else:
                print("Token inválido")
                return Response({'error': 'Token inválido o expirado.'}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)




# Vista para iniciar sesión y generar un token
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')  # Cambiado a 'email' según tu configuración actual
        password = request.data.get('password')
        print(f"Intento de inicio de sesión: {email}, {password}")  # Depuración

        try:
            # Buscar el usuario por correo
            user = CustomUser.objects.get(email=email)
            print(f"Usuario encontrado: {user.username}")

            # Autenticar usando el nombre de usuario del usuario encontrado
            user = authenticate(request, username=email, password=password)

            if user is not None:
                print("Usuario autenticado correctamente")
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'message': 'Inicio de sesión exitoso.',
                    'is_staff': user.is_staff  # Devuelve si el usuario es administrador
                })
            else:
                print("Credenciales inválidas")
                return Response({'error': 'Credenciales inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)
        except CustomUser.DoesNotExist:
            print("Correo no registrado.")
            return Response({'error': 'Correo no registrado.'}, status=status.HTTP_404_NOT_FOUND)





# Vista protegida para el panel de administración
class AdminDashboardView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Acceso denegado. Usuario no autorizado.'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'message': 'Bienvenido al panel de administración.'})
    



class UserProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
        }, status=200)



class GenerateWinnerView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_staff:  # Verifica si el usuario es administrador
            return Response({'error': 'Permisos insuficientes.'}, status=status.HTTP_403_FORBIDDEN)

        # Selecciona un ganador al azar
        participants = CustomUser.objects.filter(is_active=True, is_staff=False)
        if not participants.exists():
            return Response({'error': 'No hay participantes registrados.'}, status=status.HTTP_400_BAD_REQUEST)

        winner = random.choice(participants)

        # Actualiza el estado del ganador
        winner.is_winner = True
        winner.is_active = False  # Opcional: Cambiar el estado de actividad
        winner.save()

        send_mail(
            '¡Felicitaciones!',
            f'¡Felicidades, {winner.username}! Has ganado el sorteo de San Valentín.',
            'noreply@hotel.com',
            [winner.email],
            fail_silently=False,
        )

        return Response({'winner': winner.username, 'winner_email': winner.email}, status=status.HTTP_200_OK)



class UserListView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


