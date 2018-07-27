from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

ADMIN_ID = 1

class CryptoCurrency(models.Model):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=5)
    symbol = models.CharField(max_length=45)
    supply_limit = models.IntegerField()
    founder= models.CharField(max_length=255)
    created_at= models.DateTimeField(auto_now_add= True)
    updated_at= models.DateTimeField(auto_now= True)
    watchers = models.ManyToManyField(User, related_name= "crypto_preferences")
    owner = models.ForeignKey('auth.User',
    related_name='cryptocurrencies', 
    on_delete=models.CASCADE, default=ADMIN_ID)

class Exchange(models.Model):
    name = models.CharField(max_length=255)
    buy_fee= models.CharField(max_length=7)
    sell_fee= models.CharField(max_length=7)
    created_at= models.DateTimeField(auto_now_add= True)
    updated_at= models.DateTimeField(auto_now= True)
    desc=models.TextField(max_length=500)
    products = models.ManyToManyField(CryptoCurrency, related_name= "suppliers")
    owner = models.ForeignKey('auth.User',  # ADD THIS FIELD
    related_name='exchanges', 
    on_delete=models.CASCADE, default=ADMIN_ID)

class Transaction(models.Model):
    cryptocurrencies = models.ForeignKey(CryptoCurrency, related_name= "trade")
    exchanges = models.ForeignKey(Exchange, related_name= "past_trades")
    volume = models.DecimalField(max_digits = 20, decimal_places=2)
    buy_price= models.DecimalField(max_digits = 8, decimal_places=2)
    sell_price= models.DecimalField(max_digits = 8, decimal_places=2)
    spot_price= models.DecimalField(max_digits = 8, decimal_places=2)
    created_at= models.DateTimeField(auto_now_add= True)
    time_stamp= models.DateTimeField()
    updated_at= models.DateTimeField(auto_now= True)

    
