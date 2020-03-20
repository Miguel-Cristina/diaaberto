# Generated by Django 2.2.11 on 2020-03-19 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diaabertoapp', '0008_edificio_campus'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sala',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('identificacao', models.CharField(max_length=40, unique=True)),
                ('edificio', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='diaabertoapp.Edificio')),
            ],
        ),
        migrations.RemoveField(
            model_name='localatividade',
            name='local',
        ),
        migrations.DeleteModel(
            name='Local',
        ),
        migrations.DeleteModel(
            name='LocalAtividade',
        ),
    ]