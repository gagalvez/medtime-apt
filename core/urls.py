from django.urls import path
from . import views

urlpatterns = [
    path("", views.app, name="index"),
    path("registro/", views.registro, name="registro" ),
]
