from django.http import request
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PizzaForms, PaymentForms, AddressForms
from .models import Pizza, Order, Cart
from django.contrib.auth.decorators import login_required

def index(request):
    current_user = request.user
    orders = Order.objects.filter(user=current_user).order_by("-id")
    return render(request, 'index.html', {"user": current_user, "orders": orders})

def ordering(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == "POST":
        form = PizzaForms(request.POST)
        if form.is_valid():
            pizza = form.save()
            cart, creation = Cart.objects.get_or_create(user=request.user)
            cart.pizzas.add(pizza)

            return redirect('cart')
    else:
        form = PizzaForms()
    return render(request, 'ordering.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {"form": form})

@login_required
def cart(request):
    cart, creation = Cart.objects.get_or_create(user=request.user)
    All_pizzas = cart.pizzas.all()
    total = cart.total_price()

    if request.method == "POST":
        return redirect("payment")
    return render(request, 'cart.html', {"cart": cart, "pizzas": All_pizzas, 'total': total})

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect("order")
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {"form": form})

@login_required
def removed_from_cart(request, pizza_id):
    cart = get_object_or_404(Cart, user=request.user)  
    pizza = get_object_or_404(Pizza, id=pizza_id)  
    if cart.user != request.user:
        return redirect('/')

    if cart.pizzas.filter(id=pizza.id).exists():
        cart.pizzas.remove(pizza)
        pizza.delete()

    return redirect('cart')

@login_required
def payment(request):
    cart = get_object_or_404(Cart, user=request.user)
    pizzas = cart.pizzas.all()

    if request.method == "POST":
        payment_forms = PaymentForms(request.POST)
        address_forms = AddressForms(request.POST)
        
        if payment_forms.is_valid() and address_forms.is_valid():

            address = address_forms.save()
            order = Order.objects.create(user=request.user, address=address)
            order.pizza.set(pizzas)
            order.save()

            cart.pizzas.clear()
            return redirect('completed_order', order.id)
    else:
        payment_forms = PaymentForms()
        address_forms = AddressForms()
    return render(request, 'payment.html', {"payment": payment_forms, "address": address_forms})

@login_required
def order_complete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.user != request.user:
        return redirect('/')
    return render(request, 'completed_order.html', {"order": order})