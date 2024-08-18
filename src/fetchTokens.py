from typing import Any

import requests

# This file is meant to be run separately from the others in this repository. It retrieves some
# important keys / tokens that are required in order for some Twitch-related functionaly in
# CynanBot and CynanBotDiscord to authenticate with Twitch and run properly.
#
# So before you even run CynanBot itself, you are required to first run this script. Then, you can
# use the output information you've received to build up the information in the secretKeys.py and
# users.py files.

# taken from "Client ID" at https://dev.twitch.tv/console/apps/
TWITCH_CLIENT_ID: str | None = None

# taken from "Client Secret" at https://dev.twitch.tv/console/apps/
TWITCH_CLIENT_SECRET: str | None = None

# This code is derived from clicking this URL and then authenticating:
# https://id.twitch.tv/oauth2/authorize?response_type=code&client_id=CLIENT_ID_HERE&redirect_uri=http://localhost&scope=channel:bot+chat:read+user:read:chat+user:bot+user:write:chat+chat:edit+channel_editor+channel:read:redemptions+channel:manage:redemptions+channel:read:subscriptions+channel:read:polls+channel:read:predictions+channel:manage:predictions+channel_subscriptions+moderator:read:chatters+user:read:chat+bits:read+moderator:read:followers+moderator:manage:banned_users+channel:manage:moderators+moderation:read+channel:manage:polls+user:read:subscriptions
TWITCH_CODE_SECRET: str | None = None

if not isinstance(TWITCH_CLIENT_SECRET, str) or not isinstance(TWITCH_CLIENT_SECRET, str) or not isinstance(TWITCH_CODE_SECRET, str):
    raise ValueError(f'All variables must be set: {TWITCH_CLIENT_ID=}, {TWITCH_CLIENT_SECRET=}, {TWITCH_CODE_SECRET=}')

url = f'https://id.twitch.tv/oauth2/token?client_id={TWITCH_CLIENT_ID}&client_secret={TWITCH_CLIENT_SECRET}&code={TWITCH_CODE_SECRET}&grant_type=authorization_code&redirect_uri=http://localhost'
print(f'Contacting Twitch API URL: \"{url}\"...')

jsonResponse: dict[str, Any] | None = None

try:
    rawResponse = requests.post(url)
    jsonResponse = rawResponse.json()
except BaseException as e:
    print(f'Encountered exception ({e=}) ({TWITCH_CLIENT_ID=}) ({TWITCH_CLIENT_SECRET=}) ({TWITCH_CODE_SECRET=}) ({jsonResponse=})')

if isinstance(jsonResponse, dict):
    accessToken: str | None = jsonResponse.get('access_token', None)
    refreshToken: str | None = jsonResponse.get('refresh_token', None)

    print(f'Twitch accessToken: \"{accessToken}\"')
    print(f'Twitch refreshToken: \"{refreshToken}\"')
    print('\n\n\n')
    print('===========================')
    print('==== Begin Twitch JSON ====')
    print('===========================')
    print(str(jsonResponse))
    print('===========================')
    print('===== End Twitch JSON =====')
    print('===========================')
else:
    print(f'jsonResponse is unknown type: \"{jsonResponse}\"')
