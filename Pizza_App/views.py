from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

def index(request):
    return render(request, 'index.html')

def ordering(request):
    return render(request, "ordering.html")

def login(request):
    return render(request, 'login.html',)

def payment(request):
    return render(request, 'payment.html')

def cart(request):
    return render(request, 'cart.html')

def signup(request):
    return render(request, 'signup.html')

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/login.html"