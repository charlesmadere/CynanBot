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
        if timeZoneRepository == None:
            raise ValueError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif usersFile == None or len(usersFile) == 0 or usersFile.isspace():
            raise ValueError(f'usersFile argument is malformed: \"{usersFile}\"')

        self.__timeZoneRepository = timeZoneRepository
        self.__usersFile = usersFile

    def __createUser(self, handle: str, userJson: dict):
        if handle == None or len(handle) == 0 or handle.isspace():
            raise ValueError(f'handle argument is malformed: \"{handle}\"')
        elif userJson == None:
            raise ValueError(f'userJson argument is malformed: \"{userJson}\"')
        elif len(userJson) == 0:
            raise ValueError(f'userJson argument is empty: \"{userJson}\"')

        isAnalogueEnabled = userJson.get('analogueEnabled', False)
        isCatJamEnabled = userJson.get('catJamEnabled', False)
        isCutenessEnabled = userJson.get('cutenessEnabled', False)
        isGiveCutenessEnabled = userJson.get('giveCutenessEnabled', False)
        isJishoEnabled = userJson.get('jishoEnabled', False)
        isJokesEnabled = userJson.get('jokesEnabled', False)
        isPicOfTheDayEnabled = userJson.get('picOfTheDayEnabled', False)
        isWordOfTheDayEnabled = userJson.get('wordOfTheDayEnabled', False)

        discord = userJson.get('discord')

        increaseCutenessDoubleRewardId = None
        increaseCutenessRewardId = None
        if isCutenessEnabled:
            increaseCutenessDoubleRewardId = userJson.get('increaseCutenessDoubleRewardId')
            increaseCutenessRewardId = userJson.get('increaseCutenessRewardId')

        locationId = userJson.get('locationId')

        picOfTheDayFile = None
        picOfTheDayRewardId = None
        if isPicOfTheDayEnabled:
            picOfTheDayFile = userJson.get('picOfTheDayFile')
            picOfTheDayRewardId = userJson.get('picOfTheDayRewardId')

            if picOfTheDayFile == None or len(picOfTheDayFile) == 0 or picOfTheDayFile.isspace():
                raise ValueError(f'POTD is enabled for {handle} but picOfTheDayFile is malformed: \"{picOfTheDayFile}\"')

        speedrunProfile = userJson.get('speedrunProfile')
        twitter = userJson.get('twitter')
        timeZone = self.__timeZoneRepository.getTimeZone(userJson.get('timeZone'))

        return User(
            isAnalogueEnabled = isAnalogueEnabled,
            isCatJamEnabled = isCatJamEnabled,
            isCutenessEnabled = isCutenessEnabled,
            isGiveCutenessEnabled = isGiveCutenessEnabled,
            isJishoEnabled = isJishoEnabled,
            isJokesEnabled = isJokesEnabled,
            isPicOfTheDayEnabled = isPicOfTheDayEnabled,
            isWordOfTheDayEnabled = isWordOfTheDayEnabled,
            discord = discord,
            handle = handle,
            increaseCutenessDoubleRewardId = increaseCutenessDoubleRewardId,
            increaseCutenessRewardId = increaseCutenessRewardId,
            locationId = locationId,
            picOfTheDayFile = picOfTheDayFile,
            picOfTheDayRewardId = picOfTheDayRewardId,
            speedrunProfile = speedrunProfile,
            twitter = twitter,
            timeZone = timeZone
        )

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
            users.append(self.__createUser(handle, userJson))

        if len(users) == 0:
            raise RuntimeError(f'Unable to read in any users from users file: \"{self.__usersFile}\"')

        return users
