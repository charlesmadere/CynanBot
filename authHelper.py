import json
import os
from typing import List

import requests

from nonceRepository import NonceRepository
from user import User
from userTokensRepository import UserTokensRepository


# The authentication file should be formatted like this:
# {
#    "clientId": "", (taken from "Client ID" at https://dev.twitch.tv/console/apps/)
#    "clientSecret": "", (taken from "Client Secret" at https://dev.twitch.tv/console/apps/)
#    "iqAirApiKey": "", (from https://www.iqair.com/us/dashboard/api)
#    "ircAuthToken": "", (generated from https://twitchapps.com/tmi/),
#    "oneWeatherApiKey": "" (from https://openweathermap.org/)
# }

class AuthHelper():

    def __init__(
        self,
        nonceRepository: NonceRepository,
        authFile: str = 'authFile.json'
    ):
        if nonceRepository == None:
            raise ValueError(f'nonceRepository argument is malformed: \"{nonceRepository}\"')
        elif authFile == None or len(authFile) == 0 or authFile.isspace():
            raise ValueError(f'authFile argument is malformed: \"{authFile}\"')

        self.__nonceRepository = nonceRepository
        self.__authFile = authFile

        if not os.path.exists(authFile):
            raise FileNotFoundError(f'Auth file not found: \"{authFile}\"')

        with open(authFile, 'r') as file:
            jsonContents = json.load(file)

        if jsonContents == None:
            raise IOError(f'Error reading from auth file: \"{authFile}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of auth file ({authFile}) is empty')

        clientId = jsonContents.get('clientId')
        if clientId == None or len(clientId) == 0 or clientId.isspace():
            raise ValueError(f'Auth file ({authFile}) has malformed clientId: \"{clientId}\"')
        self.__clientId = clientId

        clientSecret = jsonContents.get('clientSecret')
        if clientSecret == None or len(clientSecret) == 0 or clientSecret.isspace():
            raise ValueError(f'Auth file ({authFile}) has malformed clientSecret: \"{clientSecret}\"')
        self.__clientSecret = clientSecret

        iqAirApiKey = jsonContents.get('iqAirApiKey')
        if iqAirApiKey == None or len(iqAirApiKey) == 0 or iqAirApiKey.isspace():
            print(f'No value for iqAirApiKey: \"{iqAirApiKey}\"')
        self.__iqAirApiKey = iqAirApiKey

        ircAuthToken = jsonContents.get('ircAuthToken')
        if ircAuthToken == None or len(ircAuthToken) == 0 or ircAuthToken.isspace():
            raise ValueError(f'Auth file ({ircAuthToken}) has malformed ircAuthToken: \"{ircAuthToken}\"')
        self.__ircAuthToken = ircAuthToken

        oneWeatherApiKey = jsonContents.get('oneWeatherApiKey')
        if oneWeatherApiKey == None or len(oneWeatherApiKey) == 0 or oneWeatherApiKey.isspace():
            print(f'No value for oneWeatherApiKey: \"{oneWeatherApiKey}\"')
        self.__oneWeatherApiKey = oneWeatherApiKey

    def getClientId(self):
        return self.__clientId

    def getClientSecret(self):
        return self.__clientSecret

    def getIqAirApiKey(self):
        return self.__iqAirApiKey

    def getIrcAuthToken(self):
        return self.__ircAuthToken

    def getOneWeatherApiKey(self):
        return self.__oneWeatherApiKey

    def __refreshAccessToken(
        self,
        handle: str,
        userTokensRepository: UserTokensRepository
    ):
        if handle == None or len(handle) == 0 or handle.isspace():
            raise ValueError(f'handle argument is malformed: \"{handle}\"')
        elif userTokensRepository == None:
            raise ValueError(f'userTokensRepository argument is malformed: \"{userTokensRepository}\"')

        refreshToken = userTokensRepository.getRefreshToken(handle)

        params = {
            'client_id': self.getClientId(),
            'client_secret': self.getClientSecret(),
            'grant_type': 'refresh_token',
            'refresh_token': refreshToken
        }

        rawResponse = requests.post(
            url = 'https://id.twitch.tv/oauth2/token',
            params = params
        )

        jsonResponse = rawResponse.json()

        if 'access_token' not in jsonResponse or len(jsonResponse['access_token']) == 0:
            raise ValueError(f'Received malformed \"access_token\" for {handle}: {jsonResponse}')
        elif 'refresh_token' not in jsonResponse or len(jsonResponse['refresh_token']) == 0:
            raise ValueError(f'Received malformed \"refresh_token\" for {handle}: {jsonResponse}')

        userTokensRepository.setTokens(
            handle = handle,
            accessToken = jsonResponse['access_token'],
            refreshToken = jsonResponse['refresh_token']
        )

    def validateAndRefreshAccessTokens(
        self,
        users: List[User],
        nonce: str,
        userTokensRepository: UserTokensRepository
    ):
        if userTokensRepository == None:
            raise ValueError(f'userTokensRepository argument is malformed: \"{userTokensRepository}\"')

        if users == None or len(users) == 0:
            print(f'Given an empty list of users, skipping access token validation')
            return

        userTokens = dict()

        for user in users:
            handle = user.getHandle()
            accessToken = userTokensRepository.getAccessToken(handle)

            if accessToken != None and ((nonce == None or len(nonce) == 0 or nonce.isspace()) or nonce == self.__nonceRepository.getNonce(handle)):
                userTokens[handle] = accessToken

        if len(userTokens) == 0:
            print('There are no users with an access token, skipping access token validation')
            return

        print(f'Validating access tokens for {len(userTokens)} user(s) (nonce: \"{nonce}\")...')

        for handle, accessToken in userTokens.items():
            headers = {
                'Authorization': f'OAuth {accessToken}'
            }

            rawResponse = requests.get(
                url = 'https://id.twitch.tv/oauth2/validate',
                headers = headers
            )

            jsonResponse = rawResponse.json()

            if jsonResponse.get('client_id') == None or len(jsonResponse['client_id']) == 0:
                print(f'Refreshing access token for {handle}...')

                self.__refreshAccessToken(
                    handle = handle,
                    userTokensRepository = userTokensRepository
                )
