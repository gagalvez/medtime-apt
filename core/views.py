from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserForm, LoginForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.

def base(request):
    return render(request, "base.html")

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            rut = form.cleaned_data['rut']
            password = form.cleaned_data['password']
            
            # Autentificar al usuario
            user = authenticate(request, username=rut, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, "¡Has iniciado sesión correctamente!")
                print("Mensaje de éxito")
                return redirect('base')
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
                print("Mensaje de error")
                form.add_error(None, "Usuario o contraseña incorrectos.")
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

