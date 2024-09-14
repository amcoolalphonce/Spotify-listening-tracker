import requests
from django.conf import settings
from django.shortcuts import redirect, render

def index(request):
    return render(request, 'analysis/index.html')


# call back not working still

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
    
    token_url = "https://accounts.spotify/api/token"
    
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


def spotify_profile(request):
    access_token = request.session.get('spotify_token')
    
    if not access_token:
        return redirect('spotify_login')
    
    headers = {
        "Authorization" : f"Bearer {access_token}"
    }
    # this should probabbly work here
    recently_played_url = 'https://api.spotify.com/v1/me/player/recently-played'
    response = requests.get(recently_played_url, headers=headers)
    recent_tracks = response.json().get('items', [])
    
    context = {
        'recent_tracks' : recent_tracks,
    }
    
    return render(request, 'analysis/profile.html')


# to implement now
""""
1. Recently played -- This has benn implemented already.
2. Top artists
3. Top genres
4. Top tracks
5. Total Minutes played 
6. Listening trends 
"""


# Refresh token handling

def refresh_spotify_token(refresh_token):
    token_url = 'https://accounts.spotify.com/api/token'
    payload = {
        "grant_type" : "refresh_token",
        "refresh_token" : refresh_token,
        "client_id" : settings.CLIENT_ID,
        "client_secret" : settings.CLIENT_SECRET,
    }
    response = requests.post(token_url, data = payload)
    return response.json()