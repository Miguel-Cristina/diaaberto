# Generated by Django 2.2.11 on 2020-06-19 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diaabertoapp', '0002_auto_20200619_1554'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='sessaoatividade',
            unique_together={('atividade', 'sessao')},
        ),
        migrations.RemoveField(
            model_name='sessaoatividade',
            name='dias',
        ),
    ]
