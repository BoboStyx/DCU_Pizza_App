from django.urls import path
from .views import SignUpView
from . import views


urlpatterns = [
   path('', views.index, name="homepage"), 
   path('ordering', views.ordering, name="new_orderpage"),
   path('cart', views.cart, name='cart'),
   path('login', views.login, name="loginpage"),
   path('payment', views.payment, name='payment'),
   path('signup', SignUpView.as_view(), name='signup'),
]