from django.test import TestCase
from .models import *
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
import pytz
from django.core.urlresolvers import reverse

class ExchangeModelTestCase(TestCase):
    """Test suite for exchange model"""
    def setUp(self):
        """Define initialized exchange and other test variables"""
        self.exchange_name = 'sample_exchange'
        self.exchange_buy_fee = '1%'
        self.exchange_sell_fee = '2%'
        self.exchange_desc = 'an exchange'
        self.exchange = Exchange(name=self.exchange_name, buy_fee=self.exchange_buy_fee, sell_fee=self.exchange_sell_fee, desc=self.exchange_desc)

    def test_model_can_create_an_exchange(self):
        """Test the exchange model can create an exchange"""
        old_count = Exchange.objects.count()
        self.exchange.save()
        new_count = Exchange.objects.count()
        self.assertNotEqual(old_count, new_count)

class ExchangeViewTestCase(TestCase):
    """Test suite for the exchange api views"""
    def setUp(self):
        """Define the test client and other test variables"""
        user = User.objects.create_superuser(username="tom", email=None, password='password')

        self.client = APIClient()
        self.client.force_authenticate(user=user)

        currency = CryptoCurrency.objects.create(name='pepecoin', abbreviation='pp', symbol='p', supply_limit=1, founder='king pepe')
        self.exchange_data = {
            "name": "sample_exchange",
            "buy_fee": "1%",
            "sell_fee": "2%",
            "desc": "exchange",
            "products": [currency.id],
            "past_trades": [],
            "owner": user.id
        }
        self.response = self.client.post(
            '/exchange',
            self.exchange_data,
            format="json"
        )

    def test_api_can_create_an_exchange(self):
        """Test api has exchange creation capability"""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
    
    def test_api_can_get_an_exchange(self):
        """Test api can get a given exchange"""
        exchange = Exchange.objects.get(id=1)
        url = '/exchange/' + str(exchange.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_can_update_an_exchange(self):
        """Test api can delete a given exchange"""
        exchange = Exchange.objects.get(id=1)
        change_exchange = {
        "name": "apples",
        "owner": "admin",
        "buy_fee": "0.25%",
        "sell_fee": "0.16%",
        "desc": "good stuff",
        "products": [1],
        "created_at": "2018-07-24T16:43:16.699539Z",
        "updated_at": "2018-07-24T17:14:27.916056Z",
        "past_trades": []
    }
        url = '/exchange/' + str(exchange.id)
        res = self.client.put(
            url,
            change_exchange
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_an_exchange(self):
        """Test api can delete a given exchange"""
        exchange = Exchange.objects.get(id=1)
        url = '/exchange/' + str(exchange.id)
        res = self.client.delete(url)
        self.assertEquals(res.status_code, status.HTTP_204_NO_CONTENT)

class CryptoCurrencyModelTestCase(TestCase):
    """Test suite for cryptocurrency model"""
    def setUp(self):
        """Define initialized exchange and other test variables"""
        self.cryptocurrency_name = 'pepecoin'
        self.cryptocurrency_abbreviation = 'pp'
        self.cryptocurrency_symbol = 'p'
        self.cryptocurrency_supply_limit = 1
        self.cryptocurrency_founder = 'king pepe'
        self.cryptocurrency = CryptoCurrency(name=self.cryptocurrency_name, abbreviation=self.cryptocurrency_abbreviation, symbol=self.cryptocurrency_symbol, supply_limit=self.cryptocurrency_supply_limit, founder=self.cryptocurrency_founder)
    
    def test_model_can_create_an_cryptocurrency(self):
        """Test the cryptocurrency model can create a cryptocurrency"""
        old_count = CryptoCurrency.objects.count()
        self.cryptocurrency.save()
        new_count = CryptoCurrency.objects.count()
        self.assertNotEqual(old_count, new_count)

class CryptoCurrencyViewTestCase(TestCase):
    """Test suite for the cryptocurrency api views"""
    def setUp(self):
        """Define the test client and other test variables"""
        user = User.objects.create_superuser(username="tom", email=None, password='password')

        self.client = APIClient()
        self.client.force_authenticate(user=user)
        
        self.cryptocurrency_data = {
            "name": "pepecoin",
            "abbreviation": "pp",
            "symbol": "p",
            "supply_limit": 1,
            "founder": "king pepe",
            "trade": [],
            "owner": user.id
        }
        self.response = self.client.post(
            '/cryptocurrency',
            self.cryptocurrency_data,
            format="json"
        )

    def test_api_can_create_a_cryptocurrency(self):
        """Test api has cryptocurrency creation capability"""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_a_cryptocurrency(self):
        """Test api can get a given cryptocurrency"""
        cryptocurrency = CryptoCurrency.objects.get(id=1)
        url = '/cryptocurrency/' + str(cryptocurrency.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 

    def test_api_can_update_a_cryptocurrency(self):
        """Test api can update a given cryptocurrency"""
        cryptocurrency = CryptoCurrency.objects.get(id=1)
        change_cryptocurrency = {
        "name": "Bitcoin",
        "owner": "admin",
        "abbreviation": "BTC",
        "symbol": "₿",
        "supply_limit": 210000000,
        "founder": "Satoshi Nakatomo",
        "created_at": "2018-07-24T16:32:32.775971Z",
        "updated_at": "2018-07-24T16:32:32.776030Z",
        "trade": []
    }
        url = '/cryptocurrency/' + str(cryptocurrency.id)
        res = self.client.put(
            url,
            change_cryptocurrency
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_a_cryptocurrency(self):
        """Test api can delete a given cryptocurrency"""
        cryptocurrency = CryptoCurrency.objects.get(id=1)
        url = '/cryptocurrency/' + str(cryptocurrency.id)
        res = self.client.delete(url)
        self.assertEquals(res.status_code, status.HTTP_204_NO_CONTENT)  

class TransactionModelTestCase(TestCase):
    """Test suite for transaction model"""
    def setUp(self):
        """Define initialized transaction and other test variables"""
        CryptoCurrency.objects.create(name='pepecoin', abbreviation='pp', symbol='p', supply_limit=1, founder='king pepe')
        Exchange.objects.create(name='sample_exchange', buy_fee='2%', sell_fee='2%', desc='an exchange')
        self.transaction_volume = 42
        self.transaction_buy_price = 11
        self.transaction_sell_price = 12
        self.transaction_spot_price = 10
        self.transaction_time_stamp = timezone.now()
        self.transaction = Transaction(cryptocurrencies=CryptoCurrency.objects.get(id=1), exchanges=Exchange.objects.get(id=1), volume=self.transaction_volume, buy_price=self.transaction_buy_price, sell_price=self.transaction_sell_price, spot_price=self.transaction_spot_price, time_stamp=self.transaction_time_stamp)
    def test_model_can_create_an_transaction(self):
        old_count = Transaction.objects.count()
        self.transaction.save()
        new_count = Transaction.objects.count()
        self.assertNotEqual(old_count, new_count)

class TransactionViewTestCase(TestCase):
    """Test suite for the transaction api views"""
    def setUp(self):
        """Define the test client and other test variables"""
        self.client = APIClient()
        CryptoCurrency.objects.create(name='pepecoin', abbreviation='pp', symbol='p', supply_limit=1, founder='king pepe')
        Exchange.objects.create(name='sample_exchange', buy_fee='2%', sell_fee='2%', desc='an exchange')
        self.transaction_data = {
            "volume": 42,
            "buy_price": 12,
            "sell_price": 11,
            "spot_price": 10,
            "time_stamp": "2131-12-15T13:31:00Z",
            "cryptocurrencies": 1,
            "exchanges": 1
        }
        self.response = self.client.post(
            '/transaction',
            self.transaction_data,
            format="json"
        )

