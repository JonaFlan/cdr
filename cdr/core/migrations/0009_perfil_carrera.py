# Generated by Django 5.1.2 on 2024-11-04 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_sesion_usuarios_inscritos'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='carrera',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
