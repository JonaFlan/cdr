from django.urls import path
from django.shortcuts import render
from .views import SesionCreateView, SesionUpdateView, SesionDeleteView
from .views import JuegoDetailView, JuegoCreateView, JuegoUpdateView, JuegoDeleteView
from .views import NoticiaDetailView, NoticiaCreateView, NoticiaUpdateView, NoticiaDeleteView
from .views import gestor_prestamos, confirmar_retiro, confirmar_devolucion, cancelar_prestamo, confirmar_inicio_sesion, confirmar_asistencia
from .views import (
    index, biblioteca, perfil, sesiones, 
    inscribirse_sesion, anular_inscripcion_sesion, 
    noticias, dado, herramientas, mapas, 
    manuales, hojapj, ver_manual_juego, confirmar_reserva, liberar_juegos_no_retirados,
    gestor_usuarios, crear_usuario, deshabilitar_usuario,seleccionar_imagen_perfil, habilitar_usuario, ver_perfil_usuario
)


urlpatterns = [
    path('', index, name='index'),
    #perfil
    path('perfil/', perfil, name='perfil'),
    path('perfil/<str:username>/', ver_perfil_usuario, name='ver_perfil_usuario'),
    path('seleccionar_imagen_perfil/', seleccionar_imagen_perfil, name='seleccionar_imagen_perfil'),

    # CRUD de JUEGOS
    path('biblioteca/', biblioteca, name='biblioteca' ),
    path('juegos/crear/', JuegoCreateView.as_view(), name='juego_crear'),
    path('juegos/<int:pk>/', JuegoDetailView.as_view(), name='juego_detalle'),
    path('juegos/editar/<int:pk>/', JuegoUpdateView.as_view(), name='juego_editar'),
    path('juegos/eliminar/<int:pk>/', JuegoDeleteView.as_view(), name='juego_eliminar'),

    # CRUD de SESIONES
    path('sesiones/', sesiones, name='sesiones'),
    path('sesiones/crear/', SesionCreateView.as_view(), name='sesion_create'),
    path('sesiones/editar/<int:pk>/', SesionUpdateView.as_view(), name='sesion_update'),
    path('sesiones/eliminar/<int:pk>/', SesionDeleteView.as_view(), name='sesion_delete'),
    path('sesiones/anular_inscripcion/<int:sesion_id>/', anular_inscripcion_sesion, name='anular_inscripcion_sesion'),
    path('sesiones/iniciar/<int:sesion_id>/', confirmar_inicio_sesion, name='iniciar_sesion_juego'),
    path('sesiones/asistencia/<int:sesion_id>/', confirmar_asistencia, name='confirmar_asistencia'),
    path('inscribirse/<int:sesion_id>/', inscribirse_sesion, name='inscribirse_sesion'),

    # CRUD de Noticias
    path('noticias/', noticias, name='noticias'),
    path('noticias/crear/', NoticiaCreateView.as_view(), name='noticia_crear'),
    path('noticias/<int:pk>/', NoticiaDetailView.as_view(), name='noticia_detalle'),
    path('noticias/editar/<int:pk>', NoticiaUpdateView.as_view(), name='noticia_editar'),
    path('noticias/eliminar/<int:pk>', NoticiaDeleteView.as_view(), name='noticia_eliminar'),
    
    # PRESTAMOS
    path('reservar/<int:pk>/', confirmar_reserva, name="confirmar_reserva" ),
    path("gestor_prestamos/", gestor_prestamos, name="gestor_prestamos"),
    path("gestor_prestamos/confirmar_retiro/<int:pk>/", confirmar_retiro, name="confirmar_retiro"),
    path("gestor_prestamos/confirmar_devolucion/<int:pk>/", confirmar_devolucion, name="confirmar_devolucion"),
    path('gestor_prestamos/cancelar/<int:pk>/', cancelar_prestamo, name='cancelar_prestamo'),


    # MISC 
    path('dado/', dado, name='dado'),
    path('herramientas/', herramientas, name='herramientas'),
    path('mapas/', mapas, name='mapas'),
    path('manuales/', manuales, name='manuales'),
    path('hojapj/', hojapj, name='hojapj'),
    path('manual/<int:juego_id>', ver_manual_juego, name='ver_manual_juego'),

    #GESTOR DE USUARIOS
    path('gestor_usuarios/', gestor_usuarios, name='gestor_usuarios'),
    path('crear_usuario/', crear_usuario, name='crear_usuario'),
    path('deshabilitar_usuario/<int:user_id>/', deshabilitar_usuario, name='deshabilitar_usuario'),
    path('gestor_usuarios/habilitar/<int:user_id>/', habilitar_usuario, name='habilitar_usuario'),

    
    path('test/', liberar_juegos_no_retirados, name='test')

]

# Asignar la misma vista para todos los errores
handler404 = 'core.views.error_view'
handler500 = 'core.views.error_view'
handler403 = 'core.views.error_view'