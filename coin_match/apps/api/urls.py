from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^cryptocurrency$', views.CryptoCreate.as_view()),
    url(r'^cryptocurrency/(?P<pk>\d+)$', views.CryptoView.as_view()),
    url(r'^exchange$', views.ExchangeCreate.as_view(), name='create'),
    url(r'^exchange/(?P<pk>\d+)$', views.ExchangeView.as_view()),
    url(r'^transaction$', views.TransactionCreate.as_view()),
    url(r'^transaction/(?P<pk>\d+)$', views.TransactionView.as_view()),
    url(r'^users/$', views.UserView.as_view(), name="users"),
    url(r'users/(?P<pk>[0-9]+)/$', views.UserDetailsView.as_view(), name="user_details"),
    url(r'^get-token/', obtain_auth_token),
    url(r'^$', views.index),
    url(r'^cryptocurrency/(?P<pk>\d+)/show$', views.show_crypto),
    url(r'^exchange/(?P<pk>\d+)/show$', views.show_exchange),
]