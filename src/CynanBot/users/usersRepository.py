import json
import os
from datetime import tzinfo
from typing import Any, Dict, List, Optional

import aiofiles
import aiofiles.ospath

import CynanBot.misc.utils as utils
from CynanBot.cuteness.cutenessBoosterPack import CutenessBoosterPack
from CynanBot.location.timeZoneRepositoryInterface import \
    TimeZoneRepositoryInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.users.exceptions import NoSuchUserException, NoUsersException
from CynanBot.users.pkmnCatchBoosterPack import PkmnCatchBoosterPack
from CynanBot.users.pkmnCatchType import PkmnCatchType
from CynanBot.users.user import User
from CynanBot.users.usersRepositoryInterface import UsersRepositoryInterface


class UsersRepository(UsersRepositoryInterface):

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        usersFile: str = 'usersRepository.json'
    ):
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(timeZoneRepository, TimeZoneRepositoryInterface), f"malformed {timeZoneRepository=}"
        if not utils.isValidStr(usersFile):
            raise TypeError(f'usersFile argument is malformed: \"{usersFile}\"')

        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
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

        async with aiofiles.open(self.__usersFile, mode = 'w', encoding = 'utf-8') as file:
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
        assert isinstance(userJson, Dict), f"malformed {userJson=}"

        areCheerActionsEnabled = utils.getBoolFromDict(userJson, 'cheerActionsEnabled', True)
        areRecurringActionsEnabled = utils.getBoolFromDict(userJson, 'recurringActionsEnabled', True)
        isAnivContentScanningEnabled = utils.getBoolFromDict(userJson, 'anivContentScanningEnabled', False)
        isCasualGamePollEnabled = utils.getBoolFromDict(userJson, 'casualGamePollEnabled', False)
        isCatJamMessageEnabled = utils.getBoolFromDict(userJson, 'catJamMessageEnabled', False)
        isChannelPredictionChartEnabled = utils.getBoolFromDict(userJson, 'channelPredictionChartEnabled', False)
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
        isSupStreamerEnabled = utils.getBoolFromDict(userJson, 'supStreamerEnabled', False)
        isTranslateEnabled = utils.getBoolFromDict(userJson, 'translateEnabled', False)
        isTriviaEnabled = utils.getBoolFromDict(userJson, 'triviaEnabled', False)
        isTriviaGameEnabled = utils.getBoolFromDict(userJson, 'triviaGameEnabled', False)
        isTriviaScoreEnabled = utils.getBoolFromDict(userJson, 'triviaScoreEnabled', isTriviaGameEnabled)
        isTtsEnabled = utils.getBoolFromDict(userJson, 'ttsEnabled', False)
        isWeatherEnabled = utils.getBoolFromDict(userJson, 'weatherEnabled', False)
        isWelcomeTtsEnabled = utils.getBoolFromDict(userJson, 'welcomeTtsEnabled', False)
        isWordOfTheDayEnabled = utils.getBoolFromDict(userJson, 'wordOfTheDayEnabled', False)
        casualGamePollRewardId = utils.getStrFromDict(userJson, 'casualGamePollRewardId', '')
        casualGamePollUrl = utils.getStrFromDict(userJson, 'casualGamePollUrl', '')
        discord = utils.getStrFromDict(userJson, 'discord', '')
        instagram = utils.getStrFromDict(userJson, 'instagram', '')
        locationId = utils.getStrFromDict(userJson, 'locationId', '')
        mastodonUrl = utils.getStrFromDict(userJson, 'mastodonUrl', '')
        speedrunProfile = utils.getStrFromDict(userJson, 'speedrunProfile', '')
        supStreamerMessage = utils.getStrFromDict(userJson, 'supStreamerMessage', '')
        twitter = utils.getStrFromDict(userJson, 'twitter', '')

        maximumTtsCheerAmount: Optional[int] = None
        minimumTtsCheerAmount: Optional[int] = None
        if isTtsEnabled:
            if 'maximumTtsCheerAmount' in userJson and utils.isValidInt(userJson.get('maximumTtsCheerAmount')):
                maximumTtsCheerAmount = utils.getIntFromDict(userJson, 'maximumTtsCheerAmount')

            if 'minimumTtsCheerAmount' in userJson and utils.isValidInt(userJson.get('minimumTtsCheerAmount')):
                minimumTtsCheerAmount = utils.getIntFromDict(userJson, 'minimumTtsCheerAmount')

        timeZones: Optional[List[tzinfo]] = None
        if 'timeZones' in userJson:
            timeZones = self.__timeZoneRepository.getTimeZones(userJson['timeZones'])
        elif 'timeZone' in userJson:
            timeZones = list()
            timeZones.append(self.__timeZoneRepository.getTimeZone(userJson['timeZone']))

        cutenessBoosterPacks: Optional[List[CutenessBoosterPack]] = None
        if isCutenessEnabled:
            cutenessBoosterPacksJson: Optional[List[Dict[str, Any]]] = userJson.get('cutenessBoosterPacks')
            cutenessBoosterPacks = self.__parseCutenessBoosterPacksFromJson(cutenessBoosterPacksJson)

        isShinyTriviaEnabled: bool = isTriviaGameEnabled
        isToxicTriviaEnabled: bool = isTriviaGameEnabled
        isSuperTriviaGameEnabled: bool = isTriviaGameEnabled
        superTriviaCheerTriggerAmount: Optional[float] = None
        superTriviaSubscribeTriggerAmount: Optional[float] = None
        superTriviaCheerTriggerMaximum: Optional[int] = None
        superTriviaGamePoints: Optional[int] = None
        superTriviaGameRewardId: Optional[str] = None
        superTriviaGameShinyMultiplier: Optional[int] = None
        superTriviaGameToxicMultiplier: Optional[int] = None
        superTriviaGameToxicPunishmentMultiplier: Optional[int] = None
        superTriviaPerUserAttempts: Optional[int] = None
        superTriviaSubscribeTriggerMaximum: Optional[int] = None
        triviaGamePoints: Optional[int] = None
        triviaGameShinyMultiplier: Optional[int] = None
        triviaGameRewardId: Optional[str] = None
        waitForSuperTriviaAnswerDelay: Optional[int] = None
        waitForTriviaAnswerDelay: Optional[int] = None
        if isTriviaGameEnabled:
            isShinyTriviaEnabled = utils.getBoolFromDict(userJson, 'shinyTriviaEnabled', isShinyTriviaEnabled)
            isToxicTriviaEnabled = utils.getBoolFromDict(userJson, 'toxicTriviaEnabled', isToxicTriviaEnabled)
            isSuperTriviaGameEnabled = utils.getBoolFromDict(userJson, 'superTriviaGameEnabled', isSuperTriviaGameEnabled)

            if 'superTriviaCheerTriggerAmount' in userJson and utils.isValidNum(userJson.get('superTriviaCheerTriggerAmount')):
                superTriviaCheerTriggerAmount = utils.getFloatFromDict(userJson, 'superTriviaCheerTriggerAmount')

            if 'superTriviaSubscribeTriggerAmount' in userJson and utils.isValidNum(userJson.get('superTriviaSubscribeTriggerAmount')):
                superTriviaSubscribeTriggerAmount = utils.getFloatFromDict(userJson, 'superTriviaSubscribeTriggerAmount')

            superTriviaCheerTriggerMaximum = utils.getIntFromDict(userJson, 'superTriviaCheerTriggerMaximum', 5)
            superTriviaGamePoints = userJson.get('superTriviaGamePoints')
            superTriviaGameRewardId = userJson.get('superTriviaGameRewardId')
            superTriviaGameShinyMultiplier = userJson.get('superTriviaGameShinyMultiplier')
            superTriviaGameToxicMultiplier = userJson.get('superTriviaGameToxicMultiplier')
            superTriviaGameToxicPunishmentMultiplier = userJson.get('superTriviaGameToxicPunishmentMultiplier')
            superTriviaPerUserAttempts = userJson.get('superTriviaPerUserAttempts')
            superTriviaSubscribeTriggerMaximum = utils.getIntFromDict(userJson, 'superTriviaSubscribeTriggerMaximum', 5)
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
            pkmnCatchBoosterPacksJson: Optional[List[Dict[str, Any]]] = userJson.get('pkmnCatchBoosterPacks')
            pkmnCatchBoosterPacks = self.__parsePkmnCatchBoosterPacksFromJson(pkmnCatchBoosterPacksJson)

        user = User(
            areCheerActionsEnabled = areCheerActionsEnabled,
            areRecurringActionsEnabled = areRecurringActionsEnabled,
            isAnivContentScanningEnabled = isAnivContentScanningEnabled,
            isCatJamMessageEnabled = isCatJamMessageEnabled,
            isCasualGamePollEnabled = isCasualGamePollEnabled,
            isChannelPredictionChartEnabled = isChannelPredictionChartEnabled,
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
            isSupStreamerEnabled = isSupStreamerEnabled,
            isToxicTriviaEnabled = isToxicTriviaEnabled,
            isTranslateEnabled = isTranslateEnabled,
            isTriviaEnabled = isTriviaEnabled,
            isTriviaGameEnabled = isTriviaGameEnabled,
            isTriviaScoreEnabled = isTriviaScoreEnabled,
            isTtsEnabled = isTtsEnabled,
            isWeatherEnabled = isWeatherEnabled,
            isWelcomeTtsEnabled = isWelcomeTtsEnabled,
            isWordOfTheDayEnabled = isWordOfTheDayEnabled,
            superTriviaCheerTriggerAmount = superTriviaCheerTriggerAmount,
            superTriviaSubscribeTriggerAmount = superTriviaSubscribeTriggerAmount,
            maximumTtsCheerAmount = maximumTtsCheerAmount,
            minimumTtsCheerAmount = minimumTtsCheerAmount,
            superTriviaCheerTriggerMaximum = superTriviaCheerTriggerMaximum,
            superTriviaGamePoints = superTriviaGamePoints,
            superTriviaGameRewardId = superTriviaGameRewardId,
            superTriviaGameShinyMultiplier = superTriviaGameShinyMultiplier,
            superTriviaGameToxicMultiplier = superTriviaGameToxicMultiplier,
            superTriviaGameToxicPunishmentMultiplier = superTriviaGameToxicPunishmentMultiplier,
            superTriviaPerUserAttempts = superTriviaPerUserAttempts,
            superTriviaSubscribeTriggerMaximum = superTriviaSubscribeTriggerMaximum,
            triviaGamePoints = triviaGamePoints,
            triviaGameShinyMultiplier = triviaGameShinyMultiplier,
            waitForSuperTriviaAnswerDelay = waitForSuperTriviaAnswerDelay,
            waitForTriviaAnswerDelay = waitForTriviaAnswerDelay,
            casualGamePollRewardId = casualGamePollRewardId,
            casualGamePollUrl = casualGamePollUrl,
            discord = discord,
            handle = handle,
            instagram = instagram,
            locationId = locationId,
            mastodonUrl = mastodonUrl,
            pkmnBattleRewardId = pkmnBattleRewardId,
            pkmnEvolveRewardId = pkmnEvolveRewardId,
            pkmnShinyRewardId = pkmnShinyRewardId,
            speedrunProfile = speedrunProfile,
            supStreamerMessage = supStreamerMessage,
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
        if jsonContents is None:
            raise ValueError(f'jsonContents argument is malformed: \"{jsonContents}\"')

        user = self.__userCache.get(handle.lower(), None)

        if user is not None:
            return user

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

    def __parseCutenessBoosterPacksFromJson(
        self,
        jsonList: Optional[List[Dict]]
    ) -> Optional[List[CutenessBoosterPack]]:
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
        if len(jsonContents) == 0:
            raise ValueError(f'JSON contents of users repository file \"{self.__usersFile}\" is empty')

        self.__jsonCache = jsonContents
        return jsonContents

    async def __readJsonAsync(self) -> Dict[str, Any]:
        if self.__jsonCache is not None:
            return self.__jsonCache

        if not await aiofiles.ospath.exists(self.__usersFile):
            raise FileNotFoundError(f'Users repository file not found: \"{self.__usersFile}\"')

        async with aiofiles.open(self.__usersFile, mode = 'r', encoding = 'utf-8') as file:
            data = await file.read()
            jsonContents = json.loads(data)

        if jsonContents is None:
            raise IOError(f'Error reading from users repository file: \"{self.__usersFile}\"')
        if len(jsonContents) == 0:
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
        if not utils.isValidBool(enabled):
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

        async with aiofiles.open(self.__usersFile, mode = 'w', encoding = 'utf-8') as file:
            jsonString = json.dumps(jsonContents, indent = 4, sort_keys = True)
            await file.write(jsonString)

        # be sure to clear caches, as JSON file contents have now been updated
        await self.clearCaches()

        self.__timber.log('UsersRepository', f'Finished changing enabled status for user \"{handle}\" to \"{enabled}\"')
