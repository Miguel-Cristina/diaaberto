# Generated by Django 2.2.11 on 2020-03-09 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diaabertoapp', '0004_auto_20200309_1409'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='localatividade',
            name='campus',
        ),
    ]