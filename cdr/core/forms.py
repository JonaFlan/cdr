from django import forms
import os
from django.conf import settings
from .models import Perfil

class ProfileUpdateForm(forms.ModelForm):
    imagen = forms.ChoiceField(
        label="Imagen de Perfil",
        choices=[],  # Se llenará dinámicamente
        widget=forms.Select(attrs={'class': 'form-select bg-dark text-light border-secondary'})
    )

    class Meta:
        model = Perfil
        fields = ['imagen']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Obtener imágenes predefinidas desde un directorio estático
        imagenes_path = None
        for directory in settings.STATICFILES_DIRS:
            posible_path = os.path.join(directory, 'perfil_imagenes')
            if os.path.exists(posible_path):
                imagenes_path = posible_path
                break

        if imagenes_path:
            imagenes = [
                (f'perfil_imagenes/{nombre}', nombre) for nombre in os.listdir(imagenes_path) if nombre.endswith(('png', 'jpg', 'jpeg'))
            ]
            self.fields['imagen'].choices = imagenes
        else:
            self.fields['imagen'].choices = []
