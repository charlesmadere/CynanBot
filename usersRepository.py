import json
import os

# The users repository file should be formatted like this:
# {
#   "cynanBot": {
#     "picOfTheDayFile": "",
#     "rewardId": "",
#     "timeZone": ""
#   },
#   "anotherUser": {
#     // ...
#   }
# }

class UsersRepository():
    def __init__(self, usersFile: str = 'usersRepository.json'):
        if usersFile == None or len(usersFile) == 0 or usersFile.isspace():
            raise ValueError(f'usersFile argument is malformed: \"{usersFile}\"')

        self.__usersFile = usersFile

    def getUser(self, handle: str):
        if handle == None or len(handle) == 0 or handle.isspace():
            raise ValueError(f'handle argument is malformed: \"{handle}\"')

        users = self.getUsers()

        for user in users:
            if handle.lower() == user.getHandle().lower():
                return user

        raise RuntimeError(f'Unable to find user with handle: \"{handle}\"')

    def getUsers(self):
        if not os.path.exists(self.__usersFile):
            raise FileNotFoundError(f'Users file not found: \"{self.__usersFile}\"')

        with open(self.__usersFile, 'r') as file:
            jsonContents = json.load(file)

        if jsonContents == None:
            raise IOError(f'Error reading from users file: \"{self.__usersFile}\"')

        users = []
        for handle in jsonContents:
            user = User(
                picOfTheDayFile = jsonContents[handle]['picOfTheDayFile'],
                rewardId = jsonContents[handle]['rewardId'],
                timeZone = jsonContents[handle]['timeZone']
            )
            users.append(user)

        if len(users) == 0:
            raise RuntimeError(f'Unable to read in any users from users file: \"{self.__usersFile}\"')

        return users
