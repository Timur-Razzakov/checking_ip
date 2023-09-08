from django.urls import path

from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('add_params/', add_params_view, name='add_params'),
    path('add_country/', add_country_view, name='add_country'),
    path('add_url/', add_url_view, name='add_url'),
    path('get_all_urls/', show_data_view, name='get_all_urls'),
    path('get/', check_url_view, name='myurl')
]
