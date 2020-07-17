import json
import os
import requests

# The channel IDs repository file should be formatted like this:
# {
#   "cynanBot": "",
#   "anotherUser": ""
# }

class ChannelIdsRepository():
    def __init__(self, channelIdsFile: str = 'channelIdsRepository.json'):
        if channelIdsFile == None or len(channelIdsFile) == 0 or channelIdsFile.isspace():
            raise ValueError(f'channelIdsFile argument is malformed: \"{channelIdsFile}\"')

        self.__channelIdsFile = channelIdsFile

    def fetchChannelId(self, handle: str, clientId: str, accessToken: str):
        if handle == None or len(handle) == 0 or handle.isspace():
            raise ValueError(f'handle argument is malformed: \"{handle}\"')
        elif clientId == None or len(clientId) == 0 or clientId.isspace():
            raise ValueError(f'clientId argument is malformed: \"{clientId}\"')
        elif accessToken == None or len(accessToken) == 0 or accessToken.isspace():
            raise ValueError(f'accessToken argument is malformed: \"{accessToken}\"')

        jsonContents = self.__readJson()
        channelId = None

        for key in jsonContents:
            if handle.lower() == key.lower():
                channelId = jsonContents[key]
                break

        if channelId == None or len(channelId) == 0 or channelId.isspace():
            headers = {
                'Client-ID': clientId,
                'Authorization': f'Bearer {accessToken}'
            }

            rawResponse = requests.get(
                url = f'https://api.twitch.tv/helix/users?login={handle}',
                headers = headers
            )

            jsonResponse = json.loads(rawResponse.content)

            if 'error' in jsonResponse and len(jsonResponse['error']) >= 1:
                raise ValueError(f'Received an error when fetching channel ID for {handle}: {jsonResponse}')

            channelId = jsonResponse['data'][0]['id']

            if channelId == None or len(channelId) == 0 or channelId.isspace():
                raise ValueError(f'Unable to fetch channel ID for {handle}: {jsonResponse}')

            self.__setChannelId(
                handle = handle,
                channelId = channelId
            )

        return channelId

    def __readJson(self):
        if not os.path.exists(self.__channelIdsFile):
            return dict()

        with open(self.__channelIdsFile, 'r') as file:
            jsonContents = json.load(file)

        if jsonContents == None:
            raise IOError(f'Error reading from channel IDs file: \"{self.__channelIdsFile}\"')

        return jsonContents

    def __setChannelId(self, handle: str, channelId: str):
        if handle == None or len(handle) == 0 or handle.isspace():
            raise ValueError(f'handle argument is malformed: \"{handle}\"')
        elif channelId == None or len(channelId) == 0 or channelId.isspace():
            raise ValueError(f'channelId argument is malformed: \"{channelId}\"')

        jsonContents = self.__readJson()
        jsonContents[handle] = channelId

        with open(self.__channelIdsFile, 'w') as file:
            json.dump(jsonContents, file, indent = 4, sort_keys = True)

        print(f'Saved new channel ID for {handle}')
