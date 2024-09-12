from django.shortcuts import render
import requests
from django.conf import settings
from django.shortcuts import redirect

def index(request):
    return render(request, 'analysis/index.html')

def spotify_login(request):
    scope = 'user-read-recently-played user-top-read'
    auth_url = 'https://accounts.spotify.com/authorize'
    
    params = {
        "client_id" : settings.CLIENT_ID,
        "response_type" : "code",
        "redirect_uri" : settings.SPOTIFY_REDIRECT_URI,
        "scope" : scope,
    }
    
    url = f"{auth_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"
    return redirect(url)