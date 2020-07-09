from channelIdsRepository import ChannelIdsRepository
import json
import os
import requests
from user import User

# The authentication file should be formatted like this:
# {
#    "clientId": "", (taken from "Client ID" at https://dev.twitch.tv/console/apps/)
#    "clientSecret": "", (taken from "Client Secret" at https://dev.twitch.tv/console/apps/)
#    "ircAuthToken": "", (generated from https://twitchapps.com/tmi/)
#    "users": {
#      "cynanBot": {
#        "accessToken": "",
#        "picOfTheDayFile": "",
#        "refreshToken": "",
#        "rewardId": ""
#      }
#    }
# }

class AuthHelper():
    def __init__(
        self,
        channelIdsRepository: ChannelIdsRepository,
        authFile: str = "authFile.json"
    ):
        self.__channelIdsRepository = channelIdsRepository

        if authFile == None or len(authFile) == 0 or authFile.isspace():
            raise ValueError('authFile argument is malformed!')

        self.__authFile = authFile
        jsonContents = self.__readAuthFileJson()

        clientId = jsonContents['clientId']
        if clientId == None or len(clientId) == 0 or clientId.isspace():
            raise ValueError('Authentication file\'s \"clientId\" field is malformed!')
        else:
            self.__clientId = clientId

        clientSecret = jsonContents['clientSecret']
        if clientSecret == None or len(clientSecret) == 0 or clientSecret.isspace():
            raise ValueError('Authentication file\'s \"clientSecret\" field is malformed!')
        else:
            self.__clientSecret = clientSecret

        ircAuthToken = jsonContents['ircAuthToken']
        if ircAuthToken == None or len(ircAuthToken) == 0 or ircAuthToken.isspace():
            raise ValueError('Authentication file\'s \"ircAuthToken\" field is malformed!')
        else:
            self.__ircAuthToken = ircAuthToken

        users = self.__readUsersJson()
        print(f'Finished reading from authentication file ({authFile}). There are {len(users)} user(s).')

    def getAccessToken(self, handle: str):
        if handle == None or len(handle) == 0 or handle.isspace():
            raise ValueError('handle argument is malformed!')

        userJson = self.__readUserJson(handle)

        if 'accessToken' not in userJson:
            raise RuntimeError(f'User \"{handle}\" has no \"accessToken\" in their JSON!')

        accessToken = userJson['accessToken']

        if accessToken == None or len(accessToken) == 0 or accessToken.isspace():
            raise ValueError('User \"{handle}\" has an invalid access token!')

        return accessToken

    def getClientId(self):
        return self.__clientId

    def getClientSecret(self):
        return self.__clientSecret

    def getIrcAuthToken(self):
        return self.__ircAuthToken

    def getRefreshToken(self, handle: str):
        if handle == None or len(handle) == 0 or handle.isspace():
            raise ValueError('handle argument is malformed!')

        userJson = self.__readUserJson(handle)

        if 'refreshToken' not in userJson:
            raise RuntimeError(f'User \"{handle}\" has no \"refreshToken\" in their JSON!')

        refreshToken = userJson['refreshToken']

        if refreshToken == None or len(refreshToken) == 0 or refreshToken.isspace():
            raise ValueError(f'User \"{handle}\" has an invalid refresh token!')

        return refreshToken

    def getUser(self, handle: str):
        if handle == None or len(handle) == 0 or handle.isspace():
            raise ValueError('handle argument is malformed!')

        users = self.getUsers()

        for user in users:
            if handle.lower() == user.getHandle().lower():
                return user

        raise RuntimeError(f'Unable to find user with handle: \"{handle}\"')

    def getUsers(self):
        usersJson = self.__readUsersJson()

        users = []
        for key in usersJson:
            userJson = usersJson[key]
            user = User(
                channelIdsRepository = self.__channelIdsRepository,
                accessToken = userJson['accessToken'],
                handle = key,
                picOfTheDayFile = userJson['picOfTheDayFile'],
                rewardId = userJson['rewardId']
            )
            users.append(user)

        return users

    def __readAuthFileJson(self):
        if not os.path.exists(self.__authFile):
            raise FileNotFoundError(f'Authentication file not found: \"{self.__authFile}\"')

        with open(self.__authFile, 'r') as file:
            jsonContents = json.load(file)

        if jsonContents == None:
            raise IOError(f'Error reading from authentication file: \"{self.__authFile}\"')

        return jsonContents

    def __readUserJson(self, handle: str):
        usersJson = self.__readUsersJson()

        for key in usersJson:
            if handle.lower() == key.lower():
                return usersJson[key]

        raise RuntimeError(f'Unable to find user with handle: \"{handle}\"')

    def __readUsersJson(self):
        jsonContents = self.__readAuthFileJson()

        if 'users' not in jsonContents:
            raise ValueError('Authentication file\'s \"users\" field is missing!')
        elif len(jsonContents['users']) == 0:
            raise ValueError('Authentication file\'s \"users\" field is empty!')

        return jsonContents['users']

    def refreshAccessTokens(self):
        jsonContents = self.__readAuthFileJson()
        usersJson = jsonContents['users']

        for handle in usersJson:
            params = {
                'client_id': self.getClientId(),
                'client_secret': self.getClientSecret(),
                'grant_type': 'refresh_token',
                'refresh_token': usersJson['refreshToken']
            }

            rawResponse = requests.post(
                url = 'https://id.twitch.tv/oauth2/token',
                params = params
            )

            jsonResponse = json.loads(rawResponse.content)

            if 'access_token' not in jsonResponse or len(jsonResponse['access_token'] == 0):
                raise ValueError(f'Received malformed \"access_token\" for {handle}: {rawResponse}')
            elif 'refresh_token' not in jsonResponse or len(jsonResponse['refresh_token'] == 0):
                raise ValueError(f'Received malformed \"refresh_token\" for {handle}: {rawResponse}')

            usersJson[handle]['accessToken'] = jsonResponse['access_token']
            usersJson[handle]['refreshToken'] = jsonResponse['refresh_token']

        with open(self.__authFile, 'w') as file:
            json.dump(jsonContents, file, indent = 4, sort_keys = True)

    def validateAccessTokens(self):
        users = self.getUsers()

        for user in users:
            headers = {
                'Authorization': f'OAuth {user.getAccessToken()}'
            }

            rawResponse = requests.get(
                url = 'https://id.twitch.tv/oauth2/validate',
                headers = headers
            )

            jsonResponse = json.loads(rawResponse.content)

            if 'client_id' not in jsonResponse or len(jsonResponse['client_id']) == 0:
                raise ValueError(f'Received malformed \"client_id\" for {user}: {rawResponse}')
