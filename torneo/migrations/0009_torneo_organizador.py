# Generated by Django 5.1.2 on 2025-03-02 13:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('torneo', '0008_alter_torneo_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='torneo',
            name='organizador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='torneos_organizados', to=settings.AUTH_USER_MODEL),
        ),
    ]
