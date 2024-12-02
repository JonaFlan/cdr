from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil
from .models import Sesion

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    imagen = forms.ChoiceField(
        label="Imagen de Perfil",
        choices=[],  # Se llenará dinámicamente
        widget=forms.Select(attrs={'class': 'form-select bg-dark text-light border-secondary'})
    )

    class Meta:
        model = Perfil
        fields = ['imagen']

class SesionForm(forms.ModelForm):
    class Meta:
        model = Sesion
        fields = ['juego', 'fecha', 'capacidad_maxima', 'usuarios_inscritos']
        widgets = {
            'juego': forms.Select(attrs={'class': 'form-control bg-dark text-light border-secondary'}),
            'fecha': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control bg-dark text-light border-secondary'
            }),
            'capacidad_maxima': forms.NumberInput(attrs={'class': 'form-control bg-dark text-light border-secondary'}),
            'usuarios_inscritos': forms.SelectMultiple(attrs={'class': 'form-control bg-dark text-light border-secondary'}),
        }