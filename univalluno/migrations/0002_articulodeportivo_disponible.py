# Generated by Django 4.2.5 on 2023-09-30 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('univalluno', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='articulodeportivo',
            name='disponible',
            field=models.BooleanField(default=True),
        ),
    ]
