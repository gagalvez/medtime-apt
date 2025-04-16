from django.urls import path, include
from . import views
from .views import authView

urlpatterns = [
    path("", views.app, name="index"),
    path("registro/", views.registro, name="registro" ),
    path("accounts/", include("django.contrib.auth.urls")),
    path("signup/", authView, name="authView"),
]
