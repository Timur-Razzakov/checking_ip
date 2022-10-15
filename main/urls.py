from django.urls import path

from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('add_params/', add_params_view, name='add_params'),
    path('get_all_urls/', show_data_view, name='get_all_urls'),
    path('<str:url>/', check_url_view, name='myurl')
]
