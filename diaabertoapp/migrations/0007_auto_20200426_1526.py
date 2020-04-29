# Generated by Django 2.2.11 on 2020-04-26 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diaabertoapp', '0006_auto_20200425_1734'),
    ]

    operations = [
        migrations.CreateModel(
            name='UtilizadorTipo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'UtilizadorTipo',
            },
        ),
        migrations.AddField(
            model_name='utilizador',
            name='cartao_cidadao',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='utilizador',
            name='data_nascimento',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='utilizador',
            name='deficiencias',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='utilizador',
            name='departamento',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='diaabertoapp.Departamento'),
        ),
        migrations.AddField(
            model_name='utilizador',
            name='email',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='utilizador',
            name='faculdade',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='diaabertoapp.Faculdade'),
        ),
        migrations.AddField(
            model_name='utilizador',
            name='numero_telemovel',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='utilizador',
            name='permitir_localizacao',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='utilizador',
            name='utilizar_dados_pessoais',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='utilizador',
            name='validado',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='utilizador',
            name='nome',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='UtilizadorParticipante',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('escola', models.CharField(max_length=255)),
                ('area_estudos', models.CharField(max_length=255)),
                ('ano_estudos', models.IntegerField(blank=True, null=True)),
                ('checkin', models.IntegerField(blank=True, null=True)),
                ('inscricao_id', models.IntegerField()),
                ('utilizador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='diaabertoapp.Utilizador')),
            ],
            options={
                'db_table': 'UtilizadorParticipante',
            },
        ),
        migrations.AddField(
            model_name='utilizador',
            name='utilizadortipo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='diaabertoapp.UtilizadorTipo'),
        ),
    ]
