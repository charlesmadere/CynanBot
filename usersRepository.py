import json
import os

import utils
from timeZoneRepository import TimeZoneRepository
from user import User


class UsersRepository():

    def __init__(
        self,
        timeZoneRepository: TimeZoneRepository,
        usersFile: str = 'usersRepository.json'
    ):
        if timeZoneRepository is None:
            raise ValueError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not utils.isValidStr(usersFile):
            raise ValueError(f'usersFile argument is malformed: \"{usersFile}\"')

        self.__timeZoneRepository = timeZoneRepository
        self.__usersFile = usersFile

    def __createUser(self, handle: str, userJson: dict):
        if not utils.isValidStr(handle):
            raise ValueError(f'handle argument is malformed: \"{handle}\"')
        elif userJson is None:
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
        isPkmnEnabled = userJson.get('pkmnEnabled', False)
        isWordOfTheDayEnabled = userJson.get('wordOfTheDayEnabled', False)
        discord = userJson.get('discord')
        locationId = userJson.get('locationId')
        speedrunProfile = userJson.get('speedrunProfile')
        twitter = userJson.get('twitter')

        timeZones = None
        if 'timeZones' in userJson:
            timeZones = self.__timeZoneRepository.getTimeZones(userJson['timeZones'])
        elif 'timeZone' in userJson:
            timeZones = list()
            timeZones.append(self.__timeZoneRepository.getTimeZone(userJson['timeZone']))

        increaseCutenessDoubleRewardId = None
        increaseCutenessRewardId = None
        if isCutenessEnabled:
            increaseCutenessDoubleRewardId = userJson.get('increaseCutenessDoubleRewardId')
            increaseCutenessRewardId = userJson.get('increaseCutenessRewardId')

        picOfTheDayFile = None
        picOfTheDayRewardId = None
        if isPicOfTheDayEnabled:
            picOfTheDayFile = userJson.get('picOfTheDayFile')
            picOfTheDayRewardId = userJson.get('picOfTheDayRewardId')

            if not utils.isValidStr(picOfTheDayFile):
                raise ValueError(f'POTD is enabled for {handle} but picOfTheDayFile is malformed: \"{picOfTheDayFile}\"')

        pkmnEvolveRewardId = None
        pkmnShinyRewardId = None
        if isPkmnEnabled:
            pkmnEvolveRewardId = userJson.get('pkmnEvolveRewardId')
            pkmnShinyRewardId = userJson.get('pkmnShinyRewardId')

        return User(
            isAnalogueEnabled=isAnalogueEnabled,
            isCatJamEnabled=isCatJamEnabled,
            isCutenessEnabled=isCutenessEnabled,
            isGiveCutenessEnabled=isGiveCutenessEnabled,
            isJishoEnabled=isJishoEnabled,
            isJokesEnabled=isJokesEnabled,
            isPicOfTheDayEnabled=isPicOfTheDayEnabled,
            isPkmnEnabled=isPkmnEnabled,
            isWordOfTheDayEnabled=isWordOfTheDayEnabled,
            discord=discord,
            handle=handle,
            increaseCutenessDoubleRewardId=increaseCutenessDoubleRewardId,
            increaseCutenessRewardId=increaseCutenessRewardId,
            locationId=locationId,
            picOfTheDayFile=picOfTheDayFile,
            picOfTheDayRewardId=picOfTheDayRewardId,
            pkmnEvolveRewardId=pkmnEvolveRewardId,
            pkmnShinyRewardId=pkmnShinyRewardId,
            speedrunProfile=speedrunProfile,
            twitter=twitter,
            timeZones=timeZones
        )

    def getUser(self, handle: str):
        if not utils.isValidStr(handle):
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

        if jsonContents is None:
            raise IOError(f'Error reading from users file: \"{self.__usersFile}\"')

        users = []
        for handle in jsonContents:
            userJson = jsonContents[handle]
            users.append(self.__createUser(handle, userJson))

        if len(users) == 0:
            raise RuntimeError(f'Unable to read in any users from users file: \"{self.__usersFile}\"')

        return users
