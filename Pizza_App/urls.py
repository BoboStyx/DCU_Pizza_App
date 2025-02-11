from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('order/', views.ordering, name='order'),
    path('payment/', views.payment, name='payment'),
    path('completed_order/order<int:order_id>', views.order_complete, name='completed_order'),
    path('logout/', LogoutView.as_view(next_page="/"), name="logout"),
    path('pizza_cart/', views.cart, name="cart"),
    path('cart/remove/order#<int:pizza_id>/',views.removed_from_cart, name='removed_from_cart'),
]