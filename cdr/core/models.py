from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from urllib.parse import urlparse, parse_qs
from django.utils.timezone import localtime

# Create your models here.

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen = models.CharField(
        max_length=255,
        default='perfil_imagenes/default-profile.png'  # Ruta relativa dentro de `static`
    )
    nivel = models.IntegerField(default=1)
    experiencia = models.IntegerField(default=0)

    TITULO_CHOICES = [
        ('NEOFITO', 'Neófito de la Cripta'),
        ('ACOLITO', 'Acolito de las sombras'),
        ('GUARDIAN', 'Guardián de la tumba'),
        ('SENIOR', 'Señor de la oscuridad'),
        ('MAESTRO', 'Maestro de la Cripta'),
        ('ARCHIMAGO', 'Archimago de las tinieblas'),
        ('LICH', 'Lich supremo'),
    ]
    titulo = models.CharField(
        max_length=50,
        choices=TITULO_CHOICES,
        default='NEOFITO'
    )

    carrera = models.CharField(max_length=50, null=True)
    rut = models.CharField(max_length=12, unique=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return f'Perfil de {self.usuario.username}'


class Juego(models.Model):
    nombre = models.CharField(max_length = 150)
    
    proveedor = models.CharField(max_length= 100)

    ESTADO_CHOICES = [
        ('DISPONIBLE', 'Disponible para préstamo'),
        ('PRESTADO', 'Prestado'),
        ('RESERVADO', 'Reservado'),
        ('NO_DISPONIBLE', 'No disponible'),
    ]
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='DISPONIBLE',
    )
    
    imagen = models.ImageField(upload_to='juegos_imagenes/', blank=True, null=True)
    descripcion = models.TextField(max_length=2000, blank=True, null=True)
    video_tutorial = models.URLField(max_length=500, blank=True, null=True)
    jugadores_min = models.PositiveIntegerField(default=1)
    jugadores_max = models.PositiveIntegerField(default=2) 

    def video_embed_url(self):
        if self.video_tutorial:
            url = urlparse(self.video_tutorial)
            # Si el enlace es del formato https://youtu.be/VIDEO_ID
            if url.netloc == "youtu.be":
                return f"https://www.youtube.com/embed{url.path}"
            # Si el enlace es del formato https://www.youtube.com/watch?v=VIDEO_ID
            elif url.netloc in ["www.youtube.com", "youtube.com"] and "v" in parse_qs(url.query):
                video_id = parse_qs(url.query)["v"][0]
                return f"https://www.youtube.com/embed/{video_id}"
        return None

    def __str__(self):
        return f'{self.nombre} | {self.estado}'
    
class Manual(models.Model):
    juego = models.ForeignKey(
        Juego,
        on_delete=models.CASCADE,
        related_name='manuales'
    )
    titulo = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='juegos_pdfs/')

    def __str__(self):
        return f'{self.titulo} | ({self.juego.nombre})'
    
    class Meta:
        verbose_name_plural = 'Manuales'

class Sesion(models.Model):
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    capacidad_maxima = models.PositiveIntegerField()
    usuarios_inscritos = models.ManyToManyField(User, related_name='sesiones_inscritas', blank=True)
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sesiones_creadas', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Sesiones'

    def __str__(self):
        return f'Sesión de {self.juego.nombre} el {self.fecha}'

    def cupos_disponibles(self):
        return self.capacidad_maxima - self.usuarios_inscritos.count()
    
    def titulo(self):
        fecha_formateada = localtime(self.fecha).strftime("%d/%m/%Y %H:%M")
        return f'{self.juego.nombre} - {fecha_formateada}'

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_publicacion = models.DateField(auto_now_add=True)
    imagen = models.ImageField(upload_to='noticias/', blank=True, null=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return self.titulo

class Prestamo(models.Model):
    ESTADO_CHOICES = [
        ('RESERVADO', 'Reservado'),
        ('PRESTADO', 'Prestado'),
        ('FINALIZADO', 'Finalizado'),
        ('CANCELADO', 'Cancelado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prestamos')
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, related_name='prestamos')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_maxima_devolucion = models.DateField()  # Fecha límite calculada
    fecha_real_devolucion = models.DateField(blank=True, null=True)  # Fecha en la que se devuelve
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='RESERVADO')
    atrasado = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f'Préstamo de {self.juego.nombre} por {self.usuario.username}'