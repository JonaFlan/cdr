from django.urls import path
from .views import SesionCreateView, SesionUpdateView, SesionDeleteView
from .views import JuegoDetailView, JuegoCreateView, JuegoUpdateView, JuegoDeleteView
from .views import NoticiaDetailView, NoticiaCreateView, NoticiaUpdateView, NoticiaDeleteView
from .views import gestor_prestamos, confirmar_retiro, confirmar_devolucion, cancelar_prestamo
from .views import (
    index, biblioteca, perfil, sesiones, 
    inscribirse_sesion, anular_inscripcion_sesion, 
    noticias, dado, herramientas, mapas, 
    manuales, hojapj, ver_manual_juego, confirmar_reserva, liberar_juegos_no_retirados
)


urlpatterns = [
    path('', index, name='index'),
    path('perfil/', perfil, name='perfil'),

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
    path('inscribirse/<int:sesion_id>/', inscribirse_sesion, name='inscribirse_sesion'),

    # CRUD de Noticias
    path('noticias/', noticias, name='noticias'),
    path('noticias/crear/', NoticiaCreateView.as_view(), name='noticia_create'),
    path('noticias/<int:pk>/', NoticiaDetailView.as_view(), name='noticia_detail'),
    path('noticias/editar/<int:pk>', NoticiaUpdateView.as_view(), name='noticia_update'),
    path('noticias/eliminar/<int:pk>', NoticiaDeleteView.as_view(), name='noticia_delete'),
    
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



    path('test/', liberar_juegos_no_retirados, name='test')
]