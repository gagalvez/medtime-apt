from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

# Modelo para el usuario
class CustomUser(AbstractUser):

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    rut = models.CharField(max_length=20, unique=True)

    USERNAME_FIELD = 'rut'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    

# Modelo para guarda las citas medicas
class CitaMedica(models.Model):
    ESPECIALIDADES = [
        ('medicina_general', 'Medicina General'),
        ('odontologia', 'Odontología'),
        ('pediatria', 'Pediatría'),
        ('dermatologia', 'Dermatología'),
        ('ginecologia', 'Ginecología'),
        ('psicologia', 'Psicología'),
    ]

    paciente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=50, choices=ESPECIALIDADES)
    fecha = models.DateField()
    hora = models.TimeField()

    def __str__(self):
        return f'{self.paciente.rut} - {self.especialidad} el {self.fecha} a las {self.hora}'