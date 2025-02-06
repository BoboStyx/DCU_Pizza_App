from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name="homepage"), 
   path('past/orders', views.order, name="previous_orders"),
   path('order', views.ordering, name="new_order")
]