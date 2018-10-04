from django.conf.urls import url

from . import views


app_name = 'locations'

urlpatterns = [
    url(r'^hotels/$', views.hotels, name='hotels'),
    url(r'^cities/$', views.cities, name='cities'),
    url(r'^(?P<city_name>\w+)/$', views.city, name='city'),
]