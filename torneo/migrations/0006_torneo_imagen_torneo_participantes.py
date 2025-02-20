# Generated by Django 5.1.2 on 2025-02-19 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('torneo', '0005_remove_torneo_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='torneo',
            name='imagen',
            field=models.FileField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='torneo',
            name='participantes',
            field=models.ManyToManyField(related_name='participante_torneo', through='torneo.TorneoParticipante', to='torneo.participante'),
        ),
    ]
