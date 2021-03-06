# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-25 18:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0008_auto_20180725_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='cryptocurrency',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cryptocurrencies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='exchange',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='exchanges', to=settings.AUTH_USER_MODEL),
        ),
    ]
