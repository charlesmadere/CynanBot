import json
import os
from datetime import tzinfo
from typing import Any

import aiofiles
import aiofiles.ospath

from .exceptions import BadModifyUserValueException, NoSuchUserException, NoUsersException
from .pkmnCatchBoosterPack import PkmnCatchBoosterPack
from .pkmnCatchType import PkmnCatchType
from .soundAlertRedemption import SoundAlertRedemption
from .user import User
from .userJsonConstant import UserJsonConstant
from .usersRepositoryInterface import UsersRepositoryInterface
from ..cuteness.cutenessBoosterPack import CutenessBoosterPack
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..soundPlayerManager.soundAlertJsonMapperInterface import SoundAlertJsonMapperInterface
from ..timber.timberInterface import TimberInterface


class UsersRepository(UsersRepositoryInterface):

    def __init__(
        self,
        soundAlertJsonMapper: SoundAlertJsonMapperInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        usersFile: str = 'usersRepository.json'
    ):
        if not isinstance(soundAlertJsonMapper, SoundAlertJsonMapperInterface):
            raise TypeError(f'soundAlertJsonMapper argument is malformed: \"{soundAlertJsonMapper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not utils.isValidStr(usersFile):
            raise TypeError(f'usersFile argument is malformed: \"{usersFile}\"')

        self.__soundAlertJsonMapper: SoundAlertJsonMapperInterface = soundAlertJsonMapper
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__usersFile: str = usersFile

        self.__jsonCache: dict[str, Any] | None = None
        self.__userCache: dict[str, User | None] = dict()

    async def addUser(self, handle: str):
        if not utils.isValidStr(handle):
            raise TypeError(f'handle argument is malformed: \"{handle}\"')

        self.__timber.log('UsersRepository', f'Adding user \"{handle}\"...')
        jsonContents = await self.__readJsonAsync()

        for key in jsonContents.keys():
            if key.casefold() == handle.casefold():
                self.__timber.log('UsersRepository', f'Unable to add user \"{handle}\" as a user with that handle already exists')
                return

        jsonContents[handle] = dict()
        await self.__writeAndFlushUsersFileAsync(jsonContents)
        self.__timber.log('UsersRepository', f'Finished adding user \"{handle}\"')

    async def clearCaches(self):
        self.__jsonCache = None
        self.__userCache.clear()
        self.__timber.log('UsersRepository', 'Caches cleared')

    def containsUser(self, handle: str) -> bool:
        if not utils.isValidStr(handle):
            raise TypeError(f'handle argument is malformed: \"{handle}\"')

        try:
            self.getUser(handle)
            return True
        except NoSuchUserException:
            return False

    async def containsUserAsync(self, handle: str) -> bool:
        if not utils.isValidStr(handle):
            raise TypeError(f'handle argument is malformed: \"{handle}\"')

        try:
            await self.getUserAsync(handle)
            return True
        except NoSuchUserException:
            return False

    def __createUser(self, handle: str, userJson: dict[str, Any]) -> User:
        if not utils.isValidStr(handle):
            raise TypeError(f'handle argument is malformed: \"{handle}\"')
        elif not isinstance(userJson, dict):
            raise TypeError(f'userJson argument is malformed: \"{userJson}\"')

        areCheerActionsEnabled = utils.getBoolFromDict(userJson, 'cheerActionsEnabled', False)

        timeoutCheerActionFollowShieldDays: int | None = None
        if areCheerActionsEnabled:
            if 'timeoutCheerActionFollowShieldDays' in userJson and utils.isValidInt(userJson.get('timeoutCheerActionFollowShieldDays')):
                timeoutCheerActionFollowShieldDays = utils.getIntFromDict(userJson, 'timeoutCheerActionFollowShieldDays')

        areBeanChancesEnabled = utils.getBoolFromDict(userJson, 'beanChancesEnabled', False)
        areRecurringActionsEnabled = utils.getBoolFromDict(userJson, 'recurringActionsEnabled', True)
        areSoundAlertsEnabled = utils.getBoolFromDict(userJson, 'soundAlertsEnabled', False)
        areTimeoutCheerActionsEnabled = utils.getBoolFromDict(userJson, 'timeoutCheerActionsEnabled', False)
        isAnivContentScanningEnabled = utils.getBoolFromDict(userJson, 'anivContentScanningEnabled', False)
        isAnivMessageCopyTimeoutEnabled = utils.getBoolFromDict(userJson, UserJsonConstant.ANIV_MESSAGE_COPY_TIMEOUT_ENABLED.jsonKey, False)
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
        isShizaMessageEnabled = utils.getBoolFromDict(userJson, 'shizaMessageEnabled', False)
        isStarWarsQuotesEnabled = utils.getBoolFromDict(userJson, 'starWarsQuotesEnabled', False)
        isSubGiftThankingEnabled = utils.getBoolFromDict(userJson, 'subGiftThankingEnabled', True)
        isSupStreamerEnabled = utils.getBoolFromDict(userJson, 'supStreamerEnabled', False)
        isTranslateEnabled = utils.getBoolFromDict(userJson, 'translateEnabled', False)
        isTriviaGameEnabled = utils.getBoolFromDict(userJson, 'triviaGameEnabled', False)
        isTriviaScoreEnabled = utils.getBoolFromDict(userJson, 'triviaScoreEnabled', isTriviaGameEnabled)
        isTtsEnabled = utils.getBoolFromDict(userJson, UserJsonConstant.TTS_ENABLED.jsonKey, False)
        isWeatherEnabled = utils.getBoolFromDict(userJson, 'weatherEnabled', False)
        isWelcomeTtsEnabled = utils.getBoolFromDict(userJson, 'welcomeTtsEnabled', False)
        isWordOfTheDayEnabled = utils.getBoolFromDict(userJson, 'wordOfTheDayEnabled', False)
        casualGamePollRewardId = utils.getStrFromDict(userJson, 'casualGamePollRewardId', '')
        casualGamePollUrl = utils.getStrFromDict(userJson, 'casualGamePollUrl', '')
        discord = utils.getStrFromDict(userJson, 'discord', '')
        instagram = utils.getStrFromDict(userJson, 'instagram', '')
        locationId = utils.getStrFromDict(userJson, 'locationId', '')
        mastodonUrl = utils.getStrFromDict(userJson, 'mastodonUrl', '')
        randomSoundAlertRewardId = utils.getStrFromDict(userJson, 'randomSoundAlertRewardId', '')
        shizaMessageRewardId = utils.getStrFromDict(userJson, 'shizaMessageRewardId', '')
        soundAlertRewardId = utils.getStrFromDict(userJson, 'soundAlertRewardId', '')
        speedrunProfile = utils.getStrFromDict(userJson, 'speedrunProfile', '')
        supStreamerMessage = utils.getStrFromDict(userJson, 'supStreamerMessage', '')
        twitterUrl = utils.getStrFromDict(userJson, 'twitterUrl', '')

        anivMessageCopyMaxAgeSeconds: int | None = None
        anivMessageCopyTimeoutProbability: float | None = None
        anivMessageCopyTimeoutSeconds: int | None = None
        if isAnivMessageCopyTimeoutEnabled:
            if 'anivMessageCopyMaxAgeSeconds' in userJson and utils.isValidInt(userJson.get('anivCopyMessageMaxAgeSeconds')):
                anivMessageCopyMaxAgeSeconds = utils.getIntFromDict(userJson, 'anivMessageCopyMaxAgeSeconds')

            if 'anivMessageCopyTimeoutProbability' in userJson and utils.isValidNum(userJson.get('anivMessageCopyTimeoutProbability')):
                anivMessageCopyTimeoutProbability = utils.getFloatFromDict(userJson, 'anivMessageCopyTimeoutProbability')

            if 'anivMessageCopyTimeoutSeconds' in userJson and utils.isValidInt(userJson.get('anivMessageCopyTimeoutSeconds')):
                anivMessageCopyTimeoutSeconds = utils.getIntFromDict(userJson, 'anivMessageCopyTimeoutSeconds')

        maximumTtsCheerAmount: int | None = None
        minimumTtsCheerAmount: int | None = None
        if isTtsEnabled:
            if 'maximumTtsCheerAmount' in userJson and utils.isValidInt(userJson.get('maximumTtsCheerAmount')):
                maximumTtsCheerAmount = utils.getIntFromDict(userJson, 'maximumTtsCheerAmount')

            if 'minimumTtsCheerAmount' in userJson and utils.isValidInt(userJson.get('minimumTtsCheerAmount')):
                minimumTtsCheerAmount = utils.getIntFromDict(userJson, 'minimumTtsCheerAmount')

        timeZones: list[tzinfo] | None = None
        if 'timeZones' in userJson:
            timeZones = self.__timeZoneRepository.getTimeZones(userJson['timeZones'])
        elif 'timeZone' in userJson:
            timeZones = list()
            timeZones.append(self.__timeZoneRepository.getTimeZone(userJson['timeZone']))

        cutenessBoosterPacks: list[CutenessBoosterPack] | None = None
        if isCutenessEnabled:
            cutenessBoosterPacksJson: list[dict[str, Any]] | None = userJson.get('cutenessBoosterPacks')
            cutenessBoosterPacks = self.__parseCutenessBoosterPacksFromJson(cutenessBoosterPacksJson)

        isShinyTriviaEnabled: bool = isTriviaGameEnabled
        isToxicTriviaEnabled: bool = isTriviaGameEnabled
        isSuperTriviaGameEnabled: bool = isTriviaGameEnabled
        superTriviaCheerTriggerAmount: float | None = None
        superTriviaSubscribeTriggerAmount: float | None = None
        superTriviaCheerTriggerMaximum: int | None = None
        superTriviaGamePoints: int | None = None
        superTriviaGameRewardId: str | None = None
        superTriviaGameShinyMultiplier: int | None = None
        superTriviaGameToxicMultiplier: int | None = None
        superTriviaGameToxicPunishmentMultiplier: int | None = None
        superTriviaPerUserAttempts: int | None = None
        superTriviaSubscribeTriggerMaximum: int | None = None
        triviaGamePoints: int | None = None
        triviaGameShinyMultiplier: int | None = None
        triviaGameRewardId: str | None = None
        waitForSuperTriviaAnswerDelay: int | None = None
        waitForTriviaAnswerDelay: int | None = None
        if isTriviaGameEnabled or isSuperTriviaGameEnabled:
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

        pkmnBattleRewardId: str | None = None
        pkmnEvolveRewardId: str | None = None
        pkmnShinyRewardId: str | None = None
        pkmnCatchBoosterPacks: list[PkmnCatchBoosterPack] | None = None
        if isPkmnEnabled:
            pkmnBattleRewardId = userJson.get('pkmnBattleRewardId')
            pkmnEvolveRewardId = userJson.get('pkmnEvolveRewardId')
            pkmnShinyRewardId = userJson.get('pkmnShinyRewardId')
            pkmnCatchBoosterPacksJson: list[dict[str, Any]] | None = userJson.get('pkmnCatchBoosterPacks')
            pkmnCatchBoosterPacks = self.__parsePkmnCatchBoosterPacksFromJson(pkmnCatchBoosterPacksJson)

        soundAlertRedemptions: dict[str, SoundAlertRedemption] | None = None
        if areSoundAlertsEnabled:
            soundAlertRedemptionsJson: list[dict[str, Any]] | None = userJson.get('soundAlertRedemptions')
            soundAlertRedemptions = self.__parseSoundAlertRedemptionsFromJson(soundAlertRedemptionsJson)

        user = User(
            areBeanChancesEnabled = areBeanChancesEnabled,
            areCheerActionsEnabled = areCheerActionsEnabled,
            areRecurringActionsEnabled = areRecurringActionsEnabled,
            areSoundAlertsEnabled = areSoundAlertsEnabled,
            areTimeoutCheerActionsEnabled = areTimeoutCheerActionsEnabled,
            isAnivContentScanningEnabled = isAnivContentScanningEnabled,
            isAnivMessageCopyTimeoutEnabled = isAnivMessageCopyTimeoutEnabled,
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
            isShizaMessageEnabled = isShizaMessageEnabled,
            isStarWarsQuotesEnabled = isStarWarsQuotesEnabled,
            isSubGiftThankingEnabled = isSubGiftThankingEnabled,
            isSuperTriviaGameEnabled = isSuperTriviaGameEnabled,
            isSupStreamerEnabled = isSupStreamerEnabled,
            isToxicTriviaEnabled = isToxicTriviaEnabled,
            isTranslateEnabled = isTranslateEnabled,
            isTriviaGameEnabled = isTriviaGameEnabled,
            isTriviaScoreEnabled = isTriviaScoreEnabled,
            isTtsEnabled = isTtsEnabled,
            isWeatherEnabled = isWeatherEnabled,
            isWelcomeTtsEnabled = isWelcomeTtsEnabled,
            isWordOfTheDayEnabled = isWordOfTheDayEnabled,
            anivMessageCopyTimeoutProbability = anivMessageCopyTimeoutProbability,
            superTriviaCheerTriggerAmount = superTriviaCheerTriggerAmount,
            superTriviaSubscribeTriggerAmount = superTriviaSubscribeTriggerAmount,
            anivMessageCopyMaxAgeSeconds = anivMessageCopyMaxAgeSeconds,
            anivMessageCopyTimeoutSeconds = anivMessageCopyTimeoutSeconds,
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
            timeoutCheerActionFollowShieldDays = timeoutCheerActionFollowShieldDays,
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
            randomSoundAlertRewardId = randomSoundAlertRewardId,
            shizaMessageRewardId = shizaMessageRewardId,
            speedrunProfile = speedrunProfile,
            soundAlertRewardId = soundAlertRewardId,
            supStreamerMessage = supStreamerMessage,
            triviaGameRewardId = triviaGameRewardId,
            twitterUrl = twitterUrl,
            soundAlertRedemptions = soundAlertRedemptions,
            cutenessBoosterPacks = cutenessBoosterPacks,
            pkmnCatchBoosterPacks = pkmnCatchBoosterPacks,
            timeZones = timeZones
        )

        self.__userCache[handle.casefold()] = user
        return user

    def __createUsers(self, jsonContents: dict[str, Any]) -> list[User]:
        if not isinstance(jsonContents, dict):
            raise TypeError(f'jsonContents argument is malformed: \"{jsonContents}\"')

        users: list[User] = list()

        for key, userJson in jsonContents.items():
            user = self.__createUser(key, userJson)
            users.append(user)

        if len(users) == 0:
            raise NoUsersException(f'Unable to read in any users from users repository file: \"{self.__usersFile}\"')

        users.sort(key = lambda user: user.getHandle().casefold())
        return users

    def __findAndCreateUser(self, handle: str, jsonContents: dict[str, Any]) -> User:
        if not utils.isValidStr(handle):
            raise TypeError(f'handle argument is malformed: \"{handle}\"')
        elif jsonContents is None:
            raise TypeError(f'jsonContents argument is malformed: \"{jsonContents}\"')

        user = self.__userCache.get(handle.casefold(), None)

        if user is not None:
            return user

        for key, userJson in jsonContents.items():
            if handle.casefold() == key.casefold():
                return self.__createUser(handle, userJson)

        raise NoSuchUserException(f'Unable to find user with handle \"{handle}\" in users repository file: \"{self.__usersFile}\"')

    def getUser(self, handle: str) -> User:
        if not utils.isValidStr(handle):
            raise TypeError(f'handle argument is malformed: \"{handle}\"')

        jsonContents = self.__readJson()
        return self.__findAndCreateUser(handle, jsonContents)

    async def getUserAsync(self, handle: str) -> User:
        if not utils.isValidStr(handle):
            raise TypeError(f'handle argument is malformed: \"{handle}\"')

        jsonContents = await self.__readJsonAsync()
        return self.__findAndCreateUser(handle, jsonContents)

    def getUsers(self) -> list[User]:
        jsonContents = self.__readJson()
        return self.__createUsers(jsonContents)

    async def getUsersAsync(self) -> list[User]:
        jsonContents = await self.__readJsonAsync()
        return self.__createUsers(jsonContents)

    async def modifyUserValue(self, handle: str, jsonConstant: UserJsonConstant, value: Any | None):
        if not utils.isValidStr(handle):
            raise TypeError(f'handle argument is malformed: \"{handle}\"')
        elif not isinstance(jsonConstant, UserJsonConstant):
            raise TypeError(f'jsonConstant argument is malformed: \"{jsonConstant}\"')

        jsonContents = await self.__readJsonAsync()
        userJson = jsonContents.get(handle.casefold())

        if not isinstance(userJson, dict):
            raise NoSuchUserException(f'Unable to find user with handle \"{handle}\" in users repository file: \"{self.__usersFile}\"')

        match jsonConstant:
            case UserJsonConstant.ANIV_MESSAGE_COPY_TIMEOUT_ENABLED:
                await self.__modifyUserBooleanValue(
                    handle = handle,
                    userJson = userJson,
                    jsonConstant = jsonConstant,
                    rawValue = value
                )

            case UserJsonConstant.CHEER_ACTIONS_ENABLED:
                await self.__modifyUserBooleanValue(
                    handle = handle,
                    userJson = userJson,
                    jsonConstant = jsonConstant,
                    rawValue = value
                )

            case UserJsonConstant.TTS_ENABLED:
                await self.__modifyUserBooleanValue(
                    handle = handle,
                    userJson = userJson,
                    jsonConstant = jsonConstant,
                    rawValue = value
                )

            case _:
                raise NotImplementedError(f'Modifying this UserJsonConstant is not implemented ({handle=}) ({jsonConstant=}) ({value=})')

        await self.__writeAndFlushUsersFileAsync(jsonContents)
        self.__timber.log('UsersRepository', f'Finished modifying user value ({handle=}) ({jsonConstant=}) ({value=})')

    async def __modifyUserBooleanValue(
        self,
        handle: str,
        userJson: dict[str, Any],
        jsonConstant: UserJsonConstant,
        rawValue: Any | None
    ):
        if not utils.isValidStr(handle):
            raise TypeError(f'handle argument is malformed: \"{handle}\"')
        elif not isinstance(userJson, dict):
            raise TypeError(f'userJson argument is malformed: \"{userJson}\"')
        elif not isinstance(jsonConstant, UserJsonConstant):
            raise TypeError(f'jsonConstant argument is malformed: \"{jsonConstant}\"')

        value: bool | None

        if isinstance(rawValue, str):
            value = utils.strictStrToBool(rawValue)
        elif utils.isValidBool(rawValue):
            value = rawValue
        else:
            raise BadModifyUserValueException(f'Bad modify user value! ({handle=}) ({jsonConstant=}) ({rawValue=})')

        userJson[jsonConstant.jsonKey] = value

    def __parseCutenessBoosterPacksFromJson(
        self,
        jsonList: list[dict[str, Any]] | None
    ) -> list[CutenessBoosterPack] | None:
        if jsonList is not None and not isinstance(jsonList, list):
            raise TypeError(f'jsonList argument is malformed: \"{jsonList}\"')
        elif jsonList is None:
            return None

        cutenessBoosterPacks: list[CutenessBoosterPack] = list()

        for cutenessBoosterPackJson in jsonList:
            cutenessBoosterPacks.append(CutenessBoosterPack(
                amount = utils.getIntFromDict(cutenessBoosterPackJson, 'amount'),
                rewardId = utils.getStrFromDict(cutenessBoosterPackJson, 'rewardId')
            ))

        cutenessBoosterPacks.sort(key = lambda pack: pack.amount)
        return cutenessBoosterPacks

    def __parsePkmnCatchBoosterPacksFromJson(
        self,
        jsonList: list[dict[str, Any]] | None
    ) -> list[PkmnCatchBoosterPack] | None:
        if not isinstance(jsonList, list) or len(jsonList) == 0:
            return None

        pkmnCatchBoosterPacks: list[PkmnCatchBoosterPack] = list()

        for pkmnCatchBoosterPackJson in jsonList:
            pkmnCatchTypeStr = utils.getStrFromDict(
                d = pkmnCatchBoosterPackJson,
                key = 'catchType',
                fallback = ''
            )

            catchType: PkmnCatchType | None = None
            if utils.isValidStr(pkmnCatchTypeStr):
                catchType = PkmnCatchType.fromStr(pkmnCatchTypeStr)

            pkmnCatchBoosterPacks.append(PkmnCatchBoosterPack(
                catchType = catchType,
                rewardId = utils.getStrFromDict(pkmnCatchBoosterPackJson, 'rewardId')
            ))

        return pkmnCatchBoosterPacks

    def __parseSoundAlertRedemptionsFromJson(
        self,
        jsonList: list[dict[str, Any]] | None
    ) -> dict[str, SoundAlertRedemption] | None:
        if not isinstance(jsonList, list) or len(jsonList) == 0:
            return None

        redemptions: dict[str, SoundAlertRedemption] = dict()

        for soundAlertJson in jsonList:
            soundAlertString = utils.getStrFromDict(soundAlertJson, 'soundAlert', '')
            soundAlert = self.__soundAlertJsonMapper.parseSoundAlert(soundAlertString)

            if soundAlert is None:
                self.__timber.log('UsersRepository', f'Unable to read string into a valid SoundAlert value ({soundAlertJson=}) ({soundAlertString=}) ({soundAlert=})')
                continue

            isImmediate = utils.getBoolFromDict(soundAlertJson, 'isImmediate', False)
            rewardId = utils.getStrFromDict(soundAlertJson, 'rewardId')

            directoryPath: str | None = None
            if 'directoryPath' in soundAlertJson and utils.isValidStr(soundAlertJson.get('directoryPath')):
                directoryPath = utils.getStrFromDict(soundAlertJson, 'directoryPath')

            redemptions[rewardId] = SoundAlertRedemption(
                isImmediate = isImmediate,
                soundAlert = soundAlert,
                directoryPath = directoryPath,
                rewardId = rewardId
            )

        return redemptions

    def __readJson(self) -> dict[str, Any]:
        if self.__jsonCache is not None:
            return self.__jsonCache

        if not os.path.exists(self.__usersFile):
            raise FileNotFoundError(f'Users repository file not found: \"{self.__usersFile}\"')

        with open(self.__usersFile, mode = 'r') as file:
            jsonContents = json.load(file)

        if jsonContents is None:
            raise IOError(f'Error reading from users repository file: \"{self.__usersFile}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of users repository file \"{self.__usersFile}\" is empty')

        self.__jsonCache = jsonContents
        return jsonContents

    async def __readJsonAsync(self) -> dict[str, Any]:
        if self.__jsonCache is not None:
            return self.__jsonCache

        if not await aiofiles.ospath.exists(self.__usersFile):
            raise FileNotFoundError(f'Users repository file not found: \"{self.__usersFile}\"')

        async with aiofiles.open(self.__usersFile, mode = 'r', encoding = 'utf-8') as file:
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
            raise TypeError(f'handle argument is malformed: \"{handle}\"')

        self.__timber.log('UsersRepository', f'Removing user \"{handle}\"...')
        await self.setUserEnabled(handle, False)
        self.__timber.log('UsersRepository', f'Finished removing user \"{handle}\"')

    async def setUserEnabled(self, handle: str, enabled: bool):
        if not utils.isValidStr(handle):
            raise TypeError(f'handle argument is malformed: \"{handle}\"')
        elif not utils.isValidBool(enabled):
            raise TypeError(f'enabled argument is malformed: \"{enabled}\"')

        self.__timber.log('UsersRepository', f'Changing enabled status for user \"{handle}\" to \"{enabled}\"...')
        jsonContents = await self.__readJsonAsync()
        preExistingHandle: str | None = None

        for key in jsonContents.keys():
            if key.casefold() == handle.casefold():
                preExistingHandle = key
                break

        if not utils.isValidStr(preExistingHandle):
            self.__timber.log('UsersRepository', f'Unable to change enabled status for user \"{handle}\" as no user with that handle currently exists')
            return

        jsonContents[preExistingHandle]['enabled'] = enabled
        await self.__writeAndFlushUsersFileAsync(jsonContents)
        self.__timber.log('UsersRepository', f'Finished changing enabled status for user ({handle=}) ({enabled=})')

    async def __writeAndFlushUsersFileAsync(self, jsonContents: dict[str, Any]):
        if not isinstance(jsonContents, dict):
            raise TypeError(f'jsonContents argument is malformed: \"{jsonContents}\"')

        async with aiofiles.open(self.__usersFile, mode = 'w', encoding = 'utf-8') as file:
            jsonString = json.dumps(jsonContents, indent = 4, sort_keys = True)
            await file.write(jsonString)
            await file.flush()

        # be sure to clear caches, as JSON file contents have now been updated
        await self.clearCaches()

        self.__timber.log('UsersRepository', f'Finished writing out changes to users repository JSON file (\"{self.__usersFile}\")')
