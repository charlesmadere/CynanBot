import json
import os
from datetime import tzinfo
from typing import Any, Collection

import aiofiles
import aiofiles.ospath
from frozendict import frozendict
from frozenlist import FrozenList

from .aniv.anivUserSettingsJsonParserInterface import AnivUserSettingsJsonParserInterface
from .aniv.whichAnivUser import WhichAnivUser
from .chatSoundAlert.absChatSoundAlert import AbsChatSoundAlert
from .chatSoundAlert.chatSoundAlertJsonParserInterface import ChatSoundAlertJsonParserInterface
from .crowdControl.crowdControlBoosterPack import CrowdControlBoosterPack
from .crowdControl.crowdControlJsonParserInterface import CrowdControlJsonParserInterface
from .cuteness.cutenessBoosterPack import CutenessBoosterPack
from .cuteness.cutenessBoosterPackJsonParserInterface import CutenessBoosterPackJsonParserInterface
from .decTalkSongs.decTalkSongBoosterPack import DecTalkSongBoosterPack
from .decTalkSongs.decTalkSongBoosterPackParserInterface import DecTalkSongBoosterPackParserInterface
from .exceptions import BadModifyUserValueException, NoSuchUserException, NoUsersException
from .pkmn.pkmnBoosterPackJsonParserInterface import PkmnBoosterPackJsonParserInterface
from .pkmn.pkmnCatchBoosterPack import PkmnCatchBoosterPack
from .soundAlert.soundAlertRedemption import SoundAlertRedemption
from .soundAlert.soundAlertRedemptionJsonParserInterface import SoundAlertRedemptionJsonParserInterface
from .timeout.timeoutBoosterPackJsonParserInterface import TimeoutBoosterPackJsonParserInterface
from .tts.ttsBoosterPack import TtsBoosterPack
from .tts.ttsBoosterPackParserInterface import TtsBoosterPackParserInterface
from .user import User
from .userJsonConstant import UserJsonConstant
from .usersRepositoryInterface import UsersRepositoryInterface
from ..language.jsonMapper.languageEntryJsonMapperInterface import LanguageEntryJsonMapperInterface
from ..language.languageEntry import LanguageEntry
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..tts.jsonMapper.ttsJsonMapperInterface import TtsJsonMapperInterface
from ..tts.models.ttsProvider import TtsProvider


class UsersRepository(UsersRepositoryInterface):

    def __init__(
        self,
        anivUserSettingsJsonParser: AnivUserSettingsJsonParserInterface,
        chatSoundAlertJsonParser: ChatSoundAlertJsonParserInterface,
        crowdControlJsonParser: CrowdControlJsonParserInterface,
        cutenessBoosterPackJsonParser: CutenessBoosterPackJsonParserInterface,
        decTalkSongBoosterPackParser: DecTalkSongBoosterPackParserInterface,
        languageEntryJsonMapper: LanguageEntryJsonMapperInterface,
        pkmnBoosterPackJsonParser: PkmnBoosterPackJsonParserInterface,
        soundAlertRedemptionJsonParser: SoundAlertRedemptionJsonParserInterface,
        timber: TimberInterface,
        timeoutBoosterPackJsonParser: TimeoutBoosterPackJsonParserInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        ttsBoosterPackParser: TtsBoosterPackParserInterface,
        ttsJsonMapper: TtsJsonMapperInterface,
        usersFile: str = '../config/usersRepository.json'
    ):
        if not isinstance(anivUserSettingsJsonParser, AnivUserSettingsJsonParserInterface):
            raise TypeError(f'anivUserSettingsJsonParser argument is malformed: \"{anivUserSettingsJsonParser}\"')
        elif not isinstance(chatSoundAlertJsonParser, ChatSoundAlertJsonParserInterface):
            raise TypeError(f'chatSoundAlertJsonParser argument is malformed: \"{chatSoundAlertJsonParser}\"')
        elif not isinstance(crowdControlJsonParser, CrowdControlJsonParserInterface):
            raise TypeError(f'crowdControlJsonParser argument is malformed: \"{crowdControlJsonParser}\"')
        elif not isinstance(cutenessBoosterPackJsonParser, CutenessBoosterPackJsonParserInterface):
            raise TypeError(f'cutenessBoosterPackJsonParser argument is malformed: \"{cutenessBoosterPackJsonParser}\"')
        elif not isinstance(decTalkSongBoosterPackParser, DecTalkSongBoosterPackParserInterface):
            raise TypeError(f'decTalkSongBoosterPackParser argument is malformed: \"{decTalkSongBoosterPackParser}\"')
        elif not isinstance(languageEntryJsonMapper, LanguageEntryJsonMapperInterface):
            raise TypeError(f'languageEntryJsonMapper argument is malformed: \"{languageEntryJsonMapper}\"')
        elif not isinstance(pkmnBoosterPackJsonParser, PkmnBoosterPackJsonParserInterface):
            raise TypeError(f'pkmnBoosterPackJsonParser argument is malformed: \"{pkmnBoosterPackJsonParser}\"')
        elif not isinstance(soundAlertRedemptionJsonParser, SoundAlertRedemptionJsonParserInterface):
            raise TypeError(f'soundAlertRedemptionJsonParser argument is malformed: \"{soundAlertRedemptionJsonParser}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutBoosterPackJsonParser, TimeoutBoosterPackJsonParserInterface):
            raise TypeError(f'timeoutBoosterPackJsonParser argument is malformed: \"{timeoutBoosterPackJsonParser}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(ttsBoosterPackParser, TtsBoosterPackParserInterface):
            raise TypeError(f'ttsBoosterPackParser argument is malformed: \"{ttsBoosterPackParser}\"')
        elif not isinstance(ttsJsonMapper, TtsJsonMapperInterface):
            raise TypeError(f'ttsJsonMapper argument is malformed: \"{ttsJsonMapper}\"')
        elif not utils.isValidStr(usersFile):
            raise TypeError(f'usersFile argument is malformed: \"{usersFile}\"')

        self.__anivUserSettingsJsonParser: AnivUserSettingsJsonParserInterface = anivUserSettingsJsonParser
        self.__chatSoundAlertJsonParser: ChatSoundAlertJsonParserInterface = chatSoundAlertJsonParser
        self.__crowdControlJsonParser: CrowdControlJsonParserInterface = crowdControlJsonParser
        self.__cutenessBoosterPackJsonParser: CutenessBoosterPackJsonParserInterface = cutenessBoosterPackJsonParser
        self.__decTalkSongBoosterPackParser: DecTalkSongBoosterPackParserInterface = decTalkSongBoosterPackParser
        self.__languageEntryJsonMapper: LanguageEntryJsonMapperInterface = languageEntryJsonMapper
        self.__pkmnBoosterPackJsonParser: PkmnBoosterPackJsonParserInterface = pkmnBoosterPackJsonParser
        self.__soundAlertRedemptionJsonParser: SoundAlertRedemptionJsonParserInterface = soundAlertRedemptionJsonParser
        self.__timber: TimberInterface = timber
        self.__timeoutBoosterPackJsonParser: TimeoutBoosterPackJsonParserInterface = timeoutBoosterPackJsonParser
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__ttsBoosterPackParser: TtsBoosterPackParserInterface = ttsBoosterPackParser
        self.__ttsJsonMapper: TtsJsonMapperInterface = ttsJsonMapper
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

        areAsplodieStatsEnabled = utils.getBoolFromDict(userJson, UserJsonConstant.ASPLODIE_STATS_ENABLED.jsonKey, False)
        areBeanStatsEnabled = utils.getBoolFromDict(userJson, UserJsonConstant.BEAN_STATS_ENABLED.jsonKey, False)
        areChatSoundAlertsEnabled = utils.getBoolFromDict(userJson, UserJsonConstant.CHAT_SOUND_ALERTS_ENABLED.jsonKey, False)
        areCheerActionsEnabled = utils.getBoolFromDict(userJson, UserJsonConstant.CHEER_ACTIONS_ENABLED.jsonKey, False)
        areRecurringActionsEnabled = utils.getBoolFromDict(userJson, 'recurringActionsEnabled', True)
        areSoundAlertsEnabled = utils.getBoolFromDict(userJson, 'soundAlertsEnabled', False)
        areTtsChattersEnabled = utils.getBoolFromDict(userJson, 'ttsChattersEnabled', False)
        isAnivContentScanningEnabled = utils.getBoolFromDict(userJson, UserJsonConstant.ANIV_CONTENT_SCANNING_ENABLED.jsonKey, False)
        isAnivMessageCopyTimeoutChatReportingEnabled = utils.getBoolFromDict(userJson, UserJsonConstant.ANIV_MESSAGE_COPY_TIMEOUT_CHAT_REPORTING_ENABLED.jsonKey, True)
        isAnivMessageCopyTimeoutEnabled = utils.getBoolFromDict(userJson, UserJsonConstant.ANIV_MESSAGE_COPY_TIMEOUT_ENABLED.jsonKey, False)
        isCasualGamePollEnabled = utils.getBoolFromDict(userJson, 'casualGamePollEnabled', False)
        isChannelPredictionChartEnabled = utils.getBoolFromDict(userJson, 'channelPredictionChartEnabled', False)
        isChatBackMessagesEnabled = utils.getBoolFromDict(userJson, 'chatBackMessagesEnabled', False)
        isChatBandEnabled = utils.getBoolFromDict(userJson, 'chatBandEnabled', False)
        isChatLoggingEnabled = utils.getBoolFromDict(userJson, 'chatLoggingEnabled', False)
        isChatterPreferredTtsEnabled = utils.getBoolFromDict(userJson, UserJsonConstant.CHATTER_PREFERRED_TTS_ENABLED.jsonKey, False)
        isCrowdControlEnabled = utils.getBoolFromDict(userJson, UserJsonConstant.CROWD_CONTROL_ENABLED.jsonKey, False)
        isCutenessEnabled = utils.getBoolFromDict(userJson, 'cutenessEnabled', False)
        isDecTalkSongsEnabled = utils.getBoolFromDict(userJson, 'decTalkSongsEnabled', False)
        isEccoEnabled = utils.getBoolFromDict(userJson, UserJsonConstant.ECCO_ENABLED.jsonKey, False)
        isEnabled = utils.getBoolFromDict(userJson, UserJsonConstant.ENABLED.jsonKey, True)
        isGiveCutenessEnabled = utils.getBoolFromDict(userJson, 'giveCutenessEnabled', False)
        isJishoEnabled = utils.getBoolFromDict(userJson, 'jishoEnabled', False)
        isLoremIpsumEnabled = utils.getBoolFromDict(userJson, 'loremIpsumEnabled', True)
        isNotifyOfPollResultsEnabled = utils.getBoolFromDict(userJson, 'notifyOfPollResultsEnabled', True)
        isNotifyOfPollStartEnabled = utils.getBoolFromDict(userJson, 'notifyOfPollStartEnabled', True)
        isNotifyOfPredictionResultsEnabled = utils.getBoolFromDict(userJson, 'notifyOfPredictionResultsEnabled', True)
        isNotifyOfPredictionStartEnabled = utils.getBoolFromDict(userJson, 'notifyOfPredictionStartEnabled', True)
        isPkmnEnabled = utils.getBoolFromDict(userJson, 'pkmnEnabled', False)
        isPokepediaEnabled = utils.getBoolFromDict(userJson, 'pokepediaEnabled', False)
        isRaceEnabled = utils.getBoolFromDict(userJson, 'raceEnabled', False)
        isStarWarsQuotesEnabled = utils.getBoolFromDict(userJson, 'starWarsQuotesEnabled', False)
        isSubGiftThankingEnabled = utils.getBoolFromDict(userJson, 'subGiftThankingEnabled', True)
        isSupStreamerEnabled = utils.getBoolFromDict(userJson, 'supStreamerEnabled', False)
        isTimeoutCheerActionIncreasedBullyFailureEnabled = utils.getBoolFromDict(userJson, 'timeoutCheerActionIncreasedBullyFailureEnabled', True)
        isTimeoutCheerActionFailureEnabled = utils.getBoolFromDict(userJson, 'timeoutCheerActionFailureEnabled', True)
        isTimeoutCheerActionReverseEnabled = utils.getBoolFromDict(userJson, 'timeoutCheerActionReverseEnabled', True)
        isTranslateEnabled = utils.getBoolFromDict(userJson, 'translateEnabled', False)
        isTriviaGameEnabled = utils.getBoolFromDict(userJson, 'triviaGameEnabled', False)
        isTriviaScoreEnabled = utils.getBoolFromDict(userJson, 'triviaScoreEnabled', isTriviaGameEnabled)
        isTtsEnabled = utils.getBoolFromDict(userJson, UserJsonConstant.TTS_ENABLED.jsonKey, False)
        isTtsMonsterApiUsageReportingEnabled = utils.getBoolFromDict(userJson, UserJsonConstant.TTS_MONSTER_API_USAGE_REPORTING_ENABLED.jsonKey, True)
        isVoicemailEnabled = utils.getBoolFromDict(userJson, UserJsonConstant.VOICEMAIL_ENABLED.jsonKey, False)
        isVulnerableChattersEnabled = utils.getBoolFromDict(userJson, UserJsonConstant.VULNERABLE_CHATTERS_ENABLED.jsonKey, False)
        isWeatherEnabled = utils.getBoolFromDict(userJson, 'weatherEnabled', False)
        isWordOfTheDayEnabled = utils.getBoolFromDict(userJson, 'wordOfTheDayEnabled', False)
        blueSkyUrl = utils.getStrFromDict(userJson, UserJsonConstant.BLUE_SKY_URL.jsonKey, '')
        casualGamePollRewardId = utils.getStrFromDict(userJson, 'casualGamePollRewardId', '')
        casualGamePollUrl = utils.getStrFromDict(userJson, 'casualGamePollUrl', '')
        discordUrl = utils.getStrFromDict(userJson, UserJsonConstant.DISCORD_URL.jsonKey, '')
        instagram = utils.getStrFromDict(userJson, 'instagram', '')
        locationId = utils.getStrFromDict(userJson, 'locationId', '')
        mastodonUrl = utils.getStrFromDict(userJson, 'mastodonUrl', '')
        randomSoundAlertRewardId = utils.getStrFromDict(userJson, 'randomSoundAlertRewardId', '')
        setChatterPreferredTtsRewardId = utils.getStrFromDict(userJson, 'setChatterPreferredTtsRewardId', '')
        soundAlertRewardId = utils.getStrFromDict(userJson, 'soundAlertRewardId', '')
        speedrunProfile = utils.getStrFromDict(userJson, 'speedrunProfile', '')
        supStreamerMessage = utils.getStrFromDict(userJson, 'supStreamerMessage', '')
        ttsChatterRewardId = utils.getStrFromDict(userJson, 'ttsChatterRewardId', '')
        voicemailRewardId = utils.getStrFromDict(userJson, 'voicemailRewardId', '')

        defaultLanguageString = utils.getStrFromDict(
            d = userJson,
            key = 'defaultLanguage',
            fallback = self.__languageEntryJsonMapper.serializeLanguageEntry(LanguageEntry.ENGLISH)
        )

        defaultLanguage = self.__languageEntryJsonMapper.requireLanguageEntry(defaultLanguageString)

        anivMessageCopyTimeoutProbability: float | None = None
        anivMessageCopyMaxAgeSeconds: int | None = None
        anivMessageCopyTimeoutMinSeconds: int | None = None
        anivMessageCopyTimeoutMaxSeconds: int | None = None
        if isAnivMessageCopyTimeoutEnabled:
            if 'anivMessageCopyTimeoutProbability' in userJson and utils.isValidNum(userJson.get('anivMessageCopyTimeoutProbability')):
                anivMessageCopyTimeoutProbability = utils.getFloatFromDict(userJson, 'anivMessageCopyTimeoutProbability')

            if 'anivMessageCopyMaxAgeSeconds' in userJson and utils.isValidInt(userJson.get('anivMessageCopyMaxAgeSeconds')):
                anivMessageCopyMaxAgeSeconds = utils.getIntFromDict(userJson, 'anivMessageCopyMaxAgeSeconds')

            if 'anivMessageCopyTimeoutMinSeconds' in userJson and utils.isValidInt(userJson.get('anivMessageCopyTimeoutMinSeconds')):
                anivMessageCopyTimeoutMinSeconds = utils.getIntFromDict(userJson, 'anivMessageCopyTimeoutMinSeconds')

            if 'anivMessageCopyTimeoutMaxSeconds' in userJson and utils.isValidInt(userJson.get('anivMessageCopyTimeoutMaxSeconds')):
                anivMessageCopyTimeoutMaxSeconds = utils.getIntFromDict(userJson, 'anivMessageCopyTimeoutMaxSeconds')

        chatSoundAlerts: FrozenList[AbsChatSoundAlert] | None = None
        if areChatSoundAlertsEnabled:
            chatSoundAlertsJson: list[dict[str, Any]] | None = userJson.get('chatSoundAlerts')
            chatSoundAlerts = self.__chatSoundAlertJsonParser.parseChatSoundAlerts(chatSoundAlertsJson)

        decTalkSongBoosterPacks: frozendict[str, DecTalkSongBoosterPack] | None = None
        if isDecTalkSongsEnabled:
            decTalkSongBoosterPacksJson: list[dict[str, Any]] | None = userJson.get('decTalkSongBoosterPacks')
            decTalkSongBoosterPacks = self.__decTalkSongBoosterPackParser.parseBoosterPacks(decTalkSongBoosterPacksJson)

        maximumGrenadesWithinCooldown: int | None = None
        if UserJsonConstant.MAXIMUM_GRENADES_WITHIN_COOLDOWN.jsonKey in userJson and utils.isValidInt(userJson.get(UserJsonConstant.MAXIMUM_GRENADES_WITHIN_COOLDOWN.jsonKey)):
            maximumGrenadesWithinCooldown = utils.getIntFromDict(userJson, UserJsonConstant.MAXIMUM_GRENADES_WITHIN_COOLDOWN.jsonKey)

        maximumTtsCheerAmount: int | None = None
        minimumTtsCheerAmount: int | None = None
        if isTtsEnabled:
            if 'maximumTtsCheerAmount' in userJson and utils.isValidInt(userJson.get('maximumTtsCheerAmount')):
                maximumTtsCheerAmount = utils.getIntFromDict(userJson, 'maximumTtsCheerAmount')

            if 'minimumTtsCheerAmount' in userJson and utils.isValidInt(userJson.get('minimumTtsCheerAmount')):
                minimumTtsCheerAmount = utils.getIntFromDict(userJson, 'minimumTtsCheerAmount')

        cutenessBoosterPacks: frozendict[str, CutenessBoosterPack] | None = None
        if isCutenessEnabled:
            cutenessBoosterPacksJson: list[dict[str, Any]] | None = userJson.get('cutenessBoosterPacks')
            cutenessBoosterPacks = self.__cutenessBoosterPackJsonParser.parseBoosterPacks(cutenessBoosterPacksJson)

        isShinyTriviaEnabled: bool = isTriviaGameEnabled
        isToxicTriviaEnabled: bool = isTriviaGameEnabled
        isSuperTriviaGameEnabled: bool = isTriviaGameEnabled
        isSuperTriviaLotrTimeoutEnabled: bool = False
        superTriviaSubscribeTriggerAmount: float | None = None
        superTriviaCheerTriggerAmount: int | None = None
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
            isSuperTriviaLotrTimeoutEnabled = utils.getBoolFromDict(userJson, 'superTriviaLotrTimeoutEnabled', False)

            if 'superTriviaSubscribeTriggerAmount' in userJson and utils.isValidNum(userJson.get('superTriviaSubscribeTriggerAmount')):
                superTriviaSubscribeTriggerAmount = utils.getFloatFromDict(userJson, 'superTriviaSubscribeTriggerAmount')

            if 'superTriviaCheerTriggerAmount' in userJson and utils.isValidInt(userJson.get('superTriviaCheerTriggerAmount')):
                superTriviaCheerTriggerAmount = utils.getIntFromDict(userJson, 'superTriviaCheerTriggerAmount')

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
        pkmnCatchBoosterPacks: frozendict[str, PkmnCatchBoosterPack] | None = None
        if isPkmnEnabled:
            pkmnBattleRewardId = userJson.get('pkmnBattleRewardId')
            pkmnEvolveRewardId = userJson.get('pkmnEvolveRewardId')
            pkmnShinyRewardId = userJson.get('pkmnShinyRewardId')
            pkmnCatchBoosterPacksJson: list[dict[str, Any]] | None = userJson.get('pkmnCatchBoosterPacks')
            pkmnCatchBoosterPacks = self.__pkmnBoosterPackJsonParser.parseBoosterPacks(pkmnCatchBoosterPacksJson)

        soundAlertRedemptions: frozendict[str, SoundAlertRedemption] | None = None
        if areSoundAlertsEnabled:
            soundAlertRedemptionsJson: list[dict[str, Any]] | None = userJson.get('soundAlertRedemptions')
            soundAlertRedemptions = self.__soundAlertRedemptionJsonParser.parseRedemptions(soundAlertRedemptionsJson)

        timeoutActionFollowShieldDays: int | None = None
        if 'timeoutActionFollowShieldDays' in userJson and utils.isValidInt(userJson.get('timeoutActionFollowShieldDays')):
            timeoutActionFollowShieldDays = utils.getIntFromDict(userJson, 'timeoutActionFollowShieldDays')

        timeoutBoosterPacksJson: list[dict[str, Any]] | None = userJson.get('timeoutBoosterPacks')
        timeoutBoosterPacks = self.__timeoutBoosterPackJsonParser.parseBoosterPacks(timeoutBoosterPacksJson)

        crowdControlButtonPressRewardId: str | None = None
        crowdControlGameShuffleRewardId: str | None = None
        crowdControlBoosterPacks: frozendict[str, CrowdControlBoosterPack] | None = None
        if isCrowdControlEnabled:
            crowdControlButtonPressRewardId = userJson.get('crowdControlButtonPressRewardId')
            crowdControlGameShuffleRewardId = userJson.get('crowdControlGameShuffleRewardId')
            crowdControlBoosterPacksJson: list[dict[str, Any]] | None = userJson.get('crowdControlBoosterPacks')
            crowdControlBoosterPacks = self.__crowdControlJsonParser.parseBoosterPacks(crowdControlBoosterPacksJson)

        defaultTtsProvider = TtsProvider.DEC_TALK
        ttsBoosterPacks: FrozenList[TtsBoosterPack] | None = None
        if isTtsEnabled:
            if 'defaultTtsProvider' in userJson and utils.isValidStr(userJson.get('defaultTtsProvider')):
                defaultTtsProvider = self.__ttsJsonMapper.requireProvider(utils.getStrFromDict(userJson, 'defaultTtsProvider'))

            ttsBoosterPacksJson: list[dict[str, Any]] | None = userJson.get('ttsBoosterPacks')
            ttsBoosterPacks = self.__ttsBoosterPackParser.parseBoosterPacks(ttsBoosterPacksJson)

        whichAnivUser = WhichAnivUser.ANEEV
        if utils.isValidStr(userJson.get(UserJsonConstant.WHICH_ANIV_USER.jsonKey)):
            whichAnivUser = self.__anivUserSettingsJsonParser.requireWhichAnivUser(utils.getStrFromDict(userJson, UserJsonConstant.WHICH_ANIV_USER.jsonKey))

        chatBackMessages: FrozenList[str] | None = None
        if isChatBackMessagesEnabled:
            chatBackMessagesJson: list[str] | Any | None = userJson.get('chatBackMessages', None)
            if isinstance(chatBackMessagesJson, list) and len(chatBackMessagesJson) >= 1:
                chatBackMessages = FrozenList(chatBackMessagesJson)
                chatBackMessages.freeze()

        timeZones: FrozenList[tzinfo] | None = None
        if 'timeZones' in userJson:
            timeZones = self.__timeZoneRepository.getTimeZones(userJson['timeZones'])
        elif 'timeZone' in userJson:
            timeZones = FrozenList()
            timeZones.append(self.__timeZoneRepository.getTimeZone(userJson['timeZone']))
            timeZones.freeze()

        user = User(
            areAsplodieStatsEnabled = areAsplodieStatsEnabled,
            areBeanStatsEnabled = areBeanStatsEnabled,
            areChatSoundAlertsEnabled = areChatSoundAlertsEnabled,
            areCheerActionsEnabled = areCheerActionsEnabled,
            areRecurringActionsEnabled = areRecurringActionsEnabled,
            areSoundAlertsEnabled = areSoundAlertsEnabled,
            isAnivContentScanningEnabled = isAnivContentScanningEnabled,
            isAnivMessageCopyTimeoutChatReportingEnabled = isAnivMessageCopyTimeoutChatReportingEnabled,
            isAnivMessageCopyTimeoutEnabled = isAnivMessageCopyTimeoutEnabled,
            isCasualGamePollEnabled = isCasualGamePollEnabled,
            isChannelPredictionChartEnabled = isChannelPredictionChartEnabled,
            isChatBackMessagesEnabled = isChatBackMessagesEnabled,
            isChatBandEnabled = isChatBandEnabled,
            isChatLoggingEnabled = isChatLoggingEnabled,
            isChatterPreferredTtsEnabled = isChatterPreferredTtsEnabled,
            isCrowdControlEnabled = isCrowdControlEnabled,
            isCutenessEnabled = isCutenessEnabled,
            isDecTalkSongsEnabled = isDecTalkSongsEnabled,
            isEccoEnabled = isEccoEnabled,
            isEnabled = isEnabled,
            isGiveCutenessEnabled = isGiveCutenessEnabled,
            isJishoEnabled = isJishoEnabled,
            isLoremIpsumEnabled = isLoremIpsumEnabled,
            isNotifyOfPollResultsEnabled = isNotifyOfPollResultsEnabled,
            isNotifyOfPollStartEnabled = isNotifyOfPollStartEnabled,
            isNotifyOfPredictionResultsEnabled = isNotifyOfPredictionResultsEnabled,
            isNotifyOfPredictionStartEnabled = isNotifyOfPredictionStartEnabled,
            isPkmnEnabled = isPkmnEnabled,
            isPokepediaEnabled = isPokepediaEnabled,
            isRaceEnabled = isRaceEnabled,
            isShinyTriviaEnabled = isShinyTriviaEnabled,
            isStarWarsQuotesEnabled = isStarWarsQuotesEnabled,
            isSubGiftThankingEnabled = isSubGiftThankingEnabled,
            isSuperTriviaGameEnabled = isSuperTriviaGameEnabled,
            isSuperTriviaLotrTimeoutEnabled = isSuperTriviaLotrTimeoutEnabled,
            isSupStreamerEnabled = isSupStreamerEnabled,
            isTimeoutCheerActionIncreasedBullyFailureEnabled = isTimeoutCheerActionIncreasedBullyFailureEnabled,
            isTimeoutCheerActionFailureEnabled = isTimeoutCheerActionFailureEnabled,
            isTimeoutCheerActionReverseEnabled = isTimeoutCheerActionReverseEnabled,
            isToxicTriviaEnabled = isToxicTriviaEnabled,
            isTranslateEnabled = isTranslateEnabled,
            isTriviaGameEnabled = isTriviaGameEnabled,
            isTriviaScoreEnabled = isTriviaScoreEnabled,
            areTtsChattersEnabled = areTtsChattersEnabled,
            isTtsEnabled = isTtsEnabled,
            isTtsMonsterApiUsageReportingEnabled = isTtsMonsterApiUsageReportingEnabled,
            isVoicemailEnabled = isVoicemailEnabled,
            isVulnerableChattersEnabled = isVulnerableChattersEnabled,
            isWeatherEnabled = isWeatherEnabled,
            isWordOfTheDayEnabled = isWordOfTheDayEnabled,
            anivMessageCopyTimeoutProbability = anivMessageCopyTimeoutProbability,
            superTriviaSubscribeTriggerAmount = superTriviaSubscribeTriggerAmount,
            anivMessageCopyMaxAgeSeconds = anivMessageCopyMaxAgeSeconds,
            anivMessageCopyTimeoutMinSeconds = anivMessageCopyTimeoutMinSeconds,
            anivMessageCopyTimeoutMaxSeconds = anivMessageCopyTimeoutMaxSeconds,
            maximumGrenadesWithinCooldown = maximumGrenadesWithinCooldown,
            maximumTtsCheerAmount = maximumTtsCheerAmount,
            minimumTtsCheerAmount = minimumTtsCheerAmount,
            superTriviaCheerTriggerAmount = superTriviaCheerTriggerAmount,
            superTriviaCheerTriggerMaximum = superTriviaCheerTriggerMaximum,
            superTriviaGamePoints = superTriviaGamePoints,
            superTriviaGameRewardId = superTriviaGameRewardId,
            superTriviaGameShinyMultiplier = superTriviaGameShinyMultiplier,
            superTriviaGameToxicMultiplier = superTriviaGameToxicMultiplier,
            superTriviaGameToxicPunishmentMultiplier = superTriviaGameToxicPunishmentMultiplier,
            superTriviaPerUserAttempts = superTriviaPerUserAttempts,
            superTriviaSubscribeTriggerMaximum = superTriviaSubscribeTriggerMaximum,
            timeoutActionFollowShieldDays = timeoutActionFollowShieldDays,
            triviaGamePoints = triviaGamePoints,
            triviaGameShinyMultiplier = triviaGameShinyMultiplier,
            ttsChatterRewardId = ttsChatterRewardId,
            voicemailRewardId = voicemailRewardId,
            waitForSuperTriviaAnswerDelay = waitForSuperTriviaAnswerDelay,
            waitForTriviaAnswerDelay = waitForTriviaAnswerDelay,
            defaultLanguage = defaultLanguage,
            blueSkyUrl = blueSkyUrl,
            casualGamePollRewardId = casualGamePollRewardId,
            casualGamePollUrl = casualGamePollUrl,
            crowdControlButtonPressRewardId = crowdControlButtonPressRewardId,
            crowdControlGameShuffleRewardId = crowdControlGameShuffleRewardId,
            discordUrl = discordUrl,
            handle = handle,
            instagram = instagram,
            locationId = locationId,
            mastodonUrl = mastodonUrl,
            pkmnBattleRewardId = pkmnBattleRewardId,
            pkmnEvolveRewardId = pkmnEvolveRewardId,
            pkmnShinyRewardId = pkmnShinyRewardId,
            randomSoundAlertRewardId = randomSoundAlertRewardId,
            setChatterPreferredTtsRewardId = setChatterPreferredTtsRewardId,
            speedrunProfile = speedrunProfile,
            soundAlertRewardId = soundAlertRewardId,
            supStreamerMessage = supStreamerMessage,
            triviaGameRewardId = triviaGameRewardId,
            defaultTtsProvider = defaultTtsProvider,
            whichAnivUser = whichAnivUser,
            crowdControlBoosterPacks = crowdControlBoosterPacks,
            cutenessBoosterPacks = cutenessBoosterPacks,
            decTalkSongBoosterPacks = decTalkSongBoosterPacks,
            pkmnCatchBoosterPacks = pkmnCatchBoosterPacks,
            soundAlertRedemptions = soundAlertRedemptions,
            timeoutBoosterPacks = timeoutBoosterPacks,
            chatSoundAlerts = chatSoundAlerts,
            chatBackMessages = chatBackMessages,
            ttsBoosterPacks = ttsBoosterPacks,
            timeZones = timeZones,
        )

        self.__userCache[handle.casefold()] = user
        return user

    def __createUsers(self, jsonContents: dict[str, Any]) -> FrozenList[User]:
        if not isinstance(jsonContents, dict):
            raise TypeError(f'jsonContents argument is malformed: \"{jsonContents}\"')

        users: list[User] = list()

        for key, userJson in jsonContents.items():
            user = self.__createUser(key, userJson)
            users.append(user)

        if len(users) == 0:
            raise NoUsersException(f'Unable to read in any users from users repository file: \"{self.__usersFile}\"')

        users.sort(key = lambda element: element.handle.casefold())
        frozenUsers: FrozenList[User] = FrozenList(users)
        frozenUsers.freeze()

        return frozenUsers

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

    def getUsers(self) -> Collection[User]:
        jsonContents = self.__readJson()
        return self.__createUsers(jsonContents)

    async def getUsersAsync(self) -> Collection[User]:
        jsonContents = await self.__readJsonAsync()
        return self.__createUsers(jsonContents)

    async def modifyUserValue(
        self,
        handle: str,
        jsonConstant: UserJsonConstant,
        value: Any | None
    ):
        if not utils.isValidStr(handle):
            raise TypeError(f'handle argument is malformed: \"{handle}\"')
        elif not isinstance(jsonConstant, UserJsonConstant):
            raise TypeError(f'jsonConstant argument is malformed: \"{jsonConstant}\"')

        jsonContents = await self.__readJsonAsync()
        userJson = jsonContents.get(handle.casefold(), None)

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

            case UserJsonConstant.BLUE_SKY_URL:
                await self.__modifyUserStringValue(
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

            case UserJsonConstant.CROWD_CONTROL_ENABLED:
                await self.__modifyUserBooleanValue(
                    handle = handle,
                    userJson = userJson,
                    jsonConstant = jsonConstant,
                    rawValue = value
                )

            case UserJsonConstant.DISCORD_URL:
                await self.__modifyUserStringValue(
                    handle = handle,
                    userJson = userJson,
                    jsonConstant = jsonConstant,
                    rawValue = value
                )

            case UserJsonConstant.RECURRING_ACTIONS_ENABLED:
                await self.__modifyUserBooleanValue(
                    handle = handle,
                    userJson = userJson,
                    jsonConstant = jsonConstant,
                    rawValue = value
                )

            case UserJsonConstant.SOUND_ALERTS_ENABLED:
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

    async def __modifyUserStringValue(
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

        value: str | None

        if isinstance(rawValue, str):
            value = rawValue
        else:
            raise BadModifyUserValueException(f'Bad modify user value! ({handle=}) ({jsonConstant=}) ({rawValue=})')

        userJson[jsonConstant.jsonKey] = value

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

        jsonContents[preExistingHandle][UserJsonConstant.ENABLED.jsonKey] = enabled
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
