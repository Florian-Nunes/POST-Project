from django.shortcuts import render
from django.http import HttpResponse

# Create your views here. MVT = MODEL VIEW TEMPLATE

def homepage(request):
    context = {}
    return render(request, 'index.html', context)

def infrapage(request):
    context = {}
    return render (request, 'index.html', context)