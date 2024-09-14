import requests
from django.conf import settings

code = requests.get('code')
response = requests.post('https://accounts.spotify.com/api/token', data =
                         {'grant_type' : 'authorization_code',
                          'code' : code,
                          'redirect_uri' : settings.SPOTIFY_REDIRECT_URI,
                          'client_id' : settings.CLIENT_ID,
                          'client_secret' : settings.CLIENT_SECRET
                          })