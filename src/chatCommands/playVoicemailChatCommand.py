from datetime import datetime
from typing import Final

from .absChatCommand import AbsChatCommand
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..streamAlertsManager.streamAlert import StreamAlert
from ..streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ..timber.timberInterface import TimberInterface
from ..tts.models.ttsEvent import TtsEvent
from ..tts.models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ..tts.provider.compositeTtsManagerProviderInterface import CompositeTtsManagerProviderInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..users.usersRepositoryInterface import UsersRepositoryInterface
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
        usersRepository: UsersRepositoryInterface,
        voicemailHelper: VoicemailHelperInterface,
        voicemailSettingsRepository: VoicemailSettingsRepositoryInterface
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
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(voicemailHelper, VoicemailHelperInterface):
            raise TypeError(f'voicemailHelper argument is malformed: \"{voicemailHelper}\"')
        elif not isinstance(voicemailSettingsRepository, VoicemailSettingsRepositoryInterface):
            raise TypeError(f'voicemailSettingsRepository argument is malformed: \"{voicemailSettingsRepository}\"')

        self.__compositeTtsManagerProvider: Final[CompositeTtsManagerProviderInterface] = compositeTtsManagerProvider
        self.__streamAlertsManager: Final[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository
        self.__voicemailHelper: Final[VoicemailHelperInterface] = voicemailHelper
        self.__voicemailSettingsRepository: Final[VoicemailSettingsRepositoryInterface] = voicemailSettingsRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        if not await self.__voicemailSettingsRepository.isEnabled():
            return

        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        if not user.isVoicemailEnabled or not user.isTtsEnabled:
            return

        voicemail = await self.__voicemailHelper.popForTargetUser(
            targetUserId = ctx.getAuthorId(),
            twitchChannelId = await ctx.getTwitchChannelId()
        )

        if voicemail is None:
            return

        providerOverridableStatus: TtsProviderOverridableStatus

        if user.isChatterPreferredTtsEnabled:
            providerOverridableStatus = TtsProviderOverridableStatus.CHATTER_OVERRIDABLE
        else:
            providerOverridableStatus = TtsProviderOverridableStatus.TWITCH_CHANNEL_DISABLED

        ttsEvent = TtsEvent(
            message = f'Playing back voicemail from {voicemail.originatingUserName}... {voicemail.message}',
            twitchChannel = user.handle,
            twitchChannelId = await ctx.getTwitchChannelId(),
            userId = voicemail.originatingUserId,
            userName = voicemail.originatingUserName,
            donation = None,
            provider = user.defaultTtsProvider,
            providerOverridableStatus = providerOverridableStatus,
            raidInfo = None
        )

        if await self.__voicemailSettingsRepository.useMessageQueueing():
            self.__streamAlertsManager.submitAlert(StreamAlert(
                soundAlert = None,
                twitchChannel = user.handle,
                twitchChannelId = await ctx.getTwitchChannelId(),
                ttsEvent = ttsEvent
            ))
        else:
            compositeTtsManager = self.__compositeTtsManagerProvider.constructNewInstance(
                useSharedSoundPlayerManager = False
            )

            await compositeTtsManager.playTtsEvent(ttsEvent)

        self.__twitchChatMessenger.send(
            text = await self.__toString(voicemail),
            twitchChannelId = await ctx.getTwitchChannelId(),
            replyMessageId = await ctx.getMessageId(),
        )

        self.__timber.log('PlayVoicemailChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')

    async def __toString(self, voicemail: PreparedVoicemailData) -> str:
        now = datetime.now(self.__timeZoneRepository.getDefault())
        timeDifferenceSeconds = round((now - voicemail.createdDateTime).total_seconds())

        durationAgoMessage: str
        if timeDifferenceSeconds < 30:
            durationAgoMessage = 'moments'
        else:
            durationAgoMessage = utils.secondsToDurationMessage(timeDifferenceSeconds)

        return f'☎️ Playing back voicemail from @{voicemail.originatingUserName} left {durationAgoMessage} ago…'
