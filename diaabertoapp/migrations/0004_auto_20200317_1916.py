# Generated by Django 2.2.11 on 2020-03-17 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diaabertoapp', '0003_auto_20200317_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atividade',
            name='local',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='diaabertoapp.LocalAtividade'),
        ),
    ]
