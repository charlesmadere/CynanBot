import json
import os
from datetime import tzinfo
from typing import Any, Dict, List, Optional

import aiofiles
import aiofiles.ospath

import CynanBotCommon.utils as utils
from CynanBotCommon.cuteness.cutenessBoosterPack import CutenessBoosterPack
from CynanBotCommon.timber.timberInterface import TimberInterface
from CynanBotCommon.timeZoneRepository import TimeZoneRepository
from CynanBotCommon.users.exceptions import (NoSuchUserException,
                                             NoUsersException)
from CynanBotCommon.users.usersRepositoryInterface import \
    UsersRepositoryInterface
from pkmn.pkmnCatchBoosterPack import PkmnCatchBoosterPack
from pkmn.pkmnCatchType import PkmnCatchType
from users.user import User


class UsersRepository(UsersRepositoryInterface):

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepository,
        usersFile: str = 'users/usersRepository.json'
    ):
        if not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepository):
            raise ValueError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not utils.isValidStr(usersFile):
            raise ValueError(f'usersFile argument is malformed: \"{usersFile}\"')

        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepository = timeZoneRepository
        self.__usersFile: str = usersFile

        self.__jsonCache: Optional[Dict[str, Any]] = None
        self.__userCache: Dict[str, Optional[User]] = dict()

    async def addUser(self, handle: str):
        if not utils.isValidStr(handle):
            raise ValueError(f'handle argument is malformed: \"{handle}\"')

        self.__timber.log('UsersRepository', f'Adding user \"{handle}\"...')
        jsonContents = await self.__readJsonAsync()

        for key in jsonContents.keys():
            if key.lower() == handle.lower():
                self.__timber.log('UsersRepository', f'Unable to add user \"{handle}\" as a user with that handle already exists')
                return

        jsonContents[handle] = dict()

        async with aiofiles.open(self.__usersFile, mode = 'w') as file:
            jsonString = json.dumps(jsonContents, indent = 4, sort_keys = True)
            await file.write(jsonString)

        # be sure to clear caches, as JSON file contents have now been updated
        await self.clearCaches()

        self.__timber.log('UsersRepository', f'Finished adding user \"{handle}\"')

    async def clearCaches(self):
        self.__jsonCache = None
        self.__userCache.clear()
        self.__timber.log('UsersRepository', 'Caches cleared')

    def containsUser(self, handle: str) -> bool:
        if not utils.isValidStr(handle):
            raise ValueError(f'handle argument is malformed: \"{handle}\"')

        try:
            self.getUser(handle)
            return True
        except NoSuchUserException:
            return False

    async def containsUserAsync(self, handle: str) -> bool:
        if not utils.isValidStr(handle):
            raise ValueError(f'handle argument is malformed: \"{handle}\"')

        try:
            await self.getUserAsync(handle)
            return True
        except NoSuchUserException:
            return False

    def __createUser(self, handle: str, userJson: Dict[str, Any]) -> User:
        if not utils.isValidStr(handle):
            raise ValueError(f'handle argument is malformed: \"{handle}\"')
        elif not isinstance(userJson, Dict):
            raise ValueError(f'userJson argument is malformed: \"{userJson}\"')

        areRecurringActionsEnabled = utils.getBoolFromDict(userJson, 'recurringActionsEnabled', True)
        isCatJamMessageEnabled = utils.getBoolFromDict(userJson, 'catJamMessageEnabled', False)
        isChatBandEnabled = utils.getBoolFromDict(userJson, 'chatBandEnabled', False)
        isChatLoggingEnabled = utils.getBoolFromDict(userJson, 'chatLoggingEnabled', False)
        isCutenessEnabled = utils.getBoolFromDict(userJson, 'cutenessEnabled', False)
        isCynanSourceEnabled = utils.getBoolFromDict(userJson, 'cynanSourceEnabled', True)
        isDeerForceMessageEnabled = utils.getBoolFromDict(userJson, 'deerForceMessageEnabled', False)
        isEnabled = utils.getBoolFromDict(userJson, 'enabled', True)
        isEyesMessageEnabled = utils.getBoolFromDict(userJson, 'eyesMessageEnabled', False)
        isGiftSubscriptionThanksMessageEnabled = utils.getBoolFromDict(userJson, 'isGiftSubscriptionThanksMessageEnabled', True)
        isGiveCutenessEnabled = utils.getBoolFromDict(userJson, 'giveCutenessEnabled', False)
        isImytSlurpMessageEnabled = utils.getBoolFromDict(userJson, 'imytSlurpMessageEnabled', False)
        isJamCatMessageEnabled = utils.getBoolFromDict(userJson, 'jamCatMessageEnabled', False)
        isJishoEnabled = utils.getBoolFromDict(userJson, 'jishoEnabled', False)
        isJokeTriviaRepositoryEnabled = utils.getBoolFromDict(userJson, 'jokeTriviaRepositoryEnabled', False)
        isLoremIpsumEnabled = utils.getBoolFromDict(userJson, 'loremIpsumEnabled', True)
        isPkmnEnabled = utils.getBoolFromDict(userJson, 'pkmnEnabled', False)
        isPokepediaEnabled = utils.getBoolFromDict(userJson, 'pokepediaEnabled', False)
        isRaceEnabled = utils.getBoolFromDict(userJson, 'raceEnabled', False)
        isRaidLinkMessagingEnabled = utils.getBoolFromDict(userJson, 'raidLinkMessagingEnabled', False)
        isRatJamMessageEnabled = utils.getBoolFromDict(userJson, 'ratJamMessageEnabled', False)
        isRewardIdPrintingEnabled = utils.getBoolFromDict(userJson, 'rewardIdPrintingEnabled', False)
        isRoachMessageEnabled = utils.getBoolFromDict(userJson, 'roachMessageEnabled', False)
        isSchubertWalkMessageEnabled = utils.getBoolFromDict(userJson, 'schubertWalkMessageEnabled', False)
        isStarWarsQuotesEnabled = utils.getBoolFromDict(userJson, 'starWarsQuotesEnabled', False)
        isSubGiftThankingEnabled = utils.getBoolFromDict(userJson, 'subGiftThankingEnabled', True)
        isTranslateEnabled = utils.getBoolFromDict(userJson, 'translateEnabled', False)
        isTriviaEnabled = utils.getBoolFromDict(userJson, 'triviaEnabled', False)
        isTriviaGameEnabled = utils.getBoolFromDict(userJson, 'triviaGameEnabled', False)
        isTtsEnabled = utils.getBoolFromDict(userJson, 'ttsEnabled', False)
        isWeatherEnabled = utils.getBoolFromDict(userJson, 'weatherEnabled', False)
        isWordOfTheDayEnabled = utils.getBoolFromDict(userJson, 'wordOfTheDayEnabled', False)
        discord = utils.getStrFromDict(userJson, 'discord', '')
        instagram = utils.getStrFromDict(userJson, 'instagram', '')
        locationId = utils.getStrFromDict(userJson, 'locationId', '')
        mastodonUrl = utils.getStrFromDict(userJson, 'mastodonUrl', '')
        minimumTtsCheerAmount = utils.getIntFromDict(userJson, 'minimumTtsCheerAmount', 100)
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

        isShinyTriviaEnabled: bool = isTriviaGameEnabled
        isToxicTriviaEnabled: bool = isTriviaGameEnabled
        isSuperTriviaGameEnabled: bool = isTriviaGameEnabled
        superTriviaCheerTriggerAmount: Optional[int] = None
        superTriviaGamePoints: Optional[int] = None
        superTriviaGameRewardId: Optional[str] = None
        superTriviaGameShinyMultiplier: Optional[int] = None
        superTriviaGameToxicMultiplier: Optional[int] = None
        superTriviaGameToxicPunishmentMultiplier: Optional[int] = None
        superTriviaPerUserAttempts: Optional[int] = None
        triviaGamePoints: Optional[int] = None
        triviaGameShinyMultiplier: Optional[int] = None
        triviaGameRewardId: Optional[str] = None
        waitForSuperTriviaAnswerDelay: Optional[int] = None
        waitForTriviaAnswerDelay: Optional[int] = None
        if isTriviaGameEnabled:
            isShinyTriviaEnabled = utils.getBoolFromDict(userJson, 'shinyTriviaEnabled', isShinyTriviaEnabled)
            isToxicTriviaEnabled = utils.getBoolFromDict(userJson, 'toxicTriviaEnabled', isToxicTriviaEnabled)
            isSuperTriviaGameEnabled = utils.getBoolFromDict(userJson, 'superTriviaGameEnabled', isSuperTriviaGameEnabled)
            superTriviaCheerTriggerAmount = utils.getIntFromDict(userJson, 'superTriviaCheerTriggerAmount', 250)
            superTriviaGamePoints = userJson.get('superTriviaGamePoints')
            superTriviaGameRewardId = userJson.get('superTriviaGameRewardId')
            superTriviaGameShinyMultiplier = userJson.get('superTriviaGameShinyMultiplier')
            superTriviaGameToxicMultiplier = userJson.get('superTriviaGameToxicMultiplier')
            superTriviaGameToxicPunishmentMultiplier = userJson.get('superTriviaGameToxicPunishmentMultiplier')
            superTriviaPerUserAttempts = userJson.get('superTriviaPerUserAttempts')
            triviaGamePoints = userJson.get('triviaGamePoints')
            triviaGameShinyMultiplier = userJson.get('triviaGameShinyMultiplier')
            triviaGameRewardId = userJson.get('triviaGameRewardId')
            waitForSuperTriviaAnswerDelay = userJson.get('waitForSuperTriviaAnswerDelay')
            waitForTriviaAnswerDelay = userJson.get('waitForTriviaAnswerDelay')

        pkmnBattleRewardId: Optional[str] = None
        pkmnEvolveRewardId: Optional[str] = None
        pkmnShinyRewardId: Optional[str] = None
        pkmnCatchBoosterPacks: Optional[List[PkmnCatchBoosterPack]] = None
        if isPkmnEnabled:
            pkmnBattleRewardId = userJson.get('pkmnBattleRewardId')
            pkmnEvolveRewardId = userJson.get('pkmnEvolveRewardId')
            pkmnShinyRewardId = userJson.get('pkmnShinyRewardId')
            pkmnCatchBoosterPacksJson: List[Dict] = userJson.get('pkmnCatchBoosterPacks')
            pkmnCatchBoosterPacks = self.__parsePkmnCatchBoosterPacksFromJson(pkmnCatchBoosterPacksJson)

        user = User(
            areRecurringActionsEnabled = areRecurringActionsEnabled,
            isCatJamMessageEnabled = isCatJamMessageEnabled,
            isChatBandEnabled = isChatBandEnabled,
            isChatLoggingEnabled = isChatLoggingEnabled,
            isCutenessEnabled = isCutenessEnabled,
            isCynanSourceEnabled = isCynanSourceEnabled,
            isDeerForceMessageEnabled = isDeerForceMessageEnabled,
            isEnabled = isEnabled,
            isEyesMessageEnabled = isEyesMessageEnabled,
            isGiftSubscriptionThanksMessageEnabled = isGiftSubscriptionThanksMessageEnabled,
            isGiveCutenessEnabled = isGiveCutenessEnabled,
            isImytSlurpMessageEnabled = isImytSlurpMessageEnabled,
            isJamCatMessageEnabled = isJamCatMessageEnabled,
            isJishoEnabled = isJishoEnabled,
            isJokeTriviaRepositoryEnabled = isJokeTriviaRepositoryEnabled,
            isLoremIpsumEnabled = isLoremIpsumEnabled,
            isPkmnEnabled = isPkmnEnabled,
            isPokepediaEnabled = isPokepediaEnabled,
            isRaceEnabled = isRaceEnabled,
            isRaidLinkMessagingEnabled = isRaidLinkMessagingEnabled,
            isRatJamMessageEnabled = isRatJamMessageEnabled,
            isRewardIdPrintingEnabled = isRewardIdPrintingEnabled,
            isRoachMessageEnabled = isRoachMessageEnabled,
            isSchubertWalkMessageEnabled = isSchubertWalkMessageEnabled,
            isShinyTriviaEnabled = isShinyTriviaEnabled,
            isStarWarsQuotesEnabled = isStarWarsQuotesEnabled,
            isSubGiftThankingEnabled = isSubGiftThankingEnabled,
            isSuperTriviaGameEnabled = isSuperTriviaGameEnabled,
            isToxicTriviaEnabled = isToxicTriviaEnabled,
            isTranslateEnabled = isTranslateEnabled,
            isTriviaEnabled = isTriviaEnabled,
            isTriviaGameEnabled = isTriviaGameEnabled,
            isTtsEnabled = isTtsEnabled,
            isWeatherEnabled = isWeatherEnabled,
            isWordOfTheDayEnabled = isWordOfTheDayEnabled,
            minimumTtsCheerAmount = minimumTtsCheerAmount,
            superTriviaCheerTriggerAmount = superTriviaCheerTriggerAmount,
            superTriviaGamePoints = superTriviaGamePoints,
            superTriviaGameRewardId = superTriviaGameRewardId,
            superTriviaGameShinyMultiplier = superTriviaGameShinyMultiplier,
            superTriviaGameToxicMultiplier = superTriviaGameToxicMultiplier,
            superTriviaGameToxicPunishmentMultiplier = superTriviaGameToxicPunishmentMultiplier,
            superTriviaPerUserAttempts = superTriviaPerUserAttempts,
            triviaGamePoints = triviaGamePoints,
            triviaGameShinyMultiplier = triviaGameShinyMultiplier,
            waitForSuperTriviaAnswerDelay = waitForSuperTriviaAnswerDelay,
            waitForTriviaAnswerDelay = waitForTriviaAnswerDelay,
            discord = discord,
            handle = handle,
            instagram = instagram,
            locationId = locationId,
            mastodonUrl = mastodonUrl,
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

        self.__userCache[handle.lower()] = user
        return user

    def __createUsers(self, jsonContents: Dict[str, Any]) -> List[User]:
        if not utils.hasItems(jsonContents):
            raise ValueError(f'jsonContents argument is malformed: \"{jsonContents}\"')

        users: List[User] = list()
        for key, userJson in jsonContents.items():
            user = self.__createUser(key, userJson)
            users.append(user)

        if not utils.hasItems(users):
            raise NoUsersException(f'Unable to read in any users from users repository file: \"{self.__usersFile}\"')

        users.sort(key = lambda user: user.getHandle().lower())
        return users

    def __findAndCreateUser(self, handle: str, jsonContents: Dict[str, Any]) -> User:
        if not utils.isValidStr(handle):
            raise ValueError(f'handle argument is malformed: \"{handle}\"')
        elif jsonContents is None:
            raise ValueError(f'jsonContents argument is malformed: \"{jsonContents}\"')

        if handle.lower() in self.__userCache:
            return self.__userCache[handle.lower()]

        for key, userJson in jsonContents.items():
            if handle.lower() == key.lower():
                return self.__createUser(handle, userJson)

        raise NoSuchUserException(f'Unable to find user with handle \"{handle}\" in users repository file: \"{self.__usersFile}\"')

    def getUser(self, handle: str) -> User:
        if not utils.isValidStr(handle):
            raise ValueError(f'handle argument is malformed: \"{handle}\"')

        jsonContents = self.__readJson()
        return self.__findAndCreateUser(handle, jsonContents)

    async def getUserAsync(self, handle: str) -> User:
        if not utils.isValidStr(handle):
            raise ValueError(f'handle argument is malformed: \"{handle}\"')

        jsonContents = await self.__readJsonAsync()
        return self.__findAndCreateUser(handle, jsonContents)

    def getUsers(self) -> List[User]:
        jsonContents = self.__readJson()
        return self.__createUsers(jsonContents)

    async def getUsersAsync(self) -> List[User]:
        jsonContents = await self.__readJsonAsync()
        return self.__createUsers(jsonContents)

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

    def __parsePkmnCatchBoosterPacksFromJson(
        self,
        jsonList: Optional[List[Dict[str, Any]]]
    ) -> Optional[List[PkmnCatchBoosterPack]]:
        if not utils.hasItems(jsonList):
            return None

        pkmnCatchBoosterPacks: List[PkmnCatchBoosterPack] = list()

        for pkmnCatchBoosterPackJson in jsonList:
            pkmnCatchTypeStr = utils.getStrFromDict(
                d = pkmnCatchBoosterPackJson,
                key = 'catchType',
                fallback = ''
            )

            pkmnCatchType: Optional[PkmnCatchType] = None
            if utils.isValidStr(pkmnCatchTypeStr):
                pkmnCatchType = PkmnCatchType.fromStr(pkmnCatchTypeStr)

            pkmnCatchBoosterPacks.append(PkmnCatchBoosterPack(
                pkmnCatchType = pkmnCatchType,
                rewardId = utils.getStrFromDict(pkmnCatchBoosterPackJson, 'rewardId')
            ))

        return pkmnCatchBoosterPacks

    def __readJson(self) -> Dict[str, Any]:
        if self.__jsonCache is not None:
            return self.__jsonCache

        if not os.path.exists(self.__usersFile):
            raise FileNotFoundError(f'Users repository file not found: \"{self.__usersFile}\"')

        with open(self.__usersFile, 'r') as file:
            jsonContents = json.load(file)

        if jsonContents is None:
            raise IOError(f'Error reading from users repository file: \"{self.__usersFile}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of users repository file \"{self.__usersFile}\" is empty')

        self.__jsonCache = jsonContents
        return jsonContents

    async def __readJsonAsync(self) -> Dict[str, Any]:
        if self.__jsonCache is not None:
            return self.__jsonCache

        if not await aiofiles.ospath.exists(self.__usersFile):
            raise FileNotFoundError(f'Users repository file not found: \"{self.__usersFile}\"')

        async with aiofiles.open(self.__usersFile, mode = 'r') as file:
            data = await file.read()
            jsonContents = json.loads(data)

        if jsonContents is None:
            raise IOError(f'Error reading from users repository file: \"{self.__usersFile}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of users repository file \"{self.__usersFile}\" is empty')

        self.__jsonCache = jsonContents
        return jsonContents

    async def removeUser(self, handle: str):
        if not utils.isValidStr(handle):
            raise ValueError(f'handle argument is malformed: \"{handle}\"')

        self.__timber.log('UsersRepository', f'Removing user \"{handle}\"...')
        await self.setUserEnabled(handle, False)
        self.__timber.log('UsersRepository', f'Finished removing user \"{handle}\"')

    async def setUserEnabled(self, handle: str, enabled: bool):
        if not utils.isValidStr(handle):
            raise ValueError(f'handle argument is malformed: \"{handle}\"')
        elif not utils.isValidBool(enabled):
            raise ValueError(f'enabled argument is malformed: \"{enabled}\"')

        self.__timber.log('UsersRepository', f'Changing enabled status for user \"{handle}\" to \"{enabled}\"...')
        jsonContents = await self.__readJsonAsync()
        preExistingHandle: Optional[str] = None

        for key in jsonContents.keys():
            if key.lower() == handle.lower():
                preExistingHandle = key
                break

        if not utils.isValidStr(preExistingHandle):
            self.__timber.log('UsersRepository', f'Unable to change enabled status for user \"{handle}\" as no user with that handle currently exists')
            return

        jsonContents[preExistingHandle]['enabled'] = enabled

        async with aiofiles.open(self.__usersFile, mode = 'w') as file:
            jsonString = json.dumps(jsonContents, indent = 4, sort_keys = True)
            await file.write(jsonString)

        # be sure to clear caches, as JSON file contents have now been updated
        await self.clearCaches()

        self.__timber.log('UsersRepository', f'Finished changing enabled status for user \"{handle}\" to \"{enabled}\"')
