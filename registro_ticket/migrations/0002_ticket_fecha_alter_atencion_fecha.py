# Generated by Django 4.2.6 on 2023-12-05 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registro_ticket', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='fecha',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='atencion',
            name='fecha',
            field=models.DateField(auto_now=True),
        ),
    ]
