from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    rut = models.CharField(max_length=20, unique=True)

    USERNAME_FIELD = 'rut'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"