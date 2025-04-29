from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

# Modelo para el usuario
class CustomUser(AbstractUser):
    ROLES = (
        ('doctor', 'Doctor'),
        ('paciente', 'Paciente'),
    )

    ESPECIALIDADES = [
        ('medicina_general', 'Medicina General'),
        ('odontologia', 'Odontología'),
        ('pediatria', 'Pediatría'),
        ('dermatologia', 'Dermatología'),
        ('ginecologia', 'Ginecología'),
        ('psicologia', 'Psicología'),
    ]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    rut = models.CharField(max_length=20, unique=True)
    rol = models.CharField(max_length=10, choices=ROLES, default='paciente')
    especialidad = models.CharField(max_length=100, choices=ESPECIALIDADES, null=True, blank=True)

    USERNAME_FIELD = 'rut'

    def str(self):
        return f"{self.nombre} {self.apellido} ({self.especialidad if self.rol == 'doctor' else 'Paciente'})"

class Especialidad(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def str(self):
        return self.nombre
    

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

    paciente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='citas_paciente')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='citas_doctor', null=True, blank=True)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()

    def str(self):
        return f'{self.paciente.rut} con {self.doctor.rut} - {self.especialidad.nombre} el {self.fecha} a las {self.hora}'