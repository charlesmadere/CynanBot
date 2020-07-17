import json
import os

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

    def getChannelId(self, handle: str):
        if handle == None or len(handle) == 0 or handle.isspace():
            raise ValueError(f'handle argument is malformed: \"{handle}\"')

        jsonContents = self.__readChannelIdsFileJson()
        channelId = None

        for key in jsonContents:
            if handle.lower() == key.lower():
                channelId = jsonContents[key]
                break

        if channelId == None or len(channelId) == 0 or channelId.isspace():
            return None
        else:
            return channelId

    def __readChannelIdsFileJson(self):
        if not os.path.exists(self.__channelIdsFile):
            return dict()

        with open(self.__channelIdsFile, 'r') as file:
            jsonContents = json.load(file)

        if jsonContents == None:
            raise IOError(f'Error reading from channel IDs file: \"{self.__channelIdsFile}\"')

        return jsonContents

    def setChannelId(self, handle: str, channelId: str):
        if handle == None or len(handle) == 0 or handle.isspace():
            raise ValueError(f'handle argument is malformed: \"{handle}\"')
        elif channelId == None or len(channelId) == 0 or channelId.isspace():
            raise ValueError(f'channelId argument is malformed: \"{channelId}\"')

        jsonContents = self.__readChannelIdsFileJson()
        jsonContents[handle] = channelId

        with open(self.__channelIdsFile, 'w') as file:
            json.dump(jsonContents, file, indent = 4, sort_keys = True)

        print(f'Saved new channel ID ({channelId}) for {handle}')
