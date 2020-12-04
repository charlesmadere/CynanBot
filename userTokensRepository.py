import json
import os


class UserTokensRepository():

    def __init__(self, userTokensFile: str = 'userTokensRepository.json'):
        if userTokensFile is None or len(userTokensFile) == 0 or userTokensFile.isspace():
            raise ValueError(
                f'userTokens argument is malformed: \"{userTokensFile}\"')

        self.__userTokensFile = userTokensFile

    def getAccessToken(self, handle: str):
        userJson = self.__readJson(handle)

        if userJson is None:
            return None
        elif 'accessToken' not in userJson:
            raise ValueError(
                f'JSON for {handle} is missing \"accessToken\": {userJson}')

        accessToken = userJson['accessToken']

        if accessToken is None or len(accessToken) == 0 or accessToken.isspace():
            raise ValueError(
                f'accessToken for {handle} is malformed: \"{accessToken}\"')

        return accessToken

    def getRefreshToken(self, handle: str):
        userJson = self.__readJson(handle)

        if userJson is None:
            raise RuntimeError(f'No user token JSON for {handle} found')
        elif 'refreshToken' not in userJson:
            raise ValueError(
                f'JSON for {handle} is missing \"refreshToken\": {userJson}')

        refreshToken = userJson['refreshToken']

        if refreshToken is None or len(refreshToken) == 0 or refreshToken.isspace():
            raise ValueError(
                f'refreshToken for {handle} is malformed: \"{refreshToken}\"')

        return refreshToken

    def __readJson(self, handle: str):
        if handle is None or len(handle) == 0 or handle.isspace():
            raise ValueError(f'handle argument is malformed: \"{handle}\"')

        if not os.path.exists(self.__userTokensFile):
            raise FileNotFoundError(
                f'User tokens file not found: \"{self.__userTokensFile}\"')

        with open(self.__userTokensFile, 'r') as file:
            jsonContents = json.load(file)

        if jsonContents is None:
            raise IOError(
                f'Error reading from user tokens file: \"{self.__userTokensFile}\"')

        for key in jsonContents:
            if handle.lower() == key.lower():
                return jsonContents[key]

        return None

    def setTokens(self, handle: str, accessToken: str, refreshToken: str):
        if handle is None or len(handle) == 0 or handle.isspace():
            raise ValueError(f'handle argument is malformed: \"{handle}\"')
        elif accessToken is None or len(accessToken) == 0 or accessToken.isspace():
            raise ValueError(
                f'accessToken argument is malformed: \"{accessToken}\"')
        elif refreshToken is None or len(refreshToken) == 0 or refreshToken.isspace():
            raise ValueError(
                f'refreshToken argument is malformed: \"{refreshToken}\"')

        if not os.path.exists(self.__userTokensFile):
            raise FileNotFoundError(
                f'User tokens file not found: \"{self.__userTokensFile}\"')

        with open(self.__userTokensFile, 'r') as file:
            jsonContents = json.load(file)

        if jsonContents is None:
            raise IOError(
                f'Error reading from user tokens file: \"{self.__userTokensFile}\"')

        jsonContents[handle] = {
            'accessToken': accessToken,
            'refreshToken': refreshToken
        }

        with open(self.__userTokensFile, 'w') as file:
            json.dump(jsonContents, file, indent=4, sort_keys=True)

        print(f'Saved new user tokens for {handle}')
