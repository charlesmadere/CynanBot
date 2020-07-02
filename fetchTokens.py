import json
import requests

CLIENT_ID = None
CLIENT_SECRET = None

# This code is derived from clicking this URL and then authenticating:
# https://id.twitch.tv/oauth2/authorize?response_type=code&client_id=CLIENT_ID_HERE&redirect_uri=http://localhost&scope=chat:read+chat:edit+channel:moderate+whispers:read+whispers:edit+channel_editor+channel:read:redemptions
CODE_SECRET = None

url = f'https://id.twitch.tv/oauth2/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&code={CODE_SECRET}&grant_type=authorization_code&redirect_uri=http://localhost'
r = requests.post(url)
print(r.content)
