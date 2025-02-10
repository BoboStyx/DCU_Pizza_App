from django.shortcuts import render, redirect, get_object_or_404
from django.http import request
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from .forms import PizzaForm, PaymentForm, AddressForm
from .models import Orders, Pizza, Cart
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'index.html')

def ordering(request):
    return render(request, "ordering.html")

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('previous_orders')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {"form": form})

def payment(request):
    return render(request, 'payment.html')

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    pizzas = cart.pizzas.all()
    total = cart.total_price()

    if request.method == "POST":
        return redirect("payment")
    return render(request, 'cart.html', {"cart": cart, "pizzas": pizzas, 'total': total})

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect("order")
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {"form": form})