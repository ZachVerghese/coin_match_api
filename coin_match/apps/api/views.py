from django.shortcuts import render, HttpResponse
from rest_framework import generics, permissions
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
import requests
from datetime import datetime
from .serializers import *
from .models import *
import json

class CryptoView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the cryptocurrency http GET, PUT and DELETE requests."""
    queryset= CryptoCurrency.objects.all()
    serializer_class=CryptoCurrencySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class CryptoCreate(generics.ListCreateAPIView):
    """This class defines the cryptocurrency create behavior of our rest api."""
    queryset = CryptoCurrency.objects.all()
    serializer_class = CryptoCurrencySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def perform_create(self, serializer):
        """Save the post data when creating a new cryptocurrency."""
        serializer.save()

class ExchangeView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the exchange http GET, PUT and DELETE requests."""
    queryset= Exchange.objects.all()
    serializer_class=ExchangeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class ExchangeCreate(generics.ListCreateAPIView):
    """This class defines the exchange create behavior of our rest api."""
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def perform_create(self, serializer):
        """Save the post data when creating a new exchange."""
        serializer.save()

class TransactionView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the transaction http GET, PUT and DELETE requests."""
    queryset= Transaction.objects.all()
    serializer_class=TransactionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class TransactionCreate(generics.ListCreateAPIView):
    """This class defines the transaction create behavior of our rest api."""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def perform_create(self, serializer):
        """Save the post data when creating a new transaction."""
        serializer.save()

class UserView(generics.ListAPIView):
    """View to list the user queryset."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailsView(generics.RetrieveAPIView):
    """View to retrieve a user instance."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
def index(request):
    print(coinsquare_data_retrieval())
    print(kraken_data_retrieval("XBT","USD"))
    print(cex_data_retrieval("BTC","USD"))
    print(bitstamp_data_retrieval("btc","usd"))
    print(bitsquare_data_retrieval("btc","usd"))
    print(localbitcoin_data_retrieval())
    print(gemini_data_retrieval("btc","usd"))
    print(coinbase_data_retrieval("BTC","USD"))

    return HttpResponse("This is a test page. Please visit endpoints starting with /exchange or /cryptocurrency to try the API!")

def coinsquare_data_retrieval():
    r= requests.get('https://coinsquare.com/api/v1/data/quotes')
    ticker= r.json()['quotes'][1]
    name= "Bitcoin"
    abbr="BTC"
    volume = float(ticker['volume'])
    time_stamp= datetime.now()
    if ticker['bid'] =='null':
        buy_price= 0
    else: 
        buy_price = float(ticker['bid'])
    if ticker['ask'] =='null' or ticker['ask'] ==None:
        sell_price= 0
    else:
        sell_price=float(ticker['ask'])
    if ticker['last'] =='null' or ticker['ask'] == None:
        spot_price= 0
    else:
        spot_price = float(ticker['last'])
    Transaction.objects.create(cryptocurrencies= CryptoCurrency.objects.get(name=name),exchanges= Exchange.objects.get(name="Coinsquare"), volume=volume, buy_price=buy_price,sell_price=sell_price,spot_price=spot_price,time_stamp=time_stamp)
    coinsquare_context_main={
        "exchange": "Coinsquare",
        "coin":name,
        "abbr":abbr,
        "spot_price":spot_price,
        "time_stamp":str(time_stamp),
        "volume":volume,
        "buy":buy_price,
        "sell":sell_price
    }
    return coinsquare_context_main

def kraken_data_retrieval(curr1,curr2):
    r= requests.get(f'https://api.kraken.com/0/public/Ticker?pair={curr1}{curr2}')
    if curr1 == "XBT":
        name= "Bitcoin"
        ticker= r.json()['result'][f'X{curr1}Z{curr2}']
    elif curr1 == "BCH":
        name="Bitcoin Cash"
        ticker= r.json()['result'][f'{curr1}{curr2}']
    elif curr1 == "DASH":
        name="Dash"
        ticker= r.json()['result'][f'{curr1}{curr2}']
    elif curr1 == "ETH":
        name= "Ethereum"
        ticker= r.json()['result'][f'X{curr1}Z{curr2}']
    elif curr1 == "LTC":
        name="LiteCoin"
        ticker= r.json()['result'][f'X{curr1}Z{curr2}']
    # elif curr1 =="DOGE":
    #     name="Dogecoin"
    #     ticker= r.json()['result'][f'XRD{curr2}']
    elif curr1 =="XRP":
        name="Ripple"
        ticker= r.json()['result'][f'X{curr1}Z{curr2}']
    volume=float(ticker['v'][1])
    time_stamp = datetime.now()
    
    if ticker['b'][0]=='null' or ticker['b'][0] == None:
        buy_price= 0
    else:
        buy_price=float(ticker['b'][0])
    if ticker['a'][0]=='null' or ticker['a'][0] == None:
        sell_price= 0
    else:
        sell_price=float(ticker['a'][0])
    if ticker['c'][0]=='null' or ticker['c'][0] == None:
        spot_price= 0
    else:
        spot_price=float(ticker['c'][0])
    Transaction.objects.create(cryptocurrencies= CryptoCurrency.objects.get(name=name),exchanges= Exchange.objects.get(name="Kraken"), volume=volume, buy_price=buy_price,sell_price=sell_price,spot_price=spot_price,time_stamp=time_stamp)
    kraken_context_main={
        "exchange":"Kraken",
        "coin":name,
        "abbr":curr1,
        "spot_price":spot_price,
        "time_stamp":str(time_stamp),
        "volume":volume,
        "buy":buy_price,
        "sell":sell_price
    }
    return kraken_context_main

def cex_data_retrieval(curr1,curr2):
    r= requests.get(f'https://cex.io/api/ticker/{curr1}/{curr2}')
    ticker= r.json()
    if curr1 == "BTC":
        name= "Bitcoin"
    elif curr1 == "BCH":
        name="Bitcoin Cash"
    elif curr1 == "DASH":
        name="Dash"
    elif curr1 == "ETH":
        name= "Ethereum"
    elif curr1 =="XRP":
        name="Ripple"
    volume=float(ticker['volume'])
    time_stamp=datetime.fromtimestamp(int(ticker['timestamp']))
    if ticker['bid'] =='null' or ticker['bid']==None:
        buy_price= 0
    else:
        buy_price=float(ticker['bid'])
    if ticker['ask'] =='null' or ticker['ask']==None:
        sell_price= 0
    else:
        sell_price=float(ticker['ask'])
    if ticker['last'] =='null' or ticker['last']==None:
        spot_price= 0
    else:
        spot_price=float(ticker['last'])
    Transaction.objects.create(cryptocurrencies= CryptoCurrency.objects.get(name=name),exchanges= Exchange.objects.get(name="Cex.io"), volume=volume, buy_price=buy_price,sell_price=sell_price,spot_price=spot_price,time_stamp=time_stamp)
    cex_context_main={
        "exchange":"CEX.io",
        "coin":name,
        "abbr":curr1,
        "spot_price":spot_price,
        "time_stamp":str(time_stamp),
        "volume":volume,
        "buy":buy_price,
        "sell":sell_price
    }
    return cex_context_main

def bitstamp_data_retrieval(curr1,curr2):
    r= requests.get(f'https://www.bitstamp.net/api/v2/ticker/{curr1}{curr2}')
    # r= requests.get('https://www.bitstamp.net/api/v2/ticker/btcusd')
    ticker= r.json()
    if curr1 == "btc":
        name= "Bitcoin"
    elif curr1 == "bch":
        name="Bitcoin Cash"
    elif curr1 == "eth":
        name= "Ethereum"
    elif curr1 == "ltc":
        name="LiteCoin"
    elif curr1 =="xrp":
        name="Ripple"
    volume=float(ticker['volume'])
    time_stamp = datetime.fromtimestamp(int(ticker['timestamp']))
    if ticker['bid'] =='null' or ticker['bid']==None:
        buy_price= 0
    else:
        buy_price=float(ticker['bid'])
    if ticker['ask'] =='null' or ticker['ask']==None:
        sell_price= 0
    else:
        sell_price=float(ticker['ask'])
    if ticker['last'] =='null' or ticker['last']==None:
        spot_price= 0
    else:
        spot_price=float(ticker['last'])
    Transaction.objects.create(cryptocurrencies= CryptoCurrency.objects.get(name=name),exchanges= Exchange.objects.get(name="BitStamp"), volume=volume, buy_price=buy_price,sell_price=sell_price,spot_price=spot_price,time_stamp=time_stamp)
    bitstamp_context_main={
        "exchange":"BitStamp",
        "coin":name,
        "abbr":curr1,
        "spot_price":spot_price,
        "time_stamp":str(time_stamp),
        "volume":volume,
        "buy":buy_price,
        "sell":sell_price
        }
    return bitstamp_context_main

def bitsquare_data_retrieval(curr1,curr2):
    r= requests.get(f'https://markets.bisq.network/api/ticker?market={curr1}_{curr2}')
    ticker= r.json()[0]
    name="Bitcoin"
    volume=float(ticker['volume_right'])
    time_stamp = datetime.now()
    if ticker['buy'] == None or ticker['buy']=="null":
        buy_price= 0
    else:
        buy_price=float(ticker['buy'])
    if ticker['sell'] =='null' or ticker['sell']==None:
        sell_price= 0
    else:
        sell_price=float(ticker['sell'])
    if ticker['last'] =='null' or ticker['last']==None:
        spot_price= 0
    else:
        spot_price=float(ticker['last'])
    Transaction.objects.create(cryptocurrencies= CryptoCurrency.objects.get(name=name),exchanges= Exchange.objects.get(name="Bitsquare"), volume=volume, buy_price=buy_price,sell_price=sell_price,spot_price=spot_price,time_stamp=time_stamp)
    bitsquare_context_main={
        "exchange":"Bitsquare",
        "coin":name,
        "abbr":curr1,
        "spot_price":spot_price,
        "time_stamp":str(time_stamp),
        "volume":volume,
        "buy":buy_price,
        "sell":sell_price
    }
    return bitsquare_context_main

def localbitcoin_data_retrieval():
    r= requests.get('https://localbitcoins.com/bitcoincharts/usd/trades.json')
    ticker= r.json()[499]
    abbr= "BTC"
    name= "Bitcoin"
    volume=float(ticker['amount'])
    time_stamp = datetime.fromtimestamp(int(ticker['date']))
    if ticker['price'] =='null' or ticker['price']==None:
        spot_price= 0
    else:
        spot_price=float(ticker['price'])
    buy_price=0
    sell_price=0
    Transaction.objects.create(cryptocurrencies= CryptoCurrency.objects.get(name=name),exchanges= Exchange.objects.get(name="Local Bitcoin"), volume=volume, buy_price=buy_price,sell_price=sell_price,spot_price=spot_price,time_stamp=time_stamp)
    local_context_main={
        "exchange":"Local Bitcoin",
        "coin":name,
        "abbr":abbr,
        "spot_price":spot_price,
        "time_stamp":str(time_stamp),
        "volume":volume,
        "buy":buy_price,
        "sell":sell_price
    }
    return local_context_main

def gemini_data_retrieval(curr1,curr2):
    r= requests.get(f'https://api.gemini.com/v1/pubticker/{curr1}{curr2}')
    ticker= r.json()
    if curr1== "btc":
        name="Bitcoin"
    elif curr1=="eth":
        name="Ethereum"
    volume=float(ticker['volume'][f'{curr1}'.upper()])
    time_stamp = datetime.fromtimestamp(int(ticker['volume']['timestamp'])/1000)
    if ticker['bid'] =='null' or ticker['bid']==None:
        buy_price= 0
    else:
        buy_price=float(ticker['bid'])
    if ticker['ask']=='null' or ticker['ask']==None:
        sell_price= 0
    else:
        sell_price=float(ticker['ask'])
    if ticker['last'] =='null' or ticker['last']==None:
        spot_price= 0
    else:
        spot_price=float(ticker['last'])
    Transaction.objects.create(cryptocurrencies= CryptoCurrency.objects.get(name=name),exchanges= Exchange.objects.get(name="Gemini"), volume=volume, buy_price=buy_price,sell_price=sell_price,spot_price=spot_price,time_stamp=time_stamp)
    gemimi_context_main={
        "exchange":"Gemini",
        "coin":name,
        "abbr":curr1,
        "spot_price":spot_price,
        "time_stamp":str(time_stamp),
        "volume":volume,
        "buy":buy_price,
        "sell":sell_price
    }
    return gemimi_context_main

def coinbase_data_retrieval(curr1,curr2):
    r= requests.get(f'https://api.coinbase.com/v2/prices/{curr1}-{curr2}/spot')
    ticker= r.json()['data']
    if curr1=="BTC":
        name="Bitcoin"
    elif curr1=="ETH":
        name="Ethereum"
    elif curr1=="BCH":
        name="Bitcoin Cash"
    elif curr1== "LTC":
        name="LiteCoin"
    if ticker['amount'] =='null' or ticker['amount']==None:
        spot_price= 0
    else:
        spot_price=float(ticker['amount'])
    b = requests.get(f'https://api.coinbase.com/v2/prices/{curr1}-{curr2}/buy')
    ticker2=b.json()['data']
    if ticker2['amount'] =='null' or ticker2['amount']==None:
        buy_price= 0
    else:
        buy_price=float(ticker2['amount'])
    s = requests.get(f'https://api.coinbase.com/v2/prices/{curr1}-{curr2}/sell')
    ticker3=s.json()['data']
    if ticker3['amount'] =='null' or ticker3['amount']==None:
        sell_price= 0
    else:
        sell_price=float(ticker3['amount'])
    time_stamp=datetime.now()
    volume=0
    Transaction.objects.create(cryptocurrencies= CryptoCurrency.objects.get(name=name),exchanges= Exchange.objects.get(name="Coinbase"), volume=volume, buy_price=buy_price,sell_price=sell_price,spot_price=spot_price,time_stamp=time_stamp)
    coinbase_context_main={
        "exchange":"Coinbase",
        "coin":name,
        "abbr":curr1,
        "spot_price":spot_price,
        "time_stamp":str(time_stamp),
        "volume":volume,
        "buy":buy_price,
        "sell":sell_price
    }
    return coinbase_context_main

def show_crypto(request, pk):
    crypto= CryptoCurrency.objects.get(id=pk)
    exchanges=crypto.suppliers.all()
    transactions= Transaction.objects.filter(cryptocurrencies=crypto).filter(exchanges=exchanges)
    context=[]
    if crypto.abbreviation=="BTC":
        context=[coinsquare_data_retrieval(),kraken_data_retrieval("XBT","USD"),cex_data_retrieval("BTC","USD"),bitstamp_data_retrieval("btc","usd"),bitsquare_data_retrieval("btc","usd"),localbitcoin_data_retrieval(),gemini_data_retrieval("btc","usd"),coinbase_data_retrieval("BTC","USD")]
    elif crypto.abbreviation=="ETH":
        context=[coinbase_data_retrieval("ETH","USD"),kraken_data_retrieval("ETH","USD"),cex_data_retrieval("ETH","USD"),bitstamp_data_retrieval("eth","usd"),gemini_data_retrieval("eth","usd")]
    elif crypto.abbreviation=="BCH":
        context=[coinbase_data_retrieval("BCH","USD"),kraken_data_retrieval("BCH","USD"),cex_data_retrieval("BCH","USD"),bitstamp_data_retrieval("bch","usd")]
    elif crypto.abbreviation=="LTC":
        context=[coinbase_data_retrieval("LTC","USD"),kraken_data_retrieval("LTC","USD"),bitstamp_data_retrieval("ltc","usd")]
    elif crypto.abbreviation=="DASH":
        context=[kraken_data_retrieval("DASH","USD"),cex_data_retrieval("DASH","USD")]
    elif crypto.abbreviation=="XRP":
        context=[kraken_data_retrieval("XRP","USD"),cex_data_retrieval("XRP","USD"),bitstamp_data_retrieval("xrp","usd")]
    return HttpResponse(json.dumps(context), content_type="application/json")

def show_exchange(request,pk):
    exchange= Exchange.objects.get(id=pk)
    currencies= exchange.products.all()
    context=[]
    if exchange.name == "Cex.io":
        context=[cex_data_retrieval("BTC","USD"),cex_data_retrieval("ETH","USD"),cex_data_retrieval("BCH","USD"),cex_data_retrieval("XRP","USD"),cex_data_retrieval("DASH","USD")]
    elif exchange.name == "Coinbase":
        context=[coinbase_data_retrieval("BTC","USD"),coinbase_data_retrieval("ETH","USD"),coinbase_data_retrieval("BCH","USD")]
    elif exchange.name=="Coinsquare":
        context=[coinsquare_data_retrieval()]
    elif exchange.name=="Kraken":
        context=[kraken_data_retrieval("XBT","USD"),kraken_data_retrieval("ETH","USD"),kraken_data_retrieval("BCH","USD"),kraken_data_retrieval("LTC","USD"),kraken_data_retrieval("XRP","USD"),kraken_data_retrieval("DASH","USD")]
    elif exchange.name=="BitStamp":
        context=[bitstamp_data_retrieval("btc","usd"),bitstamp_data_retrieval("eth","usd"),bitstamp_data_retrieval("bch","usd"),bitstamp_data_retrieval("ltc","usd"),bitstamp_data_retrieval("xrp","usd")]
    elif exchange.name=="Bitsquare":
        context=[bitsquare_data_retrieval("btc","usd")]
    elif exchange.name =="Local Bitcoin":
        context=[localbitcoin_data_retrieval()]
    elif exchange.name=="Gemini":
        context=[gemini_data_retrieval("btc","usd"),gemini_data_retrieval("eth","usd")]
    return HttpResponse(json.dumps(context), content_type="application/json")


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)