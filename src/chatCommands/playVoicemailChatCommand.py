import re
from typing import Collection, Final, Pattern

from .absChatCommand import AbsChatCommand
from .chatCommandResult import ChatCommandResult
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..streamAlertsManager.streamAlert import StreamAlert
from ..streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ..timber.timberInterface import TimberInterface
from ..tts.models.ttsEvent import TtsEvent
from ..tts.models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ..tts.provider.compositeTtsManagerProviderInterface import CompositeTtsManagerProviderInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..voicemail.helpers.voicemailHelperInterface import VoicemailHelperInterface
from ..voicemail.models.preparedVoicemailData import PreparedVoicemailData
from ..voicemail.settings.voicemailSettingsRepositoryInterface import VoicemailSettingsRepositoryInterface


class PlayVoicemailChatCommand(AbsChatCommand):

    def __init__(
        self,
        compositeTtsManagerProvider: CompositeTtsManagerProviderInterface,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        voicemailHelper: VoicemailHelperInterface,
        voicemailSettingsRepository: VoicemailSettingsRepositoryInterface,
    ):
        if not isinstance(compositeTtsManagerProvider, CompositeTtsManagerProviderInterface):
            raise TypeError(f'compositeTtsManagerProvider argument is malformed: \"{compositeTtsManagerProvider}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(voicemailHelper, VoicemailHelperInterface):
            raise TypeError(f'voicemailHelper argument is malformed: \"{voicemailHelper}\"')
        elif not isinstance(voicemailSettingsRepository, VoicemailSettingsRepositoryInterface):
            raise TypeError(f'voicemailSettingsRepository argument is malformed: \"{voicemailSettingsRepository}\"')

        self.__compositeTtsManagerProvider: Final[CompositeTtsManagerProviderInterface] = compositeTtsManagerProvider
        self.__streamAlertsManager: Final[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__voicemailHelper: Final[VoicemailHelperInterface] = voicemailHelper
        self.__voicemailSettingsRepository: Final[VoicemailSettingsRepositoryInterface] = voicemailSettingsRepository

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!playvoicemail\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'PlayVoicemailChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not await self.__voicemailSettingsRepository.isEnabled():
            return ChatCommandResult.IGNORED
        elif not chatMessage.twitchUser.isTtsEnabled:
            return ChatCommandResult.IGNORED

        voicemail = await self.__voicemailHelper.popForTargetUser(
            targetUserId = chatMessage.chatterUserId,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        if voicemail is None:
            return ChatCommandResult.IGNORED

        providerOverridableStatus: TtsProviderOverridableStatus

        if chatMessage.twitchUser.isChatterPreferredTtsEnabled:
            providerOverridableStatus = TtsProviderOverridableStatus.CHATTER_OVERRIDABLE
        else:
            providerOverridableStatus = TtsProviderOverridableStatus.TWITCH_CHANNEL_DISABLED

        ttsEvent = TtsEvent(
            message = f'Playing back voicemail from {voicemail.originatingUserName}... {voicemail.message}',
            twitchChannel = chatMessage.twitchChannel,
            twitchChannelId = chatMessage.twitchChannelId,
            userId = voicemail.originatingUserId,
            userName = voicemail.originatingUserName,
            donation = None,
            provider = chatMessage.twitchUser.defaultTtsProvider,
            providerOverridableStatus = providerOverridableStatus,
            raidInfo = None,
        )

        if await self.__voicemailSettingsRepository.useMessageQueueing():
            self.__streamAlertsManager.submitAlert(StreamAlert(
                soundAlert = None,
                twitchChannel = chatMessage.twitchChannel,
                twitchChannelId = chatMessage.twitchChannelId,
                ttsEvent = ttsEvent,
            ))
        else:
            compositeTtsManager = self.__compositeTtsManagerProvider.constructNewInstance(
                useSharedSoundPlayerManager = False,
            )

            await compositeTtsManager.playTtsEvent(ttsEvent)

        self.__twitchChatMessenger.send(
            text = await self.__toString(voicemail),
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Handled ({voicemail=}) ({chatMessage=})')
        return ChatCommandResult.CONSUMED

    async def __toString(self, voicemail: PreparedVoicemailData) -> str:
        now = self.__timeZoneRepository.getNow()
        timeDifferenceSeconds = int(round((now - voicemail.createdDateTime).total_seconds()))

        durationAgoMessage: str
        if timeDifferenceSeconds < 30:
            durationAgoMessage = 'moments'
        else:
            durationAgoMessage = utils.secondsToDurationMessage(timeDifferenceSeconds)

        return f'☎️ Playing back voicemail from @{voicemail.originatingUserName}, left {durationAgoMessage} ago…'
