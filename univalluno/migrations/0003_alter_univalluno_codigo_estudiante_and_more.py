# Generated by Django 4.2.5 on 2023-10-02 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('univalluno', '0002_articulodeportivo_disponible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='univalluno',
            name='codigo_estudiante',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='univalluno',
            name='tipo_documento',
            field=models.CharField(choices=[('Cedula de cuidadania', 'Cedula de cuidadania'), ('NIT', 'NIT'), ('Cedula de extranjeria', 'Cedula de extranjeria'), ('Pasaporte', 'Pasaporte')], max_length=50),
        ),
    ]
