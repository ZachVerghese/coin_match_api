# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-23 20:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exchange',
            name='desc',
            field=models.TextField(default='', max_length=500),
            preserve_default=False,
        ),
    ]
