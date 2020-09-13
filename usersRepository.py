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

        isAnalogueEnabled = self.__readJsonBoolean(userJson, 'analogueEnabled')
        isDeWordOfTheDayEnabled = self.__readJsonBoolean(userJson, 'deWordOfTheDayEnabled')
        isEnEsWordOfTheDayEnabled = self.__readJsonBoolean(userJson, 'enEsWordOfTheDayEnabled')
        isEnPtWordOfTheDayEnabled = self.__readJsonBoolean(userJson, 'enPtWordOfTheDayEnabled')
        isEsWordOfTheDayEnabled = self.__readJsonBoolean(userJson, 'esWordOfTheDayEnabled')
        isFrWordOfTheDayEnabled = self.__readJsonBoolean(userJson, 'frWordOfTheDayEnabled')
        isItWordOfTheDayEnabled = self.__readJsonBoolean(userJson, 'itWordOfTheDayEnabled')
        isJaWordOfTheDayEnabled = self.__readJsonBoolean(userJson, 'jaWordOfTheDayEnabled')
        isKoWordOfTheDayEnabled = self.__readJsonBoolean(userJson, 'koWordOfTheDayEnabled')
        isNoWordOfTheDayEnabled = self.__readJsonBoolean(userJson, 'noWordOfTheDayEnabled')
        isPicOfTheDayEnabled = self.__readJsonBoolean(userJson, 'picOfTheDayEnabled')
        isPtWordOfTheDayEnabled = self.__readJsonBoolean(userJson, 'ptWordOfTheDayEnabled')
        isRuWordOfTheDayEnabled = self.__readJsonBoolean(userJson, 'ruWordOfTheDayEnabled')
        isSvWordOfTheDayEnabled = self.__readJsonBoolean(userJson, 'svWordOfTheDayEnabled')
        isZhWordOfTheDayEnabled = self.__readJsonBoolean(userJson, 'zhWordOfTheDayEnabled')

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
            timeZone = self.__timeZoneRepository.getTimeZone(userJson['timeZone'])

        return User(
            isAnalogueEnabled = isAnalogueEnabled,
            isDeWordOfTheDayEnabled = isDeWordOfTheDayEnabled,
            isEnEsWordOfTheDayEnabled = isEnEsWordOfTheDayEnabled,
            isEnPtWordOfTheDayEnabled = isEnPtWordOfTheDayEnabled,
            isEsWordOfTheDayEnabled = isEsWordOfTheDayEnabled,
            isFrWordOfTheDayEnabled = isFrWordOfTheDayEnabled,
            isItWordOfTheDayEnabled = isItWordOfTheDayEnabled,
            isJaWordOfTheDayEnabled = isJaWordOfTheDayEnabled,
            isKoWordOfTheDayEnabled = isKoWordOfTheDayEnabled,
            isNoWordOfTheDayEnabled = isNoWordOfTheDayEnabled,
            isPicOfTheDayEnabled = isPicOfTheDayEnabled,
            isPtWordOfTheDayEnabled = isPtWordOfTheDayEnabled,
            isRuWordOfTheDayEnabled = isRuWordOfTheDayEnabled,
            isSvWordOfTheDayEnabled = isSvWordOfTheDayEnabled,
            isZhWordOfTheDayEnabled = isZhWordOfTheDayEnabled,
            discord = discord,
            handle = handle,
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

    def __readJsonBoolean(self, userJson: dict, key: str, defaultValue: bool = False):
        if userJson == None:
            raise ValueError(f'userJson argument is malformed: \"{userJson}\"')
        elif key == None or len(key) == 0 or key.isspace():
            raise ValueError(f'key argument is malformed: \"{key}\"')
        elif key in userJson and userJson[key] != None:
            return userJson[key]
        else:
            return defaultValue
