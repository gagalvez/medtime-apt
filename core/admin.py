from django.contrib import admin
from .models import CustomUser, Especialidad

# Register your models here.
try:
    admin.site.unregister(CustomUser)
except admin.sites.NotRegistered:
    pass

# Registra el modelo CustomUser
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'nombre', 'apellido', 'email', 'rol', 'especialidad']
    search_fields = ['username', 'nombre', 'apellido', 'email']
    list_filter = ['rol', 'especialidad']

admin.site.register(CustomUser, CustomUserAdmin)

# Registra el modelo Especialidad
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

admin.site.register(Especialidad, EspecialidadAdmin)