# Generated by Django 2.2.11 on 2020-03-14 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diaabertoapp', '0029_auto_20200312_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campus',
            name='nome',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
