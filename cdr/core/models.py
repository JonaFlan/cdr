from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='perfil_imagenes/', default='img/default-profile.png')
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

    class Meta:
        verbose_name_plural = 'Perfiles'


class Juego(models.Model):
    nombre = models.CharField(max_length = 150)
    
    proveedor = models.CharField(max_length= 100)

    ESTADO_CHOICES = [
        ('DISPONIBLE', 'Disponible'),
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
    comentario = models.TextField(max_length=500)

    def __str__(self):
        return f'{self.nombre} | {self.estado}'

class Sesion(models.Model):
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    capacidad_maxima = models.PositiveIntegerField()
    usuarios_inscritos = models.ManyToManyField(User, related_name='sesiones_inscritas', blank=True)

    class Meta:
        verbose_name_plural = 'Sesiones'

    def __str__(self):
        return f'Sesión de {self.juego.nombre} el {self.fecha}'

    def cupos_disponibles(self):
        return self.capacidad_maxima - self.usuarios_inscritos.count()

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_publicacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.titulo