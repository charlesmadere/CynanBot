import json
import os

import CynanBotCommon.utils as utils


class UserTokensRepository():

    def __init__(self, userTokensFile: str = 'userTokensRepository.json'):
        if not utils.isValidStr(userTokensFile):
            raise ValueError(f'userTokensFile argument is malformed: \"{userTokensFile}\"')

        self.__userTokensFile = userTokensFile

    def getAccessToken(self, handle: str) -> str:
        userJson = self.__readJsonForHandle(handle)

        if userJson is None:
            return None
        elif 'accessToken' not in userJson:
            raise ValueError(f'JSON for {handle} is missing \"accessToken\": {userJson}')

        accessToken = userJson['accessToken']

        if not utils.isValidStr(accessToken):
            raise ValueError(f'accessToken for {handle} is malformed: \"{accessToken}\"')

        return accessToken

    def getRefreshToken(self, handle: str) -> str:
        userJson = self.__readJsonForHandle(handle)

        if userJson is None:
            raise RuntimeError(f'No user token JSON for {handle} found')
        elif 'refreshToken' not in userJson:
            raise ValueError(f'JSON for {handle} is missing \"refreshToken\": {userJson}')

        refreshToken = userJson['refreshToken']

        if not utils.isValidStr(refreshToken):
            raise ValueError(f'refreshToken for {handle} is malformed: \"{refreshToken}\"')

        return refreshToken

    def __readJson(self) -> dict:
        if not os.path.exists(self.__userTokensFile):
            raise FileNotFoundError(f'User tokens file not found: \"{self.__userTokensFile}\"')

        with open(self.__userTokensFile, 'r') as file:
            jsonContents = json.load(file)

        if jsonContents is None:
            raise IOError(f'Error reading from user tokens file: \"{self.__userTokensFile}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of user tokens file \"{self.__userTokensFile}\" is empty')

        return jsonContents

    def __readJsonForHandle(self, handle: str) -> dict:
        if not utils.isValidStr(handle):
            raise ValueError(f'handle argument is malformed: \"{handle}\"')

        jsonContents = self.__readJson()

        for key in jsonContents:
            if handle.lower() == key.lower():
                return jsonContents[key]

        return None

    def setTokens(self, handle: str, accessToken: str, refreshToken: str):
        if not utils.isValidStr(handle):
            raise ValueError(f'handle argument is malformed: \"{handle}\"')
        elif not utils.isValidStr(accessToken):
            raise ValueError(f'accessToken argument is malformed: \"{accessToken}\"')
        elif not utils.isValidStr(refreshToken):
            raise ValueError(f'refreshToken argument is malformed: \"{refreshToken}\"')

        if not os.path.exists(self.__userTokensFile):
            raise FileNotFoundError(f'User tokens file not found: \"{self.__userTokensFile}\"')

        with open(self.__userTokensFile, 'r') as file:
            jsonContents = json.load(file)

        if jsonContents is None:
            raise IOError(f'Error reading from user tokens file: \"{self.__userTokensFile}\"')

        jsonContents[handle] = {
            'accessToken': accessToken,
            'refreshToken': refreshToken
        }

        with open(self.__userTokensFile, 'w') as file:
            json.dump(jsonContents, file, indent = 4, sort_keys = True)

        print(f'Saved new user tokens for {handle}')
