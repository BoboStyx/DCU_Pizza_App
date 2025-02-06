from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name="homepage"), 
   path('orders', views.order, name="previous_orderspage"),
   path('ordering', views.ordering, name="new_orderpage"),
   path('login', views.login, name="loginpage"),
   path('logout', views.logout, name="logoutpage")
]