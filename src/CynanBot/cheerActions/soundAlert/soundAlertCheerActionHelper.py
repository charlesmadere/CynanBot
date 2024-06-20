from datetime import datetime, timedelta

import CynanBot.misc.utils as utils
from CynanBot.cheerActions.cheerAction import CheerAction
from CynanBot.cheerActions.cheerActionBitRequirement import \
    CheerActionBitRequirement
from CynanBot.cheerActions.cheerActionStreamStatusRequirement import \
    CheerActionStreamStatusRequirement
from CynanBot.streamAlertsManager.immediateStreamAlertsManagerInterface import \
    ImmediateStreamAlertsManagerInterface
from CynanBot.cheerActions.cheerActionType import CheerActionType
from CynanBot.cheerActions.soundAlert.soundAlertCheerActionHelperInterface import \
    SoundAlertCheerActionHelperInterface
from CynanBot.location.timeZoneRepositoryInterface import \
    TimeZoneRepositoryInterface
from CynanBot.streamAlertsManager.streamAlert import StreamAlert
from CynanBot.soundPlayerManager.soundPlayerRandomizerHelperInterface import \
    SoundPlayerRandomizerHelperInterface
from CynanBot.streamAlertsManager.streamAlertsManagerInterface import \
    StreamAlertsManagerInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.tts.ttsEvent import TtsEvent
from CynanBot.tts.ttsProvider import TtsProvider
from CynanBot.twitch.configuration.twitchChannelProvider import \
    TwitchChannelProvider
from CynanBot.twitch.configuration.twitchMessageable import TwitchMessageable
from CynanBot.twitch.isLiveOnTwitchRepositoryInterface import \
    IsLiveOnTwitchRepositoryInterface
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBot.users.userInterface import UserInterface


class SoundAlertCheerActionHelper(SoundAlertCheerActionHelperInterface):

    def __init__(
        self,
        immediateStreamAlertsManager: ImmediateStreamAlertsManagerInterface,
        isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface,
        soundPlayerRandomizerHelper: SoundPlayerRandomizerHelperInterface,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        minimumFollowDuration: timedelta = timedelta(weeks = 1)
    ):
        if not isinstance(immediateStreamAlertsManager, ImmediateStreamAlertsManagerInterface):
            raise TypeError(f'immediateStreamAlertsManager argument is malformed: \"{immediateStreamAlertsManager}\"')
        elif not isinstance(isLiveOnTwitchRepository, IsLiveOnTwitchRepositoryInterface):
            raise TypeError(f'isLiveOnTwitchRepository argument is malformed: \"{isLiveOnTwitchRepository}\"')
        elif not isinstance(soundPlayerRandomizerHelper, SoundPlayerRandomizerHelperInterface):
            raise TypeError(f'soundPlayerRandomizerHelper argument is malformed: \"{soundPlayerRandomizerHelper}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(minimumFollowDuration, timedelta):
            raise TypeError(f'minimumFollowDuration argument is malformed: \"{minimumFollowDuration}\"')

        self.__immediateStreamAlertsManager: ImmediateStreamAlertsManagerInterface = immediateStreamAlertsManager
        self.__isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface = isLiveOnTwitchRepository
        self.__soundPlayerRandomizerHelper: SoundPlayerRandomizerHelperInterface = soundPlayerRandomizerHelper
        self.__streamAlertsManager: StreamAlertsManagerInterface = streamAlertsManager
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__minimumFollowDuration: timedelta = minimumFollowDuration

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def handleSoundAlertCheerAction(
        self,
        bits: int,
        actions: list[CheerAction],
        broadcasterUserId: str,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        moderatorTwitchAccessToken: str,
        moderatorUserId: str,
        userTwitchAccessToken: str,
        user: UserInterface
    ) -> bool:
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 0 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif not isinstance(actions, list):
            raise TypeError(f'actions argument is malformed: \"{actions}\"')
        elif not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not utils.isValidStr(cheerUserId):
            raise TypeError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserName):
            raise TypeError(f'cheerUserName argument is malformed: \"{cheerUserName}\"')
        elif not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(moderatorTwitchAccessToken):
            raise TypeError(f'moderatorTwitchAccessToken argument is malformed: \"{moderatorTwitchAccessToken}\"')
        elif not utils.isValidStr(moderatorUserId):
            raise TypeError(f'moderatorUserId argument is malformed: \"{moderatorUserId}\"')
        elif not utils.isValidStr(userTwitchAccessToken):
            raise TypeError(f'userTwitchAccessToken argument is malformed: \"{userTwitchAccessToken}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        if not user.areSoundAlertsEnabled():
            return False

        soundAlertActions: list[CheerAction] = list()
        for action in actions:
            if action.actionType is CheerActionType.SOUND_ALERT:
                soundAlertActions.append(action)

        if len(soundAlertActions) == 0:
            return False

        soundAlertActions.sort(key = lambda action: action.amount, reverse = True)
        soundAlertAction: CheerAction | None = None

        for action in soundAlertActions:
            if action.bitRequirement is CheerActionBitRequirement.EXACT and bits == action.amount:
                soundAlertAction = action
                break

        if soundAlertAction is None:
            for action in soundAlertActions:
                if action.bitRequirement is CheerActionBitRequirement.GREATER_THAN_OR_EQUAL_TO and bits >= action.amount:
                    soundAlertAction = action
                    break

        if soundAlertAction is None:
            return False
        elif not utils.isValidStr(soundAlertAction.tag):
            self.__timber.log('SoundAlertCheerActionHelper', f'Encountered a valid sound alert CheerAction instance but it has no tag value, this should be impossible: {soundAlertAction}')
            return False

        return await self.__playSoundAlert(
            bits = bits,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            tag = soundAlertAction.tag,
            twitchChannelId = broadcasterUserId,
            user = user
        )

    async def __playSoundAlert(
        self,
        bits: int,
        cheerUserId: str,
        cheerUserName: str,
        tag: str,
        twitchChannelId: str,
        user: UserInterface
    ) -> bool:
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif not utils.isValidStr(cheerUserId):
            raise TypeError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserName):
            raise TypeError(f'cheerUserName argument is malformed: \"{cheerUserName}\"')
        elif not utils.isValidStr(tag):
            raise TypeError(f'tag argument is malformed: \"{tag}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        if not user.areSoundAlertsEnabled():
            return False

        soundAlertPath = await self.__soundPlayerRandomizerHelper.chooseRandomFromDirectorySoundAlert(
            directoryPath = tag
        )

        if not utils.isValidStr(soundAlertPath):
            return False

        return await self.__immediateStreamAlertsManager.playSoundFile(
            file = soundAlertPath
        )

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider

    async def __verifyStreamStatus(
        self,
        soundAlertAction: CheerAction,
        twitchChannelId: str,
        user: UserInterface
    ) -> bool:
        if not isinstance(soundAlertAction, CheerAction):
            raise TypeError(f'timeoutAction argument is malformed: \"{soundAlertAction}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        requirement = soundAlertAction.streamStatusRequirement
        if requirement is CheerActionStreamStatusRequirement.ANY:
            return True

        isLive = await self.__isLiveOnTwitchRepository.isLive(twitchChannelId)
        return isLive and requirement is CheerActionStreamStatusRequirement.ONLINE or \
            not isLive and requirement is CheerActionStreamStatusRequirement.OFFLINE
