# three/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.three_view, name='three_view'),
]