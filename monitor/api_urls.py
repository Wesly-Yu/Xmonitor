from django.urls import path,re_path
from monitor import views

urlpatterns = [
    re_path('^client/config/(\d+)/$',views.client_config),
    re_path('^client/service/report/$',views.service_report),
]
