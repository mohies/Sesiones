# Generated by Django 5.1.2 on 2025-02-19 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('torneo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='torneo',
            name='participantes',
        ),
        migrations.AddField(
            model_name='torneo',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='torneos/'),
        ),
        migrations.AlterField(
            model_name='torneo',
            name='categoria',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='torneo',
            name='fecha_inicio',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='torneo',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
    ]
