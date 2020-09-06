import json
import os
from timeZoneRepository import TimeZoneRepository
from user import User

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

            isAnalogueEnabled = False
            if 'analogueEnabled' in userJson:
                isAnalogueEnabled = userJson['analogueEnabled']

            isEsWordOfTheDayEnabled = False
            if 'esWordOfTheDayEnabled' in userJson:
                isEsWordOfTheDayEnabled = userJson['esWordOfTheDayEnabled']

            isJaWordOfTheDayEnabled = False
            if 'jaWordOfTheDayEnabled' in userJson:
                isJaWordOfTheDayEnabled = userJson['jaWordOfTheDayEnabled']

            isPicOfTheDayEnabled = False
            if 'picOfTheDayEnabled' in userJson:
                isPicOfTheDayEnabled = userJson['picOfTheDayEnabled']

            isZhWordOfTheDayEnabled = False
            if 'zhWordOfTheDayEnabled' in userJson:
                isZhWordOfTheDayEnabled = userJson['zhWordOfTheDayEnabled']

            discord = None
            if 'discord' in userJson:
                discord = userJson['discord']

            picOfTheDayFile = None
            if isPicOfTheDayEnabled:
                if 'picOfTheDayFile' in userJson:
                    picOfTheDayFile = userJson['picOfTheDayFile']

                if picOfTheDayFile == None or len(picOfTheDayFile) == 0 or picOfTheDayFile.isspace():
                    raise ValueError(f'POTD is enabled for {handle} but picOfTheDayFile is malformed: \"{picOfTheDayFile}\"')

            picOfTheDayRewardId = None
            if 'picOfTheDayRewardId' in userJson:
                picOfTheDayRewardId = userJson['picOfTheDayRewardId']

            speedrunProfile = None
            if 'speedrunProfile' in userJson:
                speedrunProfile = userJson['speedrunProfile']

            twitter = None
            if 'twitter' in userJson:
                twitter = userJson['twitter']

            timeZone = None
            if 'timeZone' in userJson:
                timeZone = userJson['timeZone']

            users.append(User(
                isAnalogueEnabled = isAnalogueEnabled,
                isEsWordOfTheDayEnabled = isEsWordOfTheDayEnabled,
                isJaWordOfTheDayEnabled = isJaWordOfTheDayEnabled,
                isPicOfTheDayEnabled = isPicOfTheDayEnabled,
                isZhWordOfTheDayEnabled = isZhWordOfTheDayEnabled,
                discord = discord,
                handle = handle,
                picOfTheDayFile = picOfTheDayFile,
                picOfTheDayRewardId = picOfTheDayRewardId,
                speedrunProfile = speedrunProfile,
                twitter = twitter,
                timeZone = self.__timeZoneRepository.getTimeZone(timeZone)
            ))

        if len(users) == 0:
            raise RuntimeError(f'Unable to read in any users from users file: \"{self.__usersFile}\"')

        return users
