from django.urls import path
from .views import index, biblioteca, perfil, sesiones, inscribirse_sesion, anular_inscripcion_sesion, noticias, dado, herramientas,mapas,manuales
urlpatterns = [
    path('', index, name='index'),
    path('biblioteca/', biblioteca, name='biblioteca' ),
    path('perfil/', perfil, name='perfil'),
    path('sesiones/', sesiones, name='sesiones'),
    path('inscribirse/<int:sesion_id>/', inscribirse_sesion, name='inscribirse_sesion'),
    path('sesiones/anular_inscripcion/<int:sesion_id>/', anular_inscripcion_sesion, name='anular_inscripcion_sesion'),
    path('noticias/', noticias, name='noticias'),
    path('dado/', dado, name='dado'),
    path('herramientas/', herramientas, name='herramientas'),
    path('mapas/', mapas, name='mapas'),
    path('manuales/', manuales, name='manuales'),
]