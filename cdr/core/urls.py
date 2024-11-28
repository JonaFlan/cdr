from django.urls import path
from .views import index, biblioteca, perfil, sesiones, inscribirse_sesion, anular_inscripcion_sesion, noticias, dado, herramientas ,mapas, manuales, hojapj, ver_manual_juego
from .views import SesionCreateView, SesionUpdateView, SesionDeleteView
from .views import JuegoDetailView, JuegoCreateView, JuegoUpdateView, JuegoDeleteView
from .views import NoticiaDetailView, NoticiaCreateView, NoticiaUpdateView, NoticiaDeleteView
urlpatterns = [
    path('', index, name='index'),
    path('perfil/', perfil, name='perfil'),

    # CRUD de JUEGOS
    path('biblioteca/', biblioteca, name='biblioteca' ),
    path('juegos/crear/', JuegoCreateView.as_view(), name='juego_create'),
    path('juegos/<int:pk>/', JuegoDetailView.as_view(), name='juego_detail'),
    path('juegos/<int:pk>/editar/', JuegoUpdateView.as_view(), name='juego_update'),
    path('juegos/<int:pk>/eliminar/', JuegoDeleteView.as_view(), name='juego_delete'),

    # CRUD de SESIONES
    path('sesiones/', sesiones, name='sesiones'),
    path('sesiones/crear/', SesionCreateView.as_view(), name='sesion_create'),
    path('sesiones/<int:pk>/editar/', SesionUpdateView.as_view(), name='sesion_update'),
    path('sesiones/<int:pk>/eliminar/', SesionDeleteView.as_view(), name='sesion_delete'),
    path('inscribirse/<int:sesion_id>/', inscribirse_sesion, name='inscribirse_sesion'),
    path('sesiones/anular_inscripcion/<int:sesion_id>/', anular_inscripcion_sesion, name='anular_inscripcion_sesion'),

    # CRUD de Noticias
    path('noticias/', noticias, name='noticias'),
    path('noticias/crear/', NoticiaCreateView.as_view(), name='noticia_create'),
    path('noticias/<int:pk>/', NoticiaDetailView.as_view(), name='noticia_detail'),
    path('noticias/<int:pk>/editar/', NoticiaUpdateView.as_view(), name='noticia_update'),
    path('noticias/<int:pk>/eliminar/', NoticiaDeleteView.as_view(), name='noticia_delete'),

    path('dado/', dado, name='dado'),
    path('herramientas/', herramientas, name='herramientas'),
    path('mapas/', mapas, name='mapas'),
    path('manuales/', manuales, name='manuales'),
    path('hojapj/', hojapj, name='hojapj'),
    path('manual/<int:juego_id>', ver_manual_juego, name='ver_manual_juego'),
]