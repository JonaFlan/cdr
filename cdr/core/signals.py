from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Perfil
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model


@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)

@receiver(post_save, sender=User)
def guardar_perfil(sender, instance, **kwargs):
    instance.perfil.save()

@receiver(post_save, sender=get_user_model())
def asignar_grupo_miembro(sender, instance, created, **kwargs):
    if created:
        # Obtener el grupo "Miembros"
        grupo_miembro = Group.objects.get(name='Miembro')
        # Añadir el usuario recién creado al grupo "Miembros"
        instance.groups.add(grupo_miembro)