# Generated by Django 2.2.11 on 2020-06-22 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diaabertoapp', '0008_auto_20200620_1625'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='edificio',
            name='mapa',
        ),
        migrations.RemoveField(
            model_name='sala',
            name='mapa',
        ),
    ]