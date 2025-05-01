from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CustomUserForm, LoginForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import requests
from .models import CitaMedica, CustomUser
from django.contrib.auth import authenticate, login

# Create your views here.

def base(request):
    return render(request, "base.html")

# Logica para el registro
def signup(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            rut = form.cleaned_data['rut']
            password = form.cleaned_data['password']
            usuario = form.save(commit=False)
            usuario.username = rut  # Asigna el RUT como username
            usuario.set_password(password)
            usuario.save()

            # Luego de registrar, logea al usuario
            user = authenticate(request, rut=rut, password=password)
            if user is not None:
                login(request, user)

            messages.success(request, "¡Te has registrado e iniciado sesión exitosamente!")
            return redirect('base')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = CustomUserForm()

    return render(request, 'signup.html', {'form': form})


# Logica para el login
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        # Valida CAPTCHA
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        captcha_verification = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = captcha_verification.json()

        if not result.get('success'):
            messages.error(request, "Por favor verifica que no eres un robot.")
            return render(request, 'login.html', {'form': form})

        if form.is_valid():
            rut = form.cleaned_data['rut']
            password = form.cleaned_data['password']

            user = authenticate(request, username=rut, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, "¡Has iniciado sesión correctamente!")

                # Verifica si el usuario es doctor y redirige a "Mis citas médicas"
                if user.is_doctor:
                    return redirect('panel_doctor')  # Redirige a la página de citas médicas para doctores
                else:
                    return redirect('base')  # Redirige a la página principal para pacientes
            else:
                messages.error(request, "RUT o contraseña incorrectos.")
                form.add_error(None, "RUT o contraseña incorrectos.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


# Logica para el perfil
@login_required(login_url='login')
def perfil(request):
    cita = None
    if request.user.is_authenticated:
        try:
            cita = CitaMedica.objects.filter(paciente=request.user).latest('fecha')
        except CitaMedica.DoesNotExist:
            pass

    return render(request, 'perfil.html', {'cita': cita})

# Logica para cambiar pw
@login_required
def cambiar_contraseña(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Tu contraseña ha sido cambiada con éxito.')
            return redirect('perfil')
        else:
            messages.error(request, 'Por favor corrige los errores.')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'cambiar_contraseña.html', {'form': form})

# Logica para enviar correo con cita agendada
def enviar_correo(cita):
    subject = "Confirmación de Cita Médica Agendada"
    message = f"Hola {cita.paciente.nombre},\n\nTu cita médica ha sido agendada con éxito.\n\n" \
              f"Especialidad: {cita.especialidad}\nFecha: {cita.fecha}\nHora: {cita.hora}\n\n" \
              "Gracias por confiar en nosotros.\nMedTime"
    
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [cita.paciente.email]

    # Intentar enviar el correo
    try:
        send_mail(subject, message, from_email, recipient_list)
        print("Correo enviado correctamente")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# Logica para reenviar correo de cita desde perfil
@login_required
def reenviar_correo(request):
    try:
        cita = CitaMedica.objects.filter(paciente=request.user).latest('fecha')
        enviar_correo(cita)
        messages.success(request, "El correo fue enviado nuevamente.")
    except CitaMedica.DoesNotExist:
        messages.error(request, "No se encontró una cita para enviar.")
    return redirect('perfil')

# Logica para agendar cita
@login_required
def agendar_cita(request):
    if request.method == "POST":
        especialidad = request.POST.get("especialidad")
        doctor_id = request.POST.get("doctor")  # El ID del doctor seleccionado
        fecha = request.POST.get("fecha")
        hora = request.POST.get("hora")

        # Obtener el doctor seleccionado
        doctor = get_object_or_404(CustomUser, id=doctor_id)

        # Guarda la cita en la base de datos
        cita = CitaMedica(
            paciente=request.user,
            especialidad=especialidad,
            doctor=doctor,  # Asigna el doctor seleccionado
            fecha=fecha,
            hora=hora
        )
        cita.save()
        # Despues de agendar, envia correo al paciente
        enviar_correo(cita)

        # Redirigir a la página de cita agendada, pasando el cita_id
        return redirect('cita_agendada', cita_id=cita.id)

    return render(request, "agendar_cita.html")


# Logica para mostrar la cita agendada
@login_required
def cita_agendada(request, cita_id):
    try:
        cita = CitaMedica.objects.get(id=cita_id)
    except CitaMedica.DoesNotExist:
        messages.error(request, "La cita no se encontró.")
        return redirect('perfil')
    return render(request, "cita_agendada.html", {'cita': cita})

# No es neceario el login para ver el estado de la cita
def cita_estado(request):
    form = CustomUserForm()
    citas = []

    if request.method == "POST":
        rut = request.POST.get('rut')
        paciente = get_object_or_404(get_user_model(), rut=rut)  # Busca el usuario por RUT
        # Filtra las citas médicas del paciente
        citas = CitaMedica.objects.filter(paciente=paciente)

    return render(request, "cita_estado.html", {"citas": citas, "form": form})

# Vista para mostrar las citas del doctor
@login_required
def panel_doctor(request):
    # Verifica si el usuario es un doctor
    if request.user.is_doctor:
        # Obtiene las citas agendadas para el doctor logueado
        citas = CitaMedica.objects.filter(doctor=request.user)

        return render(request, 'panel_doctor.html', {
            'user': request.user,
            'citas': citas,
        })
    else:
        return render(request, 'panel_doctor.html', {
            'error_message': 'Acceso no permitido. Solo los doctores pueden ver esta página.',
        })

def obtener_doctores(request):
    especialidad = request.GET.get('especialidad')
    doctores = CustomUser.objects.filter(rol='doctor', especialidad=especialidad).values('id', 'nombre')

    return JsonResponse(list(doctores), safe=False)

# Vista para eliminar una cita médica
def eliminar_cita(request, cita_id):
    try:
        cita = CitaMedica.objects.get(id=cita_id)
        cita.delete()  # Elimina la cita
        messages.success(request, 'Cita eliminada con éxito.')
    except CitaMedica.DoesNotExist:
        messages.error(request, 'La cita no existe.')
    
    return redirect('cita_estado')  # Redirige de vuelta a la vista de estado de la cita