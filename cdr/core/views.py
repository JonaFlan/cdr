from datetime import timedelta, date
from django.utils.timezone import now
import calendar
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Sesion, Juego, Noticia, Prestamo
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

# Create your views here.
def hojapj(request):
    return render(request, 'core/dnd-char-generator-master/index.html')

def manuales(request):
    return render(request, 'core/manuales.html')

def ver_manual_juego(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)
    return render(request, 'core/manual.html', {'juego': juego})


def mapas(request):
    return render(request, 'core/mapas.html')

def dado(request):
    return render(request, 'core/dado.html')  # Ajuste para la ruta dentro de 'templates/core'

def index(request):
    print("Inicio")
    return render(request, 'core/index.html')


def herramientas(request):
    return render(request, 'core/herramientas.html')

@login_required
def perfil(request):
    return render(request, 'core/perfil.html', {'user': request.user})

#JUEGOS
def biblioteca(request):
    juegos = Juego.objects.all()
    return render(request, 'core/biblioteca.html', {'juegos': juegos})

class JuegoDetailView(DetailView):
    model = Juego
    template_name = 'core/juego_detail.html'
    context_object_name = 'juego'

class JuegoCreateView(CreateView):
    model = Juego
    fields = ['nombre', 'proveedor', 'estado', 'imagen', 'descripcion', 'video']
    template_name = 'core/juego_form.html'
    success_url = reverse_lazy('biblioteca')

class JuegoUpdateView(UpdateView):
    model = Juego
    fields = ['nombre', 'proveedor', 'estado', 'imagen', 'descripcion', 'video']
    template_name = 'core/juego_form.html'
    success_url = reverse_lazy('biblioteca')

class JuegoDeleteView(DeleteView):
    model = Juego
    template_name = 'juegos/juego_confirm_delete.html'
    success_url = reverse_lazy('biblioteca')



# SESIONES
@login_required
def sesiones(request):
    sesiones = Sesion.objects.all()
    return render(request, 'core/sesiones.html', {'sesiones': sesiones})

class SesionCreateView(CreateView):
    model = Sesion
    fields = ['juego', 'fecha', 'capacidad_maxima', 'usuarios_inscritos']
    template_name = 'core/sesion_form.html'
    success_url = reverse_lazy('sesiones')

class SesionUpdateView(UpdateView):
    model = Sesion
    fields = ['juego', 'fecha', 'capacidad_maxima', 'usuarios_inscritos']
    template_name = 'core/sesion_form.html'
    success_url = reverse_lazy('sesiones')

class SesionDeleteView(DeleteView):
    model = Sesion
    template_name = 'core/sesion_confirm_delete.html'
    success_url = reverse_lazy('sesiones')

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

#NOTICIAS
def noticias(request):
    noticias = Noticia.objects.order_by('-fecha_publicacion')
    return render(request, 'core/noticias.html', {'noticias': noticias})

class NoticiaDetailView(DetailView):
    model = Noticia
    template_name = 'core/noticia_detail.html'
    context_object_name = 'noticia'

class NoticiaCreateView(CreateView):
    model = Noticia
    fields = ['titulo', 'contenido']
    template_name = 'core/noticia_form.html'
    success_url = reverse_lazy('noticias')

class NoticiaUpdateView(UpdateView):
    model = Noticia
    fields = ['titulo', 'contenido']
    template_name = 'core/noticia_form.html'
    success_url = reverse_lazy('noticias')

class NoticiaDeleteView(DeleteView):
    model = Noticia
    template_name = 'core/noticia_confirm_delete.html'
    success_url = reverse_lazy('noticias')

@login_required
def confirmar_reserva(request, pk):
    juego = get_object_or_404(Juego, pk=pk)

    if juego.estado != 'DISPONIBLE':
        messages.error(request, 'Este juego no está disponible para préstamo.')
        return redirect('biblioteca')
    
    # Verificar si el usuario ya tiene 2 préstamos activos
    prestamos_activos = Prestamo.objects.filter(usuario=request.user).filter(estado__in=['RESERVADO', 'PRESTADO'])
    if prestamos_activos.count() >= 2:
        messages.error(request, "No puedes tener más de 2 préstamos activos al mismo tiempo.")
        return redirect('biblioteca')  # Redirigir a la página de la biblioteca o donde sea apropiado
    
    # Calcular la fecha máxima de devolución (3 días hábiles)
    fecha_hoy = now().date()
    
    # Caso especial: Si la reserva se hace miércoles o jueves, la fecha máxima será el viernes de esa misma semana
    if fecha_hoy.weekday() == 2 or fecha_hoy.weekday() == 3:  # 2 = Miércoles, 3 = Jueves
        fecha_maxima = fecha_hoy + timedelta(days=(4 - fecha_hoy.weekday()))  # Salta al viernes de la misma semana
    else:
        # Caso general: Si no es miércoles ni jueves, sumamos 3 días a la fecha actual
        fecha_maxima = fecha_hoy + timedelta(days=3)

    if request.method == 'POST':
        # Crear el préstamo
        prestamo = Prestamo.objects.create(
            usuario=request.user,
            juego=juego,
            fecha_maxima_devolucion=fecha_maxima
        )
        juego.estado = 'RESERVADO'
        juego.save()
        print(prestamo.fecha_solicitud)
        prestamo.save()
        messages.success(request, 'Has aceptado los términos. El juego está reservado.')
        return redirect('biblioteca')

    return render(request, 'core/confirmar_reserva.html', {
        'juego': juego,
        'fecha_devolucion': fecha_maxima,
        'horario_maximo': '16:00',
        'ubicacion': 'DAE de la sede Inacap'
    })


def confirmar_devolucion(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, pk=prestamo_id)

    if prestamo.estado != 'PRESTADO':
        messages.error(request, 'El préstamo no está activo.')
        return redirect('prestamos')

    fecha_actual = now().date()
    prestamo.fecha_real_devolucion = fecha_actual
    prestamo.estado = 'FINALIZADO'
    prestamo.juego.estado = 'DISPONIBLE'
    prestamo.juego.save()
    prestamo.save()

    # Notificar si la devolución fue fuera del plazo
    if fecha_actual > prestamo.fecha_maxima_devolucion:
        messages.warning(
            request,
            f'El juego fue devuelto tarde. Fecha máxima: {prestamo.fecha_maxima_devolucion}.'
        )

    messages.success(request, f'El juego "{prestamo.juego.nombre}" ha sido devuelto exitosamente.')
    return redirect('prestamos')