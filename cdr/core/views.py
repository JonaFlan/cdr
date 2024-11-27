from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Sesion, Juego, Noticia
# Create your views here.
def hojapj(request):
    return render(request, 'core/hojapj.html')

def manuales(request):
    return render(request, 'core/manuales.html')

def mapas(request):
    return render(request, 'core/mapas.html')

def dado(request):
    return render(request, 'core/dado.html')  # Ajuste para la ruta dentro de 'templates/core'


def index(request):
    print("Inicio")
    return render(request, 'core/index.html')

def biblioteca(request):
    print("Lista de juegos")
    juegos = Juego.objects.all()
    return render(request, 'core/biblioteca.html', {'juegos': juegos})

def herramientas(request):
    return render(request, 'core/herramientas.html')

@login_required
def perfil(request):
    return render(request, 'core/perfil.html', {'user': request.user})

@login_required
def sesiones(request):
    sesiones = Sesion.objects.all()
    return render(request, 'core/sesiones.html', {'sesiones': sesiones})

@login_required
def anular_inscripcion_sesion(request, sesion_id):
    sesion = get_object_or_404(Sesion, id=sesion_id)
    if request.user in sesion.usuarios_inscritos.all():
        sesion.usuarios_inscritos.remove(request.user)
        messages.success(request, 'Tu inscripción ha sido anulada.')
    else:
        messages.info(request, 'No estás inscrito en esta sesión.')
    return redirect('sesiones')

@login_required
def inscribirse_sesion(request, sesion_id):
    sesion = get_object_or_404(Sesion, id=sesion_id)
    if sesion.usuarios_inscritos.filter(id=request.user.id).exists():
        messages.warning(request, 'Ya estás inscrito en esta sesión.')
    elif sesion.cupos_disponibles() > 0:
        sesion.usuarios_inscritos.add(request.user)
        messages.success(request, 'Te has inscrito correctamente en la sesión.')
    else:
        messages.error(request, 'No hay cupos disponibles para esta sesión.')
    return redirect('sesiones')

def noticias(request):
    noticias = Noticia.objects.order_by('-fecha_publicacion')
    return render(request, 'core/noticias.html', {'noticias': noticias})