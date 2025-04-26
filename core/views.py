from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserForm, LoginForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
import requests


# Create your views here.

def base(request):
    return render(request, "base.html")

def login(request):
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
                return redirect('base')
            else:
                messages.error(request, "RUT o contraseña incorrectos.")
                form.add_error(None, "RUT o contraseña incorrectos.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def registro(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            # Guarda el usuario en la base de datos
            rut = form.cleaned_data['rut']
            usuario = form.save(commit=False)
            usuario.username = rut  # Asigna el RUT como username en la tabla default de django
            usuario.set_password(form.cleaned_data['password'])  # Encripta la contraseña
            usuario.save()

            messages.success(request, "¡Te has registrado exitosamente!")
            return redirect('index')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = CustomUserForm()

    return render(request, 'registro.html', {'form': form})

@login_required(login_url='login')
def perfil(request):
    return render(request, 'perfil.html')

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


def enviar_correo(request):
    # Acá podemos definir el asunto, mensaje y destinatario del correo
    subject = "Correo desde Django"
    message = "Este es un correo de prueba enviado desde tu aplicación Django."
    from_email = settings.DEFAULT_FROM_EMAIL  # Puede ser el mismo que EMAIL_HOST_USER
    recipient_list = ['ga.galvez.v@gmail.com']  # Cambia al destinatario real

    # Enviar el correo
    send_mail(subject, message, from_email, recipient_list)

    return HttpResponse("Correo enviado exitosamente.")
