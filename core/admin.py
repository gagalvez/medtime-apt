from django.contrib import admin
from .models import CustomUser, CitaMedica
from django.utils.translation import gettext_lazy as _

# Intentamos desregistrar CustomUser si ya está registrado
try:
    admin.site.unregister(CustomUser)
except admin.sites.NotRegistered:
    pass

# Registra el modelo CustomUser en el admin con una clase personalizada
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'nombre', 'apellido', 'email', 'rol', 'especialidad', 'especialidad_en_clave']
    search_fields = ['username', 'nombre', 'apellido', 'email']
    list_filter = ['rol', 'especialidad']

    # Método para mostrar el nombre en clave de la especialidad entre paréntesis
    def especialidad_en_clave(self, obj):
        if obj.rol == 'doctor' and obj.especialidad:
            return f"({obj.especialidad})"
        return ""
    especialidad_en_clave.short_description = 'Especialidad (Nombre en clave)'

admin.site.register(CustomUser, CustomUserAdmin)

# Filtro personalizado para tipo de cita
class TipoCitaFilter(admin.SimpleListFilter):
    title = _('Tipo de Cita')
    parameter_name = 'tipo_cita'

    def lookups(self, request, model_admin):
        return (
            ('paciente', _('Cita de paciente')),
            ('doctor', _('Cita de doctor')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'paciente':
            return queryset.filter(paciente__isnull=False)
        if self.value() == 'doctor':
            return queryset.filter(doctor__isnull=False)
        return queryset

# Clase base para CitaMedicaAdmin
class CitaMedicaAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'doctor_nombre_especialidad', 'get_especialidad_display', 'fecha', 'hora']
    search_fields = ['paciente__nombre', 'paciente__apellido', 'doctor__nombre', 'doctor__apellido', 'especialidad']
    list_filter = ['especialidad', 'fecha', 'hora', TipoCitaFilter]

    def doctor_nombre_especialidad(self, obj):
        if obj.doctor:
            return f"{obj.doctor.nombre} {obj.doctor.apellido} ({obj.doctor.especialidad})"
        return "Sin doctor"
    doctor_nombre_especialidad.short_description = 'Doctor (Especialidad)'

    def get_especialidad_display(self, obj):
        return obj.get_especialidad_display()

# Registra CitaMedica solo una vez, pero con el filtro adecuado para pacientes o doctores
admin.site.register(CitaMedica, CitaMedicaAdmin)
