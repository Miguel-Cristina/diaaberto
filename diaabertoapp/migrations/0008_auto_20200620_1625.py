# Generated by Django 2.2.11 on 2020-06-20 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diaabertoapp', '0007_auto_20200620_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edificio',
            name='mapa_imagem',
            field=models.ImageField(default='diaabertoapp/maps/default.png', upload_to='diaabertoapp/maps/'),
        ),
        migrations.AlterField(
            model_name='sala',
            name='mapa_imagem',
            field=models.ImageField(default='diaabertoapp/maps/default.png', upload_to='diaabertoapp/maps/'),
        ),
    ]