import json
import os

class ChannelIdsRepository():
    def __init__(self, repositoryFile: str = "channelIds.json"):
        if repositoryFile == None or len(repositoryFile) == 0 or repositoryFile.isspace():
            raise ValueError('repositoryFile argument is malformed!')

        self.__repositoryFile = repositoryFile

    def getChannelId(self, handle: str):
        if handle == None or len(handle) == 0 or handle.isspace():
            raise ValueError('handle argument is malformed!')

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
        if not os.path.exists(self.__repositoryFile):
            return dict()

        jsonContents = None

        with open(self.__repositoryFile, 'r') as file:
            jsonContents = json.loads(file)

        if jsonContents == None:
            raise IOError(f'Error reading from channel IDs file: \"{self.__repositoryFile}\"')

        return jsonContents

    def setChannelId(self, handle: str, channelId: str):
        if handle == None or len(handle) == 0 or handle.isspace():
            raise ValueError('handle argument is malformed!')
        elif channelId == None or len(channelId) == 0 or channelId.isspace():
            raise ValueError('channelId argument is malformed!')

        jsonContents = self.__readChannelIdsFileJson()
        jsonContents[handle] = channelId

        with open(self.__repositoryFile, 'w') as file:
            json.dump(jsonContents, file, indent = 4, sort_keys = True)

        print(f'Saved new {handle} channel ID')
