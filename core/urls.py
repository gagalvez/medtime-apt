from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path("", views.base, name="base"),
    path("signup/", views.signup, name="signup" ),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='base'), name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path("cambiar-contraseña/", views.cambiar_contraseña, name="cambiar_contraseña"),
    path('enviar-correo/', views.enviar_correo, name='enviar_correo'),
    path('agendar-cita/', views.agendar_cita, name='agendar_cita'),
    path('cita-agendada/<int:cita_id>/', views.cita_agendada, name='cita_agendada'),
    path('reenviar-correo/', views.reenviar_correo, name='reenviar_correo'),
]
