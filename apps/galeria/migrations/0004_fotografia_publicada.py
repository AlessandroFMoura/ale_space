# Generated by Django 4.1 on 2025-04-24 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galeria', '0003_fotografia_categoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='fotografia',
            name='publicada',
            field=models.BooleanField(default=False),
        ),
    ]
