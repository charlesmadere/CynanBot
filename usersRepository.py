import json
import os
from typing import Dict, List

import CynanBotCommon.utils as utils
from cutenessBoosterPack import CutenessBoosterPack
from CynanBotCommon.timeZoneRepository import TimeZoneRepository
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

        self.__timeZoneRepository: TimeZoneRepository = timeZoneRepository
        self.__usersFile: str = usersFile

    def __createUser(self, handle: str, userJson: dict) -> User:
        if not utils.isValidStr(handle):
            raise ValueError(f'handle argument is malformed: \"{handle}\"')
        elif not utils.hasItems(userJson):
            raise ValueError(f'userJson argument is empty or malformed: \"{userJson}\"')

        isAnalogueEnabled = userJson.get('analogueEnabled', False)
        isCatJamEnabled = userJson.get('catJamEnabled', False)
        isChatBandEnabled = userJson.get('chatBandEnabled', False)
        isCutenessEnabled = userJson.get('cutenessEnabled', False)
        isDiccionarioEnabled = userJson.get('diccionarioEnabled', False)
        isGiveCutenessEnabled = userJson.get('giveCutenessEnabled', False)
        isJishoEnabled = userJson.get('jishoEnabled', False)
        isJokesEnabled = userJson.get('jokesEnabled', False)
        isLocalTriviaRepositoryEnabled = userJson.get('localTriviaRepositoryEnabled', False)
        isPicOfTheDayEnabled = userJson.get('picOfTheDayEnabled', False)
        isPkmnEnabled = userJson.get('pkmnEnabled', False)
        isPokepediaEnabled = userJson.get('pokepediaEnabled', False)
        isRaceEnabled = userJson.get('raceEnabled', False)
        isRaidLinkMessagingEnabled = userJson.get('raidLinkMessagingEnabled', False)
        isRatJamEnabled = userJson.get('ratJamEnabled', False)
        isRewardIdPrintingEnabled = userJson.get('rewardIdPrintingEnabled', False)
        isStarWarsQuotesEnabled = userJson.get('starWarsQuotesEnabled', False)
        isTamalesEnabled = userJson.get('tamalesEnabled', False)
        isTranslateEnabled = userJson.get('translateEnabled', False)
        isTriviaEnabled = userJson.get('triviaEnabled', False)
        isTriviaGameEnabled = userJson.get('triviaGameEnabled', False)
        isWeatherEnabled = userJson.get('weatherEnabled', False)
        isWordOfTheDayEnabled = userJson.get('wordOfTheDayEnabled', False)
        discord = userJson.get('discord')
        instagram = userJson.get('instagram')
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
        cutenessBoosterPacks = None
        if isCutenessEnabled:
            increaseCutenessDoubleRewardId = userJson.get('increaseCutenessDoubleRewardId')
            cutenessBoosterPacksJson = userJson.get('cutenessBoosterPacks')

            if utils.hasItems(cutenessBoosterPacksJson):
                cutenessBoosterPacks: List[CutenessBoosterPack] = list()

                for cutenessBoosterPackJson in cutenessBoosterPacksJson:
                    cutenessBoosterPacks.append(CutenessBoosterPack(
                        amount = utils.getIntFromDict(cutenessBoosterPackJson, 'amount'),
                        rewardId = utils.getStrFromDict(cutenessBoosterPackJson, 'rewardId')
                    ))

                cutenessBoosterPacks.sort(key = lambda pack: pack.getAmount())

        picOfTheDayFile = None
        picOfTheDayRewardId = None
        if isPicOfTheDayEnabled:
            picOfTheDayFile = userJson.get('picOfTheDayFile')
            picOfTheDayRewardId = userJson.get('picOfTheDayRewardId')

            if not utils.isValidStr(picOfTheDayFile):
                raise ValueError(f'POTD is enabled for {handle} but picOfTheDayFile is malformed: \"{picOfTheDayFile}\"')

        triviaGameRewardId = None
        triviaGamePoints = None
        waitForTriviaAnswerDelay = None
        if isTriviaGameEnabled:
            triviaGameRewardId = userJson.get('triviaGameRewardId')
            triviaGamePoints = userJson.get('triviaGamePoints')
            waitForTriviaAnswerDelay = userJson.get('waitForTriviaAnswerDelay')

        pkmnBattleRewardId = None
        pkmnCatchRewardId = None
        pkmnEvolveRewardId = None
        pkmnShinyRewardId = None
        if isPkmnEnabled:
            pkmnBattleRewardId = userJson.get('pkmnBattleRewardId')
            pkmnCatchRewardId = userJson.get('pkmnCatchRewardId')
            pkmnEvolveRewardId = userJson.get('pkmnEvolveRewardId')
            pkmnShinyRewardId = userJson.get('pkmnShinyRewardId')

        return User(
            isAnalogueEnabled = isAnalogueEnabled,
            isCatJamEnabled = isCatJamEnabled,
            isChatBandEnabled = isChatBandEnabled,
            isCutenessEnabled = isCutenessEnabled,
            isDiccionarioEnabled = isDiccionarioEnabled,
            isGiveCutenessEnabled = isGiveCutenessEnabled,
            isJishoEnabled = isJishoEnabled,
            isJokesEnabled = isJokesEnabled,
            isLocalTriviaRepositoryEnabled = isLocalTriviaRepositoryEnabled,
            isPicOfTheDayEnabled = isPicOfTheDayEnabled,
            isPkmnEnabled = isPkmnEnabled,
            isPokepediaEnabled = isPokepediaEnabled,
            isRaceEnabled = isRaceEnabled,
            isRaidLinkMessagingEnabled = isRaidLinkMessagingEnabled,
            isRatJamEnabled = isRatJamEnabled,
            isRewardIdPrintingEnabled = isRewardIdPrintingEnabled,
            isStarWarsQuotesEnabled = isStarWarsQuotesEnabled,
            isTamalesEnabled = isTamalesEnabled,
            isTranslateEnabled = isTranslateEnabled,
            isTriviaEnabled = isTriviaEnabled,
            isTriviaGameEnabled = isTriviaGameEnabled,
            isWeatherEnabled = isWeatherEnabled,
            isWordOfTheDayEnabled = isWordOfTheDayEnabled,
            triviaGamePoints = triviaGamePoints,
            waitForTriviaAnswerDelay = waitForTriviaAnswerDelay,
            discord = discord,
            handle = handle,
            increaseCutenessDoubleRewardId = increaseCutenessDoubleRewardId,
            instagram = instagram,
            locationId = locationId,
            picOfTheDayFile = picOfTheDayFile,
            picOfTheDayRewardId = picOfTheDayRewardId,
            pkmnBattleRewardId = pkmnBattleRewardId,
            pkmnCatchRewardId = pkmnCatchRewardId,
            pkmnEvolveRewardId = pkmnEvolveRewardId,
            pkmnShinyRewardId = pkmnShinyRewardId,
            speedrunProfile = speedrunProfile,
            triviaGameRewardId = triviaGameRewardId,
            twitter = twitter,
            cutenessBoosterPacks = cutenessBoosterPacks,
            timeZones = timeZones
        )

    def getUser(self, handle: str) -> User:
        if not utils.isValidStr(handle):
            raise ValueError(f'handle argument is malformed: \"{handle}\"')

        jsonContents = self.__readJson()

        for key in jsonContents:
            if handle.lower() == key.lower():
                return self.__createUser(handle, jsonContents[key])

        raise RuntimeError(f'Unable to find user with handle \"{handle}\" in users file: \"{self.__usersFile}\"')

    def getUsers(self) -> List[User]:
        jsonContents = self.__readJson()

        users: List[User] = list()
        for key in jsonContents:
            user = self.__createUser(key, jsonContents[key])
            users.append(user)

        if not utils.hasItems(users):
            raise RuntimeError(f'Unable to read in any users from users file: \"{self.__usersFile}\"')

        users.sort(key = lambda user: user.getHandle().lower())
        return users

    def __readJson(self) -> Dict:
        if not os.path.exists(self.__usersFile):
            raise FileNotFoundError(f'Users file not found: \"{self.__usersFile}\"')

        with open(self.__usersFile, 'r') as file:
            jsonContents = json.load(file)

        if jsonContents is None:
            raise IOError(f'Error reading from users file: \"{self.__usersFile}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of users file \"{self.__usersFile}\" is empty')

        return jsonContents
