# products/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('home', views1.index, name='index'),
    path('cart/', views1.cart, name='cart')
]