from django.contrib import admin
from .models import Juego, Perfil, Sesion, Noticia, Manual
# Register your models here.

admin.site.register(Juego)
admin.site.register(Perfil)
admin.site.register(Sesion)
admin.site.register(Noticia)
admin.site.register(Manual)