import json
import os
from typing import Dict, List

import CynanBotCommon.utils as utils
from cuteness.cutenessBoosterPack import CutenessBoosterPack
from CynanBotCommon.timeZoneRepository import TimeZoneRepository
from pkmn.pkmnCatchBoosterPack import PkmnCatchBoosterPack
from pkmn.pkmnCatchType import PkmnCatchType

from user.user import User


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

        isAnalogueEnabled = utils.getBoolFromDict(userJson, 'analogueEnabled', False)
        isCatJamEnabled = utils.getBoolFromDict(userJson, 'catJamEnabled', False)
        isChatBandEnabled = utils.getBoolFromDict(userJson, 'chatBandEnabled', False)
        isCutenessEnabled = utils.getBoolFromDict(userJson, 'cutenessEnabled', False)
        isCynanMessageEnabled = utils.getBoolFromDict(userJson, 'cynanMessageEnabled', False)
        isCynanSourceEnabled = utils.getBoolFromDict(userJson, 'cynanSourceEnabled', True)
        isDeerForceMessageEnabled = utils.getBoolFromDict(userJson, 'deerForceMessageEnabled', False)
        isGiveCutenessEnabled = utils.getBoolFromDict(userJson, 'giveCutenessEnabled', False)
        isJamCatEnabled = utils.getBoolFromDict(userJson, 'jamCatEnabled', False)
        isJishoEnabled = utils.getBoolFromDict(userJson, 'jishoEnabled', False)
        isJokesEnabled = utils.getBoolFromDict(userJson, 'jokesEnabled', False)
        isLocalTriviaRepositoryEnabled = utils.getBoolFromDict(userJson, 'localTriviaRepositoryEnabled', False)
        isPicOfTheDayEnabled = utils.getBoolFromDict(userJson, 'picOfTheDayEnabled', False)
        isPkmnEnabled = utils.getBoolFromDict(userJson, 'pkmnEnabled', False)
        isPokepediaEnabled = utils.getBoolFromDict(userJson, 'pokepediaEnabled', False)
        isRaceEnabled = utils.getBoolFromDict(userJson, 'raceEnabled', False)
        isRaidLinkMessagingEnabled = utils.getBoolFromDict(userJson, 'raidLinkMessagingEnabled', False)
        isRatJamEnabled = utils.getBoolFromDict(userJson, 'ratJamEnabled', False)
        isRewardIdPrintingEnabled = utils.getBoolFromDict(userJson, 'rewardIdPrintingEnabled', False)
        isStarWarsQuotesEnabled = utils.getBoolFromDict(userJson, 'starWarsQuotesEnabled', False)
        isTamalesEnabled = utils.getBoolFromDict(userJson, 'tamalesEnabled', False)
        isTranslateEnabled = utils.getBoolFromDict(userJson, 'translateEnabled', False)
        isTriviaEnabled = utils.getBoolFromDict(userJson, 'triviaEnabled', False)
        isTriviaGameEnabled = utils.getBoolFromDict(userJson, 'triviaGameEnabled', False)
        isWeatherEnabled = utils.getBoolFromDict(userJson, 'weatherEnabled', False)
        isWordOfTheDayEnabled = utils.getBoolFromDict(userJson, 'wordOfTheDayEnabled', False)
        discord: str = userJson.get('discord')
        instagram: str = userJson.get('instagram')
        locationId: str = userJson.get('locationId')
        speedrunProfile: str = userJson.get('speedrunProfile')
        twitter: str = userJson.get('twitter')

        timeZones = None
        if 'timeZones' in userJson:
            timeZones = self.__timeZoneRepository.getTimeZones(userJson['timeZones'])
        elif 'timeZone' in userJson:
            timeZones = list()
            timeZones.append(self.__timeZoneRepository.getTimeZone(userJson['timeZone']))

        increaseCutenessDoubleRewardId: str = None
        cutenessBoosterPacks: List[CutenessBoosterPack] = None
        if isCutenessEnabled:
            increaseCutenessDoubleRewardId = userJson.get('increaseCutenessDoubleRewardId')
            cutenessBoosterPacksJson = userJson.get('cutenessBoosterPacks')
            cutenessBoosterPacks = self.__parseCutenessBoosterPacksFromJson(cutenessBoosterPacksJson)

        picOfTheDayFile: str = None
        picOfTheDayRewardId: str = None
        if isPicOfTheDayEnabled:
            picOfTheDayFile = userJson.get('picOfTheDayFile')
            picOfTheDayRewardId = userJson.get('picOfTheDayRewardId')

            if not utils.isValidStr(picOfTheDayFile):
                raise ValueError(f'POTD is enabled for {handle} but picOfTheDayFile is malformed: \"{picOfTheDayFile}\"')

        triviaGameRewardId: str = None
        triviaGamePoints: int = None
        triviaGameTutorialCutenessThreshold: int = None
        waitForTriviaAnswerDelay: int = None
        if isTriviaGameEnabled:
            triviaGameRewardId = userJson.get('triviaGameRewardId')
            triviaGamePoints = userJson.get('triviaGamePoints')
            triviaGameTutorialCutenessThreshold = userJson.get('triviaGameTutorialCutenessThreshold')
            waitForTriviaAnswerDelay = userJson.get('waitForTriviaAnswerDelay')

        pkmnBattleRewardId: str = None
        pkmnEvolveRewardId: str = None
        pkmnShinyRewardId: str = None
        pkmnCatchBoosterPacks: List[PkmnCatchBoosterPack] = None
        if isPkmnEnabled:
            pkmnBattleRewardId = userJson.get('pkmnBattleRewardId')
            pkmnEvolveRewardId = userJson.get('pkmnEvolveRewardId')
            pkmnShinyRewardId = userJson.get('pkmnShinyRewardId')
            pkmnCatchBoosterPacksJson = userJson.get('pkmnCatchBoosterPacks')
            pkmnCatchBoosterPacks = self.__parsePkmnCatchBoosterPacksFromJson(pkmnCatchBoosterPacksJson)

        return User(
            isAnalogueEnabled = isAnalogueEnabled,
            isCatJamEnabled = isCatJamEnabled,
            isChatBandEnabled = isChatBandEnabled,
            isCutenessEnabled = isCutenessEnabled,
            isCynanMessageEnabled = isCynanMessageEnabled,
            isCynanSourceEnabled = isCynanSourceEnabled,
            isDeerForceMessageEnabled = isDeerForceMessageEnabled,
            isGiveCutenessEnabled = isGiveCutenessEnabled,
            isJamCatEnabled = isJamCatEnabled,
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
            triviaGameTutorialCutenessThreshold = triviaGameTutorialCutenessThreshold,
            waitForTriviaAnswerDelay = waitForTriviaAnswerDelay,
            discord = discord,
            handle = handle,
            increaseCutenessDoubleRewardId = increaseCutenessDoubleRewardId,
            instagram = instagram,
            locationId = locationId,
            picOfTheDayFile = picOfTheDayFile,
            picOfTheDayRewardId = picOfTheDayRewardId,
            pkmnBattleRewardId = pkmnBattleRewardId,
            pkmnEvolveRewardId = pkmnEvolveRewardId,
            pkmnShinyRewardId = pkmnShinyRewardId,
            speedrunProfile = speedrunProfile,
            triviaGameRewardId = triviaGameRewardId,
            twitter = twitter,
            cutenessBoosterPacks = cutenessBoosterPacks,
            pkmnCatchBoosterPacks = pkmnCatchBoosterPacks,
            timeZones = timeZones
        )

    def getUser(self, handle: str) -> User:
        if not utils.isValidStr(handle):
            raise ValueError(f'handle argument is malformed: \"{handle}\"')

        jsonContents = self.__readJson()

        for key in jsonContents:
            if handle.lower() == key.lower():
                return self.__createUser(handle, jsonContents[key])

        raise RuntimeError(f'Unable to find user with handle \"{handle}\" in users repository file: \"{self.__usersFile}\"')

    def getUsers(self) -> List[User]:
        jsonContents = self.__readJson()

        users: List[User] = list()
        for key in jsonContents:
            user = self.__createUser(key, jsonContents[key])
            users.append(user)

        if not utils.hasItems(users):
            raise RuntimeError(f'Unable to read in any users from users repository file: \"{self.__usersFile}\"')

        users.sort(key = lambda user: user.getHandle().lower())
        return users

    def __parseCutenessBoosterPacksFromJson(self, json: Dict) -> List[CutenessBoosterPack]:
        if not utils.hasItems(json):
            return None

        cutenessBoosterPacks: List[CutenessBoosterPack] = list()

        for cutenessBoosterPackJson in json:
            cutenessBoosterPacks.append(CutenessBoosterPack(
                amount = utils.getIntFromDict(cutenessBoosterPackJson, 'amount'),
                rewardId = utils.getStrFromDict(cutenessBoosterPackJson, 'rewardId')
            ))

        cutenessBoosterPacks.sort(key = lambda pack: pack.getAmount())
        return cutenessBoosterPacks

    def __parsePkmnCatchBoosterPacksFromJson(self, json: Dict) -> List[PkmnCatchBoosterPack]:
        if not utils.hasItems(json):
            return None

        pkmnCatchBoosterPacks: List[PkmnCatchBoosterPack] = list()

        for pkmnCatchBoosterPackJson in json:
            pkmnCatchTypeStr = utils.getStrFromDict(
                d = pkmnCatchBoosterPackJson,
                key = 'catchType',
                fallback = PkmnCatchType.NORMAL.toStr()
            )

            pkmnCatchBoosterPacks.append(PkmnCatchBoosterPack(
                pkmnCatchType = PkmnCatchType.fromStr(pkmnCatchTypeStr),
                rewardId = utils.getStrFromDict(pkmnCatchBoosterPackJson, 'rewardId')
            ))

        pkmnCatchBoosterPacks.sort(key = lambda pack: pack.getCatchType().getSortOrder())
        return pkmnCatchBoosterPacks

    def __readJson(self) -> Dict:
        if not os.path.exists(self.__usersFile):
            raise FileNotFoundError(f'Users repository file not found: \"{self.__usersFile}\"')

        with open(self.__usersFile, 'r') as file:
            jsonContents = json.load(file)

        if jsonContents is None:
            raise IOError(f'Error reading from users repository file: \"{self.__usersFile}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of users repository file \"{self.__usersFile}\" is empty')

        return jsonContents
