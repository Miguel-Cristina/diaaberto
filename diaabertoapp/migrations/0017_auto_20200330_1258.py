# Generated by Django 2.2.11 on 2020-03-30 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diaabertoapp', '0016_auto_20200324_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialquantidade',
            name='material',
            field=models.CharField(max_length=255, null=True),
        ),
    ]