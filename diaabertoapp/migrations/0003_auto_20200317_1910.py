# Generated by Django 2.2.11 on 2020-03-17 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diaabertoapp', '0002_auto_20200317_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atividade',
            name='local',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='diaabertoapp.LocalAtividade'),
        ),
    ]
