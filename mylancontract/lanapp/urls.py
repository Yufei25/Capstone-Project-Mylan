
from django.conf.urls import url
from django.contrib.auth import views as authviews
from lanapp import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^search/', views.key_search, name='key_search'),
]
