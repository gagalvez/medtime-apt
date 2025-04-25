from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path("", views.base, name="base"),
    path("registro/", views.registro, name="registro" ),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='base'), name='logout'),
    path('perfil/', views.perfil, name='perfil'),
]
