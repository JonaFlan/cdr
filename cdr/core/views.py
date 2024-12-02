from datetime import timedelta
from django.db.models import Case, When, IntegerField
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.timezone import now, localtime
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import Sesion, Juego, Noticia, Prestamo
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import Perfil  # Cambiar Profile por Perfil
from .forms import ProfileUpdateForm 
import os
from django.conf import settings



@login_required
def seleccionar_imagen_perfil(request):
    # Ruta absoluta al directorio de imágenes
    imagenes_dir = os.path.join(settings.BASE_DIR, 'core', 'static', 'perfil_imagenes')

    # Verifica si el directorio existe antes de listar
    if not os.path.exists(imagenes_dir):
        messages.error(request, 'El directorio de imágenes no existe.')
        return redirect('perfil')

    # Listar imágenes disponibles
    imagenes = [
        f'perfil_imagenes/{img}' for img in os.listdir(imagenes_dir)
        if img.endswith(('.png', '.jpg', '.jpeg', '.gif'))
    ]

    if request.method == 'POST':
        imagen_seleccionada = request.POST.get('imagen')
        if imagen_seleccionada and imagen_seleccionada in imagenes:
            perfil = request.user.perfil
            perfil.imagen = imagen_seleccionada
            perfil.save()
            messages.success(request, '¡Tu imagen de perfil ha sido actualizada!')
            return redirect('perfil')
        else:
            messages.error(request, 'Por favor selecciona una imagen válida.')

    return render(request, 'core/seleccionar_imagen_perfil.html', {
        'imagenes': imagenes
    })


# Solo accesible para administradores
@user_passes_test(lambda u: u.is_staff)
def gestor_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'core/gestor_usuarios.html', {'usuarios': usuarios})

@user_passes_test(lambda u: u.is_staff)
def crear_usuario(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        is_staff = 'is_staff' in request.POST
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe.")
        else:
            usuario = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                is_staff=is_staff
            )
            messages.success(request, "Usuario creado exitosamente.")
        return redirect('gestor_usuarios')
    return render(request, 'core/crear_usuario.html')

@user_passes_test(lambda u: u.is_staff)
def deshabilitar_usuario(request, user_id):
    usuario = get_object_or_404(User, pk=user_id)
    usuario.is_active = False
    usuario.save()
    messages.success(request, f'El usuario {usuario.username} ha sido deshabilitado.')
    return redirect('gestor_usuarios')

@user_passes_test(lambda u: u.is_staff)
def habilitar_usuario(request, user_id):
    usuario = get_object_or_404(User, pk=user_id)
    usuario.is_active = True
    usuario.save()
    messages.success(request, f'El usuario {usuario.username} ha sido habilitado.')
    return redirect('gestor_usuarios')

# @user_passes_test(lambda u: u.is_staff)
# def eliminar_usuario(request, user_id):
#     usuario = get_object_or_404(User, pk=user_id)

#     if request.method == "POST":
#         if usuario.is_staff:
#             messages.error(request, "No se puede eliminar un usuario administrador.")
#         else:
#             usuario.delete()
#             messages.success(request, f"El usuario {usuario.username} ha sido eliminado.")
#         return redirect('gestor_usuarios')

#     return render(request, 'core/eliminar_usuario.html', {'usuario': usuario})



# Decorador para permitir solo a administradores
def admin_required(user):
    return user.is_staff

# Create your views here.
def hojapj(request):
    return render(request, 'core/hojapj.html')

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
    user = request.user
    perfil = user.perfil  # Relación con el modelo Perfil
    imagen_form = ProfileUpdateForm(instance=perfil)
    password_form = PasswordChangeForm(user=user)

    if request.method == 'POST':
        if 'cambiar_imagen' in request.POST:
            imagen_form = ProfileUpdateForm(request.POST, instance=perfil)
            if imagen_form.is_valid():
                imagen_form.save()
                messages.success(request, 'Tu imagen de perfil ha sido actualizada.')
                return redirect('perfil')
        elif 'cambiar_contraseña' in request.POST:
            password_form = PasswordChangeForm(user=user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Mantener la sesión activa
                messages.success(request, 'Tu contraseña ha sido cambiada exitosamente.')
                return redirect('perfil')
            else:
                print(password_form.errors)  # Para depurar errores
                messages.error(request, 'Hubo un error al cambiar tu contraseña.')


    return render(request, 'core/perfil.html', {
        'user': user,
        'imagen_form': imagen_form,
        'password_form': password_form,
    })


#JUEGOS
def biblioteca(request):
    juegos = Juego.objects.all()
    return render(request, 'core/biblioteca.html', {'juegos': juegos})

class JuegoDetailView(DetailView):
    model = Juego
    template_name = 'core/juego_detalle.html'
    context_object_name = 'juego'

# Crear un juego (solo administradores)
class JuegoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Juego
    fields = ['nombre', 'proveedor', 'estado', 'imagen', 'descripcion', 'video_tutorial', 'jugadores_min', 'jugadores_max']
    template_name = 'core/juego_formulario.html'
    success_url = reverse_lazy('biblioteca')

    def test_func(self):
        return self.request.user.is_staff  # Solo permite acceso a administradores

# Editar un juego (solo administradores)
class JuegoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Juego
    fields = ['nombre', 'proveedor', 'estado', 'imagen', 'descripcion', 'video_tutorial', 'jugadores_min', 'jugadores_max']
    template_name = 'core/juego_formulario.html'
    success_url = reverse_lazy('biblioteca')

    def test_func(self):
        return self.request.user.is_staff  # Solo administradores

# Eliminar un juego (solo administradores)
class JuegoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Juego
    template_name = 'core/juego_confirmar_eliminar.html'
    success_url = reverse_lazy('biblioteca')

    def test_func(self):
        return self.request.user.is_staff  # Solo administradores


# SESIONES
@login_required
def sesiones(request):
    sesiones = Sesion.objects.all()
    return render(request, 'core/sesiones.html', {'sesiones': sesiones})

class SesionCreateView(CreateView):
    form_class = SesionForm
    template_name = 'core/sesion_form.html'
    success_url = reverse_lazy('sesiones')

    def form_valid(self, form):
        form.instance.creador = self.request.user
        form.instance.capacidad_maxima = form.instance.juego.jugadores_max

        response = super().form_valid(form)

        usuarios_ids = self.request.POST.getlist('usuarios_inscritos')
        for user_id in usuarios_ids:
            user = User.objects.get(id=user_id)
            form.instance.usuarios_inscritos.add(user)

        messages.success(self.request, 'La sesión ha sido creada exitosamente.')  

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuarios'] = User.objects.all()
        return context


class SesionUpdateView(UpdateView):
    model = Sesion
    form_class = SesionForm
    template_name = 'core/sesion_form.html'
    success_url = reverse_lazy('sesiones')

    def get_initial(self):
        initial = super().get_initial()
        if self.object.fecha:
            initial['fecha'] = localtime(self.object.fecha).strftime('%Y-%m-%dT%H:%M')
        return initial

    def form_valid(self, form):
        eliminar_usuarios = self.request.POST.getlist('eliminar_usuarios')
        for usuario_id in eliminar_usuarios:
            usuario = User.objects.get(id=usuario_id)
            form.instance.usuarios_inscritos.remove(usuario)

        response = super().form_valid(form)

        usuarios_ids = self.request.POST.getlist('usuarios_inscritos')
        for user_id in usuarios_ids:
            user = User.objects.get(id=user_id)
            if user not in form.instance.usuarios_inscritos.all():
                form.instance.usuarios_inscritos.add(user)

        messages.success(self.request, 'La sesión ha sido actualizada correctamente.')  

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuarios'] = User.objects.all()
        return context

class SesionDeleteView(DeleteView):
    model = Sesion
    template_name = 'core/sesion_confirm_delete.html'
    success_url = reverse_lazy('sesiones')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        
        if obj.creador != self.request.user:
            messages.error(self.request, 'No tienes permiso para eliminar esta sesión.')
            return redirect('sesiones')

        messages.success(self.request, 'La sesión ha sido eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)



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

class NoticiaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Noticia
    fields = ['titulo', 'contenido', 'imagen']
    template_name = 'core/noticia_formulario.html'
    success_url = reverse_lazy('noticias')

    def form_valid(self, form):
        form.instance.autor = self.request.user
        messages.success(self.request, 'La noticia ha sido creada exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al intentar crear la noticia. Por favor, verifica los datos.')
        return super().form_invalid(form)

    def test_func(self):
        return self.request.user.is_staff

class NoticiaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Noticia
    fields = ['titulo', 'contenido', 'imagen']
    template_name = 'core/noticia_formulario.html'
    success_url = reverse_lazy('noticias')

    def form_valid(self, form):
        messages.success(self.request, 'La noticia ha sido actualizada exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al actualizar la noticia. Por favor, verifica los datos.')
        return super().form_invalid(form)
    
    def test_func(self):
        return self.request.user.is_staff

class NoticiaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Noticia
    template_name = 'core/noticia_confirmar_eliminar.html'  # No es necesario porque usamos el modal
    success_url = reverse_lazy('noticias')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'La noticia ha sido eliminada correctamente.')
        return super().delete(request, *args, **kwargs)
    
    def test_func(self):
        return self.request.user.is_staff

#PRESTAMOS
def gestor_prestamos(request):
    if request.user.is_staff:
        # Obtener todos los préstamos para el administrador
        prestamos = Prestamo.objects.annotate(
            prioridad=Case(
                When(estado__in=["RESERVADO", "PRESTADO"], then=0),  # Préstamos vigentes
                When(estado__in=["CANCELADO", "FINALIZADO"], then=1),  # Préstamos terminados
                default=2,
                output_field=IntegerField(),
            )
        ).order_by(
            "prioridad",  # Primero los vigentes
            "fecha_solicitud",  # Orden ascendente para vigentes
            "-fecha_real_devolucion"  # Orden descendente para finalizados/cancelados
        )
    else:
        # Obtener solo los préstamos del usuario
        prestamos = Prestamo.objects.filter(usuario=request.user).annotate(
            prioridad=Case(
                When(estado__in=["RESERVADO", "PRESTADO"], then=0),
                When(estado__in=["CANCELADO", "FINALIZADO"], then=1),
                default=2,
                output_field=IntegerField(),
            )
        ).order_by(
            "prioridad",
            "fecha_solicitud",
            "-fecha_real_devolucion"
        )
    return render(request, "core/gestor_prestamos.html", {"prestamos": prestamos})

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


@user_passes_test(admin_required)
def confirmar_retiro(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk, estado="RESERVADO")
    prestamo.estado = "PRESTADO"
    prestamo.juego.estado = "PRESTADO"
    prestamo.save()
    prestamo.juego.save()
    messages.success(request, f"El retiro del juego '{prestamo.juego.nombre}' fue confirmado.")
    return redirect("gestor_prestamos")

@user_passes_test(admin_required)
def confirmar_devolucion(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk, estado="PRESTADO")
    prestamo.estado = "FINALIZADO"
    prestamo.juego.estado = "DISPONIBLE"
    prestamo.fecha_real_devolucion = now()
    prestamo.save()
    prestamo.juego.save()

    # Notificar si la devolución fue fuera del plazo
    if prestamo.atrasado:
        messages.warning(
            request,
            f'El juego fue devuelto tarde. Fecha máxima: {prestamo.fecha_maxima_devolucion}.'
        )

    messages.success(request, f"La devolución del juego '{prestamo.juego.nombre}' fue confirmada.")
    return redirect("gestor_prestamos")

@user_passes_test(admin_required)
def cancelar_prestamo(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)
    
    # Cambiar el estado a 'CANCELADO'
    prestamo.estado = 'CANCELADO'
    prestamo.save()
    
    messages.success(request, f"El préstamo del juego '{prestamo.juego.nombre}' ha sido cancelado por el administrador.")
    
    return redirect('gestor_prestamos')

#TAREAS
def liberar_juegos_no_retirados(request):
    """Libera juegos que no fueron retirados el mismo día."""
    hoy = localtime(now()).date()

    # Filtrar préstamos con fecha_reserva antes de hoy
    reservas_vencidas = Prestamo.objects.filter(
        estado='RESERVADO',
        fecha_reserva__date__lt=hoy  # Menores a hoy (incluye ayer y anteriores)
    )
    for prestamo in reservas_vencidas:
        prestamo.juego.estado = 'DISPONIBLE'
        prestamo.juego.save()
        prestamo.estado = 'CANCELADO'
        prestamo.save()
        print(f"Juego liberado: {prestamo.juego.nombre} (ID: {prestamo.juego.id})")
        
    return redirect('biblioteca')