from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name="homepage"), 
   path('orders', views.about, name="previous_orders")
]