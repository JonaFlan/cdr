# Generated by Django 5.1.2 on 2024-12-08 22:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_perfil_rut'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil',
            name='experiencia',
        ),
        migrations.AddField(
            model_name='perfil',
            name='cdlc',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='perfil',
            name='xp',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sesion',
            name='cdlc_creador',
            field=models.PositiveIntegerField(default=25),
        ),
        migrations.AddField(
            model_name='sesion',
            name='cdlc_participante',
            field=models.PositiveIntegerField(default=10),
        ),
        migrations.AddField(
            model_name='sesion',
            name='codigo_secreto',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='sesion',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('en_curso', 'En curso'), ('finalizada', 'Finalizada')], default='pendiente', max_length=20),
        ),
        migrations.AddField(
            model_name='sesion',
            name='usuarios_participantes',
            field=models.ManyToManyField(blank=True, related_name='sesiones_participadas', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sesion',
            name='xp_creador',
            field=models.PositiveIntegerField(default=50),
        ),
        migrations.AddField(
            model_name='sesion',
            name='xp_participante',
            field=models.PositiveIntegerField(default=20),
        ),
    ]