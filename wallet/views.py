from tkinter.font import names

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
@api_view()
def welcome(request):
    return Response("Welcome to EaziPay")

def greeting(request, name):
    return HttpResponse(f"Hello,{name}")

def second_greeting(request, name):
    return render(request, 'hello.html', {'name': name})
