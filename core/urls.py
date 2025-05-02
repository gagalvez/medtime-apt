from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.base, name="base"),
    path("signup/", views.signup, name="signup" ),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='base'), name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path("cambiar-contraseña/", views.cambiar_contraseña, name="cambiar_contraseña"),
    path('enviar-correo/', views.enviar_correo, name='enviar_correo'),
    path('agendar-cita/', views.agendar_cita, name='agendar_cita'),
    path('cita-agendada/<int:cita_id>/', views.cita_agendada, name='cita_agendada'),
    path('reenviar-correo/', views.reenviar_correo, name='reenviar_correo'),
    path('cita_estado/', views.cita_estado, name='cita_estado'),
    path('doctores/', views.obtener_doctores, name='obtener_doctores'),
    path('eliminar_cita/<int:cita_id>/', views.eliminar_cita, name='eliminar_cita'),
    path('panel_doctor/', views.panel_doctor, name='panel_doctor'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
