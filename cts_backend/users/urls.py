from django.urls import path
from django.http import JsonResponse
from . import views
from .views import RegisterView, VerifyEmailView, SetPasswordView
from .views import GenerateWinnerView
from .views import UserProfileView

urlpatterns = [
    path('', lambda request: JsonResponse({'message': 'Bienvenido a la API. Usa /register/, /login/, etc.'})),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('verify-email/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('set-password/', SetPasswordView.as_view(), name='set-password'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('admin/dashboard/', views.AdminDashboardView.as_view(), name='admin-dashboard'),
    path('generate-winner/', GenerateWinnerView.as_view(), name='generate-winner'),
    path('user-profile/', UserProfileView.as_view(), name='user-profile'),
    path('user-list/', views.UserListView.as_view(), name='user-list'),

]
