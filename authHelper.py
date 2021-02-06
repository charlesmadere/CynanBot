import json
import os
from typing import List

import requests

import CynanBotCommon.utils as utils
from CynanBotCommon.nonceRepository import NonceRepository
from user import User
from userTokensRepository import UserTokensRepository


class AuthHelper():

    def __init__(
        self,
        nonceRepository: NonceRepository,
        authFile: str = 'authFile.json',
        oauth2TokenUrl: str = 'https://id.twitch.tv/oauth2/token',
        oauth2ValidateUrl: str = 'https://id.twitch.tv/oauth2/validate'
    ):
        if nonceRepository is None:
            raise ValueError(f'nonceRepository argument is malformed: \"{nonceRepository}\"')
        elif not utils.isValidStr(authFile):
            raise ValueError(f'authFile argument is malformed: \"{authFile}\"')
        elif not utils.isValidUrl(oauth2TokenUrl):
            raise ValueError(f'oauth2TokenUrl argument is malformed: \"{oauth2TokenUrl}\"')
        elif not utils.isValidUrl(oauth2ValidateUrl):
            raise ValueError(f'oauth2ValidateUrl argument is malformed: \"{oauth2ValidateUrl}\"')

        self.__nonceRepository = nonceRepository
        self.__authFile = authFile
        self.__oauth2TokenUrl = oauth2TokenUrl
        self.__oauth2ValidateUrl = oauth2ValidateUrl

        if not os.path.exists(authFile):
            raise FileNotFoundError(f'Auth file not found: \"{authFile}\"')

        with open(authFile, 'r') as file:
            jsonContents = json.load(file)

        if jsonContents is None:
            raise IOError(f'Error reading from auth file: \"{authFile}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of auth file \"{authFile}\" is empty')

        clientId = jsonContents.get('clientId')
        if not utils.isValidStr(clientId):
            raise ValueError(f'Auth file ({authFile}) has malformed clientId: \"{clientId}\"')
        self.__clientId = clientId

        clientSecret = jsonContents.get('clientSecret')
        if not utils.isValidStr(clientSecret):
            raise ValueError(f'Auth file ({authFile}) has malformed clientSecret: \"{clientSecret}\"')
        self.__clientSecret = clientSecret

        iqAirApiKey = jsonContents.get('iqAirApiKey')
        if not utils.isValidStr(iqAirApiKey):
            print(f'No value for iqAirApiKey: \"{iqAirApiKey}\"')
        self.__iqAirApiKey = iqAirApiKey

        ircAuthToken = jsonContents.get('ircAuthToken')
        if not utils.isValidStr(ircAuthToken):
            raise ValueError(f'Auth file ({ircAuthToken}) has malformed ircAuthToken: \"{ircAuthToken}\"')
        self.__ircAuthToken = ircAuthToken

        oneWeatherApiKey = jsonContents.get('oneWeatherApiKey')
        if not utils.isValidStr(oneWeatherApiKey):
            print(f'No value for oneWeatherApiKey: \"{oneWeatherApiKey}\"')
        self.__oneWeatherApiKey = oneWeatherApiKey

    def getClientId(self) -> str:
        return self.__clientId

    def getClientSecret(self) -> str:
        return self.__clientSecret

    def getIqAirApiKey(self) -> str:
        return self.__iqAirApiKey

    def getIrcAuthToken(self) -> str:
        return self.__ircAuthToken

    def getOneWeatherApiKey(self) -> str:
        return self.__oneWeatherApiKey

    def __refreshAccessToken(
        self,
        handle: str,
        userTokensRepository: UserTokensRepository
    ):
        if not utils.isValidStr(handle):
            raise ValueError(f'handle argument is malformed: \"{handle}\"')
        elif userTokensRepository is None:
            raise ValueError(f'userTokensRepository argument is malformed: \"{userTokensRepository}\"')

        refreshToken = userTokensRepository.getRefreshToken(handle)

        params = {
            'client_id': self.getClientId(),
            'client_secret': self.getClientSecret(),
            'grant_type': 'refresh_token',
            'refresh_token': refreshToken
        }

        rawResponse = requests.post(
            url=self.__oauth2TokenUrl,
            params=params
        )

        jsonResponse = rawResponse.json()

        if 'access_token' not in jsonResponse or len(jsonResponse['access_token']) == 0:
            raise ValueError(f'Received malformed \"access_token\" for {handle}: {jsonResponse}')
        elif 'refresh_token' not in jsonResponse or len(jsonResponse['refresh_token']) == 0:
            raise ValueError(f'Received malformed \"refresh_token\" for {handle}: {jsonResponse}')

        userTokensRepository.setTokens(
            handle=handle,
            accessToken=jsonResponse['access_token'],
            refreshToken=jsonResponse['refresh_token']
        )

    def validateAndRefreshAccessTokens(
        self,
        users: List[User],
        nonce: str,
        userTokensRepository: UserTokensRepository
    ):
        if userTokensRepository is None:
            raise ValueError(f'userTokensRepository argument is malformed: \"{userTokensRepository}\"')

        if not utils.hasItems(users):
            print(f'Given an empty list of users, skipping access token validation')
            return

        userTokens = dict()

        for user in users:
            handle = user.getHandle()
            accessToken = userTokensRepository.getAccessToken(handle)

            if accessToken is not None and (not utils.isValidStr(nonce) or nonce == self.__nonceRepository.getNonce(handle)):
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
                url=self.__oauth2ValidateUrl,
                headers=headers,
                timeout=utils.getDefaultTimeout()
            )

            jsonResponse = rawResponse.json()

            if jsonResponse.get('client_id') is None or len(jsonResponse['client_id']) == 0:
                print(f'Refreshing access token for {handle}...')

                self.__refreshAccessToken(
                    handle=handle,
                    userTokensRepository=userTokensRepository
                )
