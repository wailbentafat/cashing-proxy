

from django.urls import path
from . import views

urlpatterns = [
    path('<path:path>', views.proxy, name='proxy'), 
    path('clear-cache/', views.clear_cache, name='clear_cache'),  
]

