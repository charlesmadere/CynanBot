import json
import os
from typing import Dict, List

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

    def getIqAirApiKey(self) -> str:
        jsonContents = self.__readJson()
        return jsonContents.get('iqAirApiKey')

    def getMerriamWebsterApiKey(self) -> str:
        jsonContents = self.__readJson()
        return jsonContents.get('merriamWebsterApiKey')

    def getOneWeatherApiKey(self) -> str:
        jsonContents = self.__readJson()
        return jsonContents.get('oneWeatherApiKey')

    def __readJson(self) -> Dict:
        if not os.path.exists(self.__authFile):
            raise FileNotFoundError(f'Auth file not found: \"{self.__authFile}\"')

        with open(self.__authFile, 'r') as file:
            jsonContents = json.load(file)

        if jsonContents is None:
            raise IOError(f'Error reading from auth file: \"{self.__authFile}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of auth file \"{self.__authFile}\" is empty')

        return jsonContents

    def requireIqAirApiKey(self) -> str:
        iqAirApiKey = self.getIqAirApiKey()

        if not utils.isValidStr(iqAirApiKey):
            raise ValueError(f'\"iqAirApiKey\" in auth file \"{self.__authFile}\" is malformed: \"{iqAirApiKey}\"')

        return iqAirApiKey

    def requireMerriamWebsterApiKey(self) -> str:
        merriamWebsterApiKey = self.getMerriamWebsterApiKey()

        if not utils.isValidStr(merriamWebsterApiKey):
            raise ValueError(f'\"merriamWebsterApiKey\" in auth file \"{self.__authFile}\" is malformed: \"{merriamWebsterApiKey}\"')

        return merriamWebsterApiKey

    def requireOneWeatherApiKey(self) -> str:
        oneWeatherApiKey = self.getOneWeatherApiKey()

        if not utils.isValidStr(oneWeatherApiKey):
            raise ValueError(f'\"oneWeatherApiKey\" in auth file \"{self.__authFile}\" is malformed: \"{oneWeatherApiKey}\"')

        return oneWeatherApiKey

    def requireTwitchClientId(self) -> str:
        jsonContents = self.__readJson()

        twitchClientId = jsonContents.get('twitchClientId')
        if not utils.isValidStr(twitchClientId):
            raise ValueError(f'\"twitchClientId\" in auth file \"{self.__authFile}\" is malformed: \"{twitchClientId}\"')

        return twitchClientId

    def requireTwitchIrcAuthToken(self) -> str:
        jsonContents = self.__readJson()

        twitchIrcAuthToken = jsonContents.get('twitchIrcAuthToken')
        if not utils.isValidStr(twitchIrcAuthToken):
            raise ValueError(f'\"twitchIrcAuthToken\" in auth file \"{self.__authFile}\" is malformed: \"{twitchIrcAuthToken}\"')

        return twitchIrcAuthToken

    def requireTwitchClientSecret(self) -> str:
        jsonContents = self.__readJson()

        twitchClientSecret = jsonContents.get('twitchClientSecret')
        if not utils.isValidStr(twitchClientSecret):
            raise ValueError(f'\"twitchClientSecret\" in auth file \"{self.__authFile}\" is malformed: \"{twitchClientSecret}\"')

        return twitchClientSecret

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
            'client_id': self.requireTwitchClientId(),
            'client_secret': self.requireTwitchClientSecret(),
            'grant_type': 'refresh_token',
            'refresh_token': refreshToken
        }

        rawResponse = requests.post(
            url = self.__oauth2TokenUrl,
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
        if userTokensRepository is None:
            raise ValueError(f'userTokensRepository argument is malformed: \"{userTokensRepository}\"')

        if not utils.hasItems(users):
            print(f'Given an empty list of users, skipping access token validation')
            return

        userTokens = dict()

        for user in users:
            handle = user.getHandle()
            accessToken = userTokensRepository.getAccessToken(handle)

            if utils.isValidStr(accessToken):
                if utils.isValidStr(nonce):
                    if nonce == self.__nonceRepository.getNonce(handle):
                        userTokens[handle] = accessToken
                else:
                    userTokens[handle] = accessToken

        if not utils.hasItems(userTokens):
            print('There are no users with an access token, skipping access token validation')
            return

        print(f'Validating access tokens for {len(userTokens)} user(s) (nonce: \"{nonce}\")...')

        for handle, accessToken in userTokens.items():
            rawResponse = requests.get(
                url = self.__oauth2ValidateUrl,
                headers = {
                    'Authorization': f'OAuth {accessToken}'
                },
                timeout = utils.getDefaultTimeout()
            )

            jsonResponse = rawResponse.json()

            if jsonResponse.get('client_id') is None or len(jsonResponse['client_id']) == 0:
                print(f'Refreshing access token for \"{handle}\"...')

                self.__refreshAccessToken(
                    handle = handle,
                    userTokensRepository = userTokensRepository
                )
