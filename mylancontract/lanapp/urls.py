
from django.conf.urls import url
from django.contrib.auth import views as authviews
from lanapp import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^upload/', views.upload, name='upload'),
    url(r'^search_portal', views.search_portal, name='search'),
    url(r'^search/', views.key_search, name='key_search'),
    url(r'^display/', views.display, name='display'),
    url(r'^export/', views.export, name='export'),
    url(r'^clean/', views.clean, name='clean'),
]
