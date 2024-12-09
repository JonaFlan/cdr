from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from urllib.parse import urlparse, parse_qs
from django.utils.timezone import localtime
import random
import string


# Create your models here.

class Perfil(models.Model):

    TITULO_CHOICES = [
        ('NEOFITO', 'Neófito de la Cripta'),
        ('ACOLITO', 'Acolito de las sombras'),
        ('GUARDIAN', 'Guardián de la tumba'),
        ('SENIOR', 'Señor de la oscuridad'),
        ('MAESTRO', 'Maestro de la Cripta'),
        ('ARCHIMAGO', 'Archimago de las tinieblas'),
        ('LICH', 'Lich supremo'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen = models.CharField(max_length=255, default='perfil_imagenes/default-profile.png')  # Ruta relativa dentro de `static`
    nivel = models.IntegerField(default=1)
    titulo = models.CharField(max_length=50, choices=TITULO_CHOICES, default='NEOFITO')
    carrera = models.CharField(max_length=50, null=True)
    rut = models.CharField(max_length=12, unique=True, null=True, blank=True)
    xp = models.PositiveIntegerField(default=0)  # Experiencia
    cdlc = models.PositiveIntegerField(default=0)  # Créditos De La Cripta

    def agregar_recompensas(self, xp=0, cdlc=0):
        self.xp += xp
        self.cdlc += cdlc
        self.save()

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
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_curso', 'En curso'),
        ('finalizada', 'Finalizada'),
    ]

    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    capacidad_maxima = models.PositiveIntegerField()
    usuarios_inscritos = models.ManyToManyField(User, related_name='sesiones_inscritas', blank=True)
    usuarios_participantes = models.ManyToManyField(User, related_name='sesiones_participadas', blank=True)
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sesiones_creadas', blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    xp_participante = models.PositiveIntegerField(default=20)  # XP por participar
    cdlc_participante = models.PositiveIntegerField(default=10)  # CDLC por participar
    xp_creador = models.PositiveIntegerField(default=50)  # XP por crear la sesión
    cdlc_creador = models.PositiveIntegerField(default=25)  # CDLC por organizar
    codigo_secreto = models.CharField(max_length=6, blank=True, null=True)  # Código de acceso


    class Meta:
        verbose_name_plural = 'Sesiones'

    def __str__(self):
        return f'Sesión de {self.juego.nombre} el {self.fecha}'

    def cupos_disponibles(self):
        return self.capacidad_maxima - self.usuarios_inscritos.count()
    
    def generar_codigo_secreto(self):
        """Genera un código aleatorio para la sesión."""
        self.codigo_secreto = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.save()
    
    def verificar_codigo(self, codigo):
        """Verifica si el código ingresado coincide con el de la sesión."""
        return self.codigo_secreto == codigo

    def otorgar_recompensas(self):
        # Recompensas para el creador
        self.creador.perfil.agregar_recompensas(xp=self.xp_creador, cdlc=self.cdlc_creador)
        
        # Recompensas para los participantes
        for usuario in self.usuarios_participantes.all():
            usuario.perfil.agregar_recompensas(xp=self.xp_participante, cdlc=self.cdlc_participante)

        # Cambiar el estado a finalizada
        self.estado = 'finalizada'
        self.save()

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