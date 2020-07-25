import json
import os
from timeZoneRepository import TimeZoneRepository
from user import User

# The users repository file should be formatted like this:
# {
#   "cynanBot": {
#     "picOfTheDayFile": "",
#     "picOfTheDayRewardId": "",
#     "timeZone": ""
#   },
#   "anotherUser": {
#     // ...
#   }
# }

class UsersRepository():
    def __init__(
        self,
        timeZoneRepository: TimeZoneRepository,
        usersFile: str = 'usersRepository.json'
    ):
        if usersFile == None or len(usersFile) == 0 or usersFile.isspace():
            raise ValueError(f'usersFile argument is malformed: \"{usersFile}\"')
        elif timeZoneRepository == None:
            raise ValueError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__usersFile = usersFile
        self.__timeZoneRepository = timeZoneRepository

    def getUser(self, handle: str):
        if handle == None or len(handle) == 0 or handle.isspace():
            raise ValueError(f'handle argument is malformed: \"{handle}\"')

        users = self.getUsers()

        for user in users:
            if handle.lower() == user.getHandle().lower():
                return user

        raise RuntimeError(f'Unable to find user with handle \"{handle}\" in users file: \"{self.__usersFile}\"')

    def getUsers(self):
        if not os.path.exists(self.__usersFile):
            raise FileNotFoundError(f'Users file not found: \"{self.__usersFile}\"')

        with open(self.__usersFile, 'r') as file:
            jsonContents = json.load(file)

        if jsonContents == None:
            raise IOError(f'Error reading from users file: \"{self.__usersFile}\"')

        users = []
        for handle in jsonContents:
            userJson = jsonContents[handle]

            picOfTheDayRewardId = None
            if 'picOfTheDayRewardId' in userJson:
                picOfTheDayRewardId = userJson['picOfTheDayRewardId']

            timeZone = None
            if 'timeZone' in userJson:
                timeZone = userJson['timeZone']

            users.append(User(
                handle = handle,
                picOfTheDayFile = userJson['picOfTheDayFile'],
                picOfTheDayRewardId = picOfTheDayRewardId,
                timeZone = self.__timeZoneRepository.getTimeZone(timeZone)
            ))

        if len(users) == 0:
            raise RuntimeError(f'Unable to read in any users from users file: \"{self.__usersFile}\"')

        return users
