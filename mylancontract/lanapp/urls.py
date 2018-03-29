
from django.conf.urls import url
from django.contrib.auth import views as authviews
from lanapp import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload/', views.upload, name='upload'),
    url(r'^search_portal', views.search_portal, name='search'),
    url(r'^search/', views.key_search, name='key_search'),
    url(r'^display/', views.display, name='display'),
    url(r'^export/', views.export, name='export'),
    url(r'^clean/', views.clean, name='clean'),
    url(r'^upload_contract/', views.upload_contract, name='upload_contract'),
    url(r'^show_contracts/', views.show_contracts, name='show_contracts'),
    url(r'^delete_contract/(?P<id>.+)$', views.delete_contract, name='delete_contract'),
    url(r'^get_contract/(?P<id>.+)$', views.get_contract, name='get_contract'),
    url(r'^delete_all_contract/', views.delete_all_contract, name='delete_all_contract'),
]
