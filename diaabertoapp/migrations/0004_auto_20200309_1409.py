# Generated by Django 2.2.11 on 2020-03-09 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diaabertoapp', '0003_campus_localatividade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campus',
            name='morada',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='campus',
            name='nome',
            field=models.CharField(max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='edificio',
            name='nome',
            field=models.CharField(max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='localatividade',
            name='descricao',
            field=models.TextField(null=True),
        ),
    ]
