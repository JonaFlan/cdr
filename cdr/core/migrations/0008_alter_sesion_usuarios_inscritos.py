# Generated by Django 5.1.2 on 2024-11-04 06:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_sesion_usuarios_inscritos'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='sesion',
            name='usuarios_inscritos',
            field=models.ManyToManyField(blank=True, related_name='sesiones_inscritas', to=settings.AUTH_USER_MODEL),
        ),
    ]
