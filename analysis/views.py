from django.shortcuts import render
import requests
from django.conf import settings
from django.shortcuts import redirect

def index(request):
    return render(request, 'analysis/index.html')