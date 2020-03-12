# Generated by Django 2.2.11 on 2020-03-11 23:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diaabertoapp', '0022_atividade_materiais'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='atividade',
            name='materiais',
        ),
        migrations.CreateModel(
            name='AtividadeMaterial',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantidade', models.IntegerField()),
                ('atividade_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='diaabertoapp.Atividade')),
                ('material_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='diaabertoapp.Material')),
            ],
        ),
    ]
