from typing import Any, Dict, Optional

import requests

# This file is meant to be run separately from the others in this repository. It retrieves some
# important keys / tokens that are required in order for some Twitch-related functionaly in
# CynanBot and CynanBotDiscord to authenticate with Twitch and run properly.
#
# So before you even run CynanBot itself, you are required to first run this script. Then, you can
# use the output information you've received to build up the information in the secretKeys.py and
# users.py files.

# taken from "Client ID" at https://dev.twitch.tv/console/apps/
TWITCH_CLIENT_ID: Optional[str] = None

# taken from "Client Secret" at https://dev.twitch.tv/console/apps/
TWITCH_CLIENT_SECRET: Optional[str] = None

# This code is derived from clicking this URL and then authenticating:
# https://id.twitch.tv/oauth2/authorize?response_type=code&client_id=CLIENT_ID_HERE&redirect_uri=http://localhost&scope=channel:bot+chat:read+user:read:chat+user:bot+user:write:chat+chat:edit+channel:moderate+whispers:read+whispers:edit+channel_editor+channel:read:redemptions+channel:manage:redemptions+channel:read:subscriptions+channel:read:polls+channel:read:predictions+channel:manage:predictions+moderator:read:chatters+user:read:chat+bits:read+moderator:read:followers+moderation:read+moderator:manage:banned_users+channel:manage:moderators+moderation:read
TWITCH_CODE_SECRET: Optional[str] = None

if not isinstance(TWITCH_CLIENT_SECRET, str) or not isinstance(TWITCH_CLIENT_SECRET, str) or not isinstance(TWITCH_CODE_SECRET, str):
    raise ValueError(f'All variables must be set: {TWITCH_CLIENT_ID=}, {TWITCH_CLIENT_SECRET=}, {TWITCH_CODE_SECRET=}')

url = f'https://id.twitch.tv/oauth2/token?client_id={TWITCH_CLIENT_ID}&client_secret={TWITCH_CLIENT_SECRET}&code={TWITCH_CODE_SECRET}&grant_type=authorization_code&redirect_uri=http://localhost'

jsonResponse: Optional[Dict[str, Any]] = None

try:
    rawResponse = requests.post(url)
    jsonResponse = rawResponse.json()
except Exception as e:
    print(f'Encountered exception ({e=}) ({TWITCH_CLIENT_ID=}) ({TWITCH_CLIENT_SECRET}) ({TWITCH_CODE_SECRET=})')

print(f'All Twitch JSON: {jsonResponse}')

if jsonResponse is not None:    
    accessToken: Optional[str] = jsonResponse.get('access_token')
    refreshToken: Optional[str] = jsonResponse.get('refresh_token')
    print(f'Twitch accessToken: \"{accessToken}\"')
    print(f'Twitch refreshToken: \"{refreshToken}\"')
