import json
import os
from datetime import tzinfo
from typing import Dict, List

import CynanBotCommon.utils as utils
from cuteness.cutenessBoosterPack import CutenessBoosterPack
from CynanBotCommon.timeZoneRepository import TimeZoneRepository
from pkmn.pkmnCatchBoosterPack import PkmnCatchBoosterPack
from pkmn.pkmnCatchType import PkmnCatchType

from users.user import User


class UsersRepository():

    def __init__(
        self,
        timeZoneRepository: TimeZoneRepository,
        usersFile: str = 'users/usersRepository.json'
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
        elif userJson is None:
            raise ValueError(f'userJson argument is malformed: \"{userJson}\"')

        isAnalogueEnabled = utils.getBoolFromDict(userJson, 'analogueEnabled', False)
        isCatJamEnabled = utils.getBoolFromDict(userJson, 'catJamEnabled', False)
        isChatBandEnabled = utils.getBoolFromDict(userJson, 'chatBandEnabled', False)
        isCutenessEnabled = utils.getBoolFromDict(userJson, 'cutenessEnabled', False)
        isCynanMessageEnabled = utils.getBoolFromDict(userJson, 'cynanMessageEnabled', False)
        isCynanSourceEnabled = utils.getBoolFromDict(userJson, 'cynanSourceEnabled', True)
        isDeerForceMessageEnabled = utils.getBoolFromDict(userJson, 'deerForceMessageEnabled', False)
        isEyesMessageEnabled = utils.getBoolFromDict(userJson, 'eyesMessageEnabled', False)
        isGiftSubscriptionThanksMessageEnabled = utils.getBoolFromDict(userJson, 'isGiftSubscriptionThanksMessageEnabled', True)
        isGiveCutenessEnabled = utils.getBoolFromDict(userJson, 'giveCutenessEnabled', False)
        isImytSlurpEnabled = utils.getBoolFromDict(userJson, 'imytSlurpEnabled', False)
        isJamCatEnabled = utils.getBoolFromDict(userJson, 'jamCatEnabled', False)
        isJishoEnabled = utils.getBoolFromDict(userJson, 'jishoEnabled', False)
        isJokesEnabled = utils.getBoolFromDict(userJson, 'jokesEnabled', False)
        isJokeTriviaRepositoryEnabled = utils.getBoolFromDict(userJson, 'jokeTriviaRepositoryEnabled', False)
        isLoremIpsumEnabled = utils.getBoolFromDict(userJson, 'loremIpsumEnabled', True)
        isPicOfTheDayEnabled = utils.getBoolFromDict(userJson, 'picOfTheDayEnabled', False)
        isPkmnEnabled = utils.getBoolFromDict(userJson, 'pkmnEnabled', False)
        isPokepediaEnabled = utils.getBoolFromDict(userJson, 'pokepediaEnabled', False)
        isRaceEnabled = utils.getBoolFromDict(userJson, 'raceEnabled', False)
        isRaidLinkMessagingEnabled = utils.getBoolFromDict(userJson, 'raidLinkMessagingEnabled', False)
        isRatJamEnabled = utils.getBoolFromDict(userJson, 'ratJamEnabled', False)
        isRewardIdPrintingEnabled = utils.getBoolFromDict(userJson, 'rewardIdPrintingEnabled', False)
        isStarWarsQuotesEnabled = utils.getBoolFromDict(userJson, 'starWarsQuotesEnabled', False)
        isSubGiftThankingEnabled = utils.getBoolFromDict(userJson, 'subGiftThankingEnabled', True)
        isTamalesEnabled = utils.getBoolFromDict(userJson, 'tamalesEnabled', False)
        isTranslateEnabled = utils.getBoolFromDict(userJson, 'translateEnabled', False)
        isTriviaEnabled = utils.getBoolFromDict(userJson, 'triviaEnabled', False)
        isTriviaGameEnabled = utils.getBoolFromDict(userJson, 'triviaGameEnabled', False)
        isWeatherEnabled = utils.getBoolFromDict(userJson, 'weatherEnabled', False)
        isWordOfTheDayEnabled = utils.getBoolFromDict(userJson, 'wordOfTheDayEnabled', False)
        discord = utils.getStrFromDict(userJson, 'discord', '')
        instagram = utils.getStrFromDict(userJson, 'instagram', '')
        locationId = utils.getStrFromDict(userJson, 'locationId', '')
        speedrunProfile = utils.getStrFromDict(userJson, 'speedrunProfile', '')
        twitter = utils.getStrFromDict(userJson, 'twitter', '')

        timeZones: List[tzinfo] = None
        if 'timeZones' in userJson:
            timeZones = self.__timeZoneRepository.getTimeZones(userJson['timeZones'])
        elif 'timeZone' in userJson:
            timeZones = list()
            timeZones.append(self.__timeZoneRepository.getTimeZone(userJson['timeZone']))

        cutenessBoosterPacks: List[CutenessBoosterPack] = None
        if isCutenessEnabled:
            cutenessBoosterPacksJson: List[Dict] = userJson.get('cutenessBoosterPacks')
            cutenessBoosterPacks = self.__parseCutenessBoosterPacksFromJson(cutenessBoosterPacksJson)

        picOfTheDayFile: str = None
        picOfTheDayRewardId: str = None
        if isPicOfTheDayEnabled:
            picOfTheDayFile = userJson.get('picOfTheDayFile')
            picOfTheDayRewardId = userJson.get('picOfTheDayRewardId')

            if not utils.isValidStr(picOfTheDayFile):
                raise ValueError(f'POTD is enabled for {handle} but picOfTheDayFile is malformed: \"{picOfTheDayFile}\"')

        isSuperTriviaEnabled: bool = False
        superTriviaGameMultiplier: int = None
        triviaGameRewardId: str = None
        triviaGamePoints: int = None
        triviaGameTutorialCutenessThreshold: int = None
        waitForTriviaAnswerDelay: int = None
        if isTriviaGameEnabled:
            isSuperTriviaEnabled = utils.getBoolFromDict(userJson, 'superTriviaEnabled', isSuperTriviaEnabled)
            superTriviaGameMultiplier = userJson.get('superTriviaGameMultiplier')
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
            pkmnCatchBoosterPacksJson: List[Dict] = userJson.get('pkmnCatchBoosterPacks')
            pkmnCatchBoosterPacks = self.__parsePkmnCatchBoosterPacksFromJson(pkmnCatchBoosterPacksJson)

        return User(
            isAnalogueEnabled = isAnalogueEnabled,
            isCatJamEnabled = isCatJamEnabled,
            isChatBandEnabled = isChatBandEnabled,
            isCutenessEnabled = isCutenessEnabled,
            isCynanMessageEnabled = isCynanMessageEnabled,
            isCynanSourceEnabled = isCynanSourceEnabled,
            isDeerForceMessageEnabled = isDeerForceMessageEnabled,
            isEyesMessageEnabled = isEyesMessageEnabled,
            isGiftSubscriptionThanksMessageEnabled = isGiftSubscriptionThanksMessageEnabled,
            isGiveCutenessEnabled = isGiveCutenessEnabled,
            isImytSlurpEnabled = isImytSlurpEnabled,
            isJamCatEnabled = isJamCatEnabled,
            isJishoEnabled = isJishoEnabled,
            isJokesEnabled = isJokesEnabled,
            isJokeTriviaRepositoryEnabled = isJokeTriviaRepositoryEnabled,
            isLoremIpsumEnabled = isLoremIpsumEnabled,
            isPicOfTheDayEnabled = isPicOfTheDayEnabled,
            isPkmnEnabled = isPkmnEnabled,
            isPokepediaEnabled = isPokepediaEnabled,
            isRaceEnabled = isRaceEnabled,
            isRaidLinkMessagingEnabled = isRaidLinkMessagingEnabled,
            isRatJamEnabled = isRatJamEnabled,
            isRewardIdPrintingEnabled = isRewardIdPrintingEnabled,
            isStarWarsQuotesEnabled = isStarWarsQuotesEnabled,
            isSubGiftThankingEnabled = isSubGiftThankingEnabled,
            isSuperTriviaEnabled = isSuperTriviaEnabled,
            isTamalesEnabled = isTamalesEnabled,
            isTranslateEnabled = isTranslateEnabled,
            isTriviaEnabled = isTriviaEnabled,
            isTriviaGameEnabled = isTriviaGameEnabled,
            isWeatherEnabled = isWeatherEnabled,
            isWordOfTheDayEnabled = isWordOfTheDayEnabled,
            superTriviaGameMultiplier = superTriviaGameMultiplier,
            triviaGamePoints = triviaGamePoints,
            triviaGameTutorialCutenessThreshold = triviaGameTutorialCutenessThreshold,
            waitForTriviaAnswerDelay = waitForTriviaAnswerDelay,
            discord = discord,
            handle = handle,
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

    def __parseCutenessBoosterPacksFromJson(self, jsonList: List[Dict]) -> List[CutenessBoosterPack]:
        if not utils.hasItems(jsonList):
            return None

        cutenessBoosterPacks: List[CutenessBoosterPack] = list()

        for cutenessBoosterPackJson in jsonList:
            cutenessBoosterPacks.append(CutenessBoosterPack(
                amount = utils.getIntFromDict(cutenessBoosterPackJson, 'amount'),
                rewardId = utils.getStrFromDict(cutenessBoosterPackJson, 'rewardId')
            ))

        cutenessBoosterPacks.sort(key = lambda pack: pack.getAmount())
        return cutenessBoosterPacks

    def __parsePkmnCatchBoosterPacksFromJson(self, jsonList: List[Dict]) -> List[PkmnCatchBoosterPack]:
        if not utils.hasItems(jsonList):
            return None

        pkmnCatchBoosterPacks: List[PkmnCatchBoosterPack] = list()

        for pkmnCatchBoosterPackJson in jsonList:
            pkmnCatchTypeStr = utils.getStrFromDict(
                d = pkmnCatchBoosterPackJson,
                key = 'catchType',
                fallback = ''
            )

            pkmnCatchType: PkmnCatchType = None
            if utils.isValidStr(pkmnCatchTypeStr):
                pkmnCatchType = PkmnCatchType.fromStr(pkmnCatchTypeStr)

            pkmnCatchBoosterPacks.append(PkmnCatchBoosterPack(
                pkmnCatchType = pkmnCatchType,
                rewardId = utils.getStrFromDict(pkmnCatchBoosterPackJson, 'rewardId')
            ))

        return pkmnCatchBoosterPacks

    def __readJson(self) -> Dict[str, object]:
        if not os.path.exists(self.__usersFile):
            raise FileNotFoundError(f'Users repository file not found: \"{self.__usersFile}\"')

        with open(self.__usersFile, 'r') as file:
            jsonContents = json.load(file)

        if jsonContents is None:
            raise IOError(f'Error reading from users repository file: \"{self.__usersFile}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of users repository file \"{self.__usersFile}\" is empty')

        return jsonContents
