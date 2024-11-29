# Generated by Django 5.1.2 on 2024-11-29 19:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_juego_jugadores_max_juego_jugadores_min'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Prestamo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_solicitud', models.DateTimeField(auto_now_add=True)),
                ('fecha_maxima_devolucion', models.DateField()),
                ('fecha_real_devolucion', models.DateField(blank=True, null=True)),
                ('estado', models.CharField(choices=[('RESERVADO', 'Reservado'), ('PRESTADO', 'Prestado'), ('FINALIZADO', 'Finalizado')], default='RESERVADO', max_length=20)),
                ('juego', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prestamos', to='core.juego')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prestamos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]