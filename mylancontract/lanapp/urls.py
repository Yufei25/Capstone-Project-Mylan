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
    url(r'^test/', views.test, name='test'),
    url(r'^upload_contract/', views.upload_contract, name='upload_contract'),
    url(r'^show_contracts/', views.show_contracts, name='show_contracts'),
    url(r'^delete_contract/(?P<id>.+)$', views.delete_contract, name='delete_contract'),
    url(r'^get_contract/(?P<id>.+)$', views.get_contract, name='get_contract'),
    url(r'^delete_all_contract/', views.delete_all_contract, name='delete_all_contract'),

    # url(r'^search/', views.get_contract_display, name='get_contract_display'),
    url(r'^get_current_contract/(?P<contract_id>\d+)', views.get_current_contract, name='get_current_contract'),

    url(r'^get-changes/?$', views.get_changes),
    url(r'^get-changes/(?P<time>.+)$', views.get_changes),
    # url(r'^contract-upload', views.contract_upload),
    # url(r'^show_contracts_test', views.show_contracts_test, name='show_contracts_test'),
    url(r'^contract-comment/(?P<contract_id>\d+)$', views.contract_comment),
    url(r'^content-comment/(?P<content_id>\d+)$', views.content_comment),
    url(r'^warning-comment/(?P<warning_id>\d+)$', views.warning_comment),
    # url(r'^content-comment/(?P<contract_id>\d+)$', views.content_comment),
    # url(r'^warning-comment/(?P<contract_id>\d+)$', views.warning_comment),
    url(r'^get-contract-comments-changes/(?P<contract_id>\d+)/(?P<time>.+)$', views.get_contract_comments_changes),
    url(r'^get-contents-changes/(?P<contract_id>\d+)/(?P<time>.+)$', views.get_contents_changes),
    url(r'^get-warnings-changes/(?P<contract_id>\d+)/(?P<time>.+)$', views.get_warnings_changes),

    url(r'^get-content-comments-changes/(?P<content_id>\d+)/(?P<time>.+)$', views.get_content_comments_changes),
    url(r'^get-warning-comments-changes/(?P<warning_id>\d+)/(?P<time>.+)$', views.get_warning_comments_changes),
    url(r'^about/', views.about, name='about'),
]
