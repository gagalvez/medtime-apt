from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Modelo personalizado de usuario
class CustomUser(AbstractUser):
    ROLES = (
        ('doctor', 'Doctor'),
        ('paciente', 'Paciente'),
    )

    ESPECIALIDADES = [
        ('Medico General', 'Medicina General'),
        ('Odontologo', 'Odontología'),
        ('Pediatra', 'Pediatría'),
        ('Dermatologo', 'Dermatología'),
        ('Ginecologo', 'Ginecología'),
        ('Psicologo', 'Psicología'),
    ]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    rut = models.CharField(max_length=20, unique=True)
    rol = models.CharField(max_length=10, choices=ROLES, default='paciente')
    especialidad = models.CharField(max_length=100, choices=ESPECIALIDADES, null=True, blank=True)
    imagen = models.ImageField(upload_to='doctores/', null=True, blank=True)

    USERNAME_FIELD = 'rut'

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.get_especialidad_display() if self.rol == 'doctor' else 'Paciente'})"

    @property
    def is_doctor(self):
        return self.rol == 'doctor'

    @property
    def is_paciente(self):
        return self.rol == 'paciente'


# Modelo para las citas médicas
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
    especialidad = models.CharField(max_length=100, choices=ESPECIALIDADES)
    fecha = models.DateField()
    hora = models.TimeField()

    def __str__(self):
        return f'{self.paciente.rut} con {self.doctor.rut if self.doctor else "Sin doctor"} - {self.get_especialidad_display()} el {self.fecha} a las {self.hora}'
