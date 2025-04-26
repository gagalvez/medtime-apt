from django import forms
from .models import CustomUser
from django.contrib.auth import authenticate

class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['rut', 'nombre', 'apellido', 'email', 'password']


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