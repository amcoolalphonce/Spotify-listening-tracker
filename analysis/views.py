import requests
from django.conf import settings
from django.shortcuts import redirect, render

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

def spotify_callback(request):
    code = request.GET.get('code')
    
    token_url = "https//accounts.spotify/api/token"
    
    payload ={
        "grant_type" : "authorization_code",
        "code" : code,
        "redirect_uri" : settings.SPOTIFY_REDIRECT_URI,
        "client_id" : settings.CLIENT_ID,
        "client_secret" : settings.CLIENT_SECRET
    }
    
    response = requests.post(token_url, data = payload)
    token_data = response.json()
    
    access_token = token_data.get('access_token')
    
    request.session['spotify_token'] = access_token # save token to session
    
    return redirect('spotify_profile')