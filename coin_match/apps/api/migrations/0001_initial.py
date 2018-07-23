# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-23 20:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CryptoCurrency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('abbreviation', models.CharField(max_length=5)),
                ('symbol', models.CharField(max_length=45)),
                ('supply_limit', models.IntegerField()),
                ('founder', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('buy_fee', models.CharField(max_length=7)),
                ('sell_fee', models.CharField(max_length=7)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('products', models.ManyToManyField(related_name='suppliers', to='api.CryptoCurrency')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('volume', models.DecimalField(decimal_places=10, max_digits=20)),
                ('buy_price', models.DecimalField(decimal_places=10, max_digits=20)),
                ('sell_price', models.DecimalField(decimal_places=10, max_digits=20)),
                ('spot_price', models.DecimalField(decimal_places=10, max_digits=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('time_stamp', models.DateTimeField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cryptocurrencies', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trade', to='api.CryptoCurrency')),
                ('exchanges', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='past_trades', to='api.CryptoCurrency')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=45)),
                ('last_name', models.CharField(max_length=45)),
                ('email', models.CharField(max_length=45)),
                ('password', models.CharField(max_length=45)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='cryptocurrency',
            name='watchers',
            field=models.ManyToManyField(related_name='crypto_preferences', to='api.User'),
        ),
    ]
