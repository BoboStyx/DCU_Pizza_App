from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def order(request):
    return render(request, 'orders.html')

def ordering(request):
    return render(request, "ordering.html")