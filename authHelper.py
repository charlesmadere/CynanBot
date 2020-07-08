import json
import os
from user import User

class AuthHelper():
    def __init__(
        self,
        authFile: str = "authFile.json"
    ):
        self.__authFile = authFile

        if not os.path.exists(authFile):
            raise FileNotFoundError(f'Authentication file not found: \"{authFile}\"')

        print(f'Reading authentication file... ({authFile})')

        jsonContents = None
        with open(authFile, 'r') as file:
            jsonContents = json.loads(file)

        clientId = jsonContents['clientId']
        if clientId == None or len(clientId) == 0 or clientId.isspace():
            raise ValueError('Authentication file\'s clientId field is malformed!')
        else:
            self.__clientId = clientId

        clientSecret = jsonContents['clientSecret']
        if clientSecret == None or len(clientSecret) == 0 or clientSecret.isspace():
            raise ValueError('Authentication file\'s clientSecret field is malformed!')
        else:
            self.__clientSecret = clientSecret

        ircAuthToken = jsonContents['ircAuthToken']
        if ircAuthToken == None or len(ircAuthToken) == 0 or ircAuthToken.isspace():
            raise ValueError('Authentication file\'s ircAuthToken field is malformed!')
        else:
            self.__ircAuthToken = ircAuthToken

        users = jsonContents['users']
        if users == None or len(users) == 0:
            raise ValueError('Authentication file\'s users field is malformed!')

        print(f'Finished reading from authentication file')

    def getClientId(self):
        return self.__clientId

    def getClientSecret(self):
        return self.__clientSecret

    def getIrcAuthToken(self):
        return self.__ircAuthToken

    def getUser(self, twitchHandle: str):
        users = self.getUsers()

        for user in users:
            if twitchHandle.lower() == user.twitchHandle.lower():
                return user

        raise RuntimeError(f'Unable to find Twitch User with handle: \"{twitchHandle}\"')

    def getUsers(self):
        jsonContents = None
        with open(self.__authFile, 'r') as file:
            jsonContents = json.loads(file)

        users = []
        for key in jsonContents['users']:
            jsonUser = jsonContents['users'][key]
            user = User(
                twitchHandle = key,
                picOfTheDayFile = jsonUser['picOfTheDayFile'],
                rewardId = jsonUser['rewardId']
            )
            users.append(user)

        return users

    def saveNewCredentials(
        self,
        twitchHandle: str,
        accessToken: str,
        refreshToken: str
    ):
        credentials = {
            'accessToken': accessToken,
            'refreshToken': refreshToken
        }

        jsonContents = None
        with open(self.__authFile, 'r') as file:
            jsonContents = json.loads(file)

        jsonContents['users'][twitchHandle] = credentials

        with open(self.__authFile, 'w') as file:
            json.dump(jsonContents, file, indent = 4, sort_keys = True)
