from django import forms
from .models import CustomUser
from django.contrib.auth import authenticate
import re

class CustomUserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=5,
        required=True,
        label="Contraseña"
    )

    class Meta:
        model = CustomUser
        fields = ['rut', 'nombre', 'apellido', 'email', 'password']

    # Validación para el RUT
    def clean_rut(self):
        rut = self.cleaned_data.get('rut')

        # Eliminar puntos y guion para el RUT
        rut_normalizado = rut.replace('.', '').replace('-', '')

        # Validar el formato (sin puntos ni guion)
        pattern = r'^\d{7,8}[0-9kK]$'  # 7 u 8 dígitos + dígito verificador
        if not re.match(pattern, rut_normalizado):
            raise forms.ValidationError('El RUT debe tener 7 u 8 dígitos seguidos por un dígito verificador.')

        if CustomUser.objects.filter(rut=rut_normalizado).exists():
            raise forms.ValidationError('El RUT ya está registrado.')

        # Aplica formato 00.000.000-0
        cuerpo = rut_normalizado[:-1]
        dv = rut_normalizado[-1]

        # Aplica formato dependiendo de si tiene 7 u 8 dígitos en el cuerpo
        if len(cuerpo) == 7:
            rut_formateado = f"{cuerpo[:1]}.{cuerpo[1:4]}.{cuerpo[4:7]}-{dv.upper()}"
        else:
            rut_formateado = f"{cuerpo[:2]}.{cuerpo[2:5]}.{cuerpo[5:8]}-{dv.upper()}"

        return rut_formateado

    # Capitaliza la primera letra del nombre
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        return nombre.capitalize()

    # Capitaliza la primera letra del apellido
    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido')
        return apellido.capitalize()

    # Validación para la contraseña, mínimo 5 caracteres
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 5:
            raise forms.ValidationError('La contraseña debe tener al menos 5 caracteres.')
        return password

    # Validación para el email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email


class LoginForm(forms.Form):
    rut = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'placeholder': 'RUT'}))
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Contraseña')

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        return rut

    def clean(self):
        cleaned_data = super().clean()
        rut = cleaned_data.get('rut')
        password = cleaned_data.get('password')

        # Intentar autenticar al usuario
        user = authenticate(username=rut, password=password)
        if user is None:
            raise forms.ValidationError("Usuario o contraseña incorrectos.")
        return cleaned_data