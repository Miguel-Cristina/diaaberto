# Generated by Django 2.2.11 on 2020-04-01 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diaabertoapp', '0003_auto_20200401_1440'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tarefa',
            old_name='colaborador',
            new_name='coolaborador',
        ),
        migrations.RenameField(
            model_name='tarefa',
            old_name='coordenador',
            new_name='cordenador',
        ),
    ]