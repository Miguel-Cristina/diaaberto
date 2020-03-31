# Generated by Django 2.2.11 on 2020-03-31 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diaabertoapp', '0017_auto_20200330_1258'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sessao',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('hora', models.TimeField(null=True, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='materialquantidade',
            name='quantidade',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='SessaoAtividade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.DateField(null=True)),
                ('atividade', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sessao_atividade', to='diaabertoapp.Atividade')),
                ('sessao', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='diaabertoapp.Sessao')),
            ],
        ),
    ]