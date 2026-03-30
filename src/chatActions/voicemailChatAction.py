import locale
from datetime import timedelta
from typing import Final

from .absChatAction2 import AbsChatAction2
from .chatActionResult import ChatActionResult
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..voicemail.helpers.voicemailHelperInterface import VoicemailHelperInterface
from ..voicemail.settings.voicemailSettingsRepositoryInterface import VoicemailSettingsRepositoryInterface


class VoicemailChatAction(AbsChatAction2):

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        voicemailHelper: VoicemailHelperInterface,
        voicemailSettingsRepository: VoicemailSettingsRepositoryInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(voicemailHelper, VoicemailHelperInterface):
            raise TypeError(f'voicemailHelper argument is malformed: \"{voicemailHelper}\"')
        elif not isinstance(voicemailSettingsRepository, VoicemailSettingsRepositoryInterface):
            raise TypeError(f'voicemailSettingsRepository argument is malformed: \"{voicemailSettingsRepository}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__voicemailHelper: Final[VoicemailHelperInterface] = voicemailHelper
        self.__voicemailSettingsRepository: Final[VoicemailSettingsRepositoryInterface] = voicemailSettingsRepository

    @property
    def actionName(self) -> str:
        return 'VoicemailChatAction'

    async def handleChatAction(
        self,
        mostRecentChat: MostRecentChat | None,
        chatMessage: TwitchChatMessage,
    ) -> ChatActionResult:
        if not chatMessage.twitchUser.isVoicemailEnabled or not chatMessage.twitchUser.isTtsEnabled:
            return ChatActionResult.IGNORED
        elif not await self.__voicemailSettingsRepository.isEnabled():
            return ChatActionResult.IGNORED

        now = self.__timeZoneRepository.getNow()

        hoursBetweenNotifications = timedelta(
            hours = await self.__voicemailSettingsRepository.getHoursBetweenAutomaticVoicemailChatNotifications()
        )

        if mostRecentChat is not None and (mostRecentChat.mostRecentChat + hoursBetweenNotifications) > now:
            return ChatActionResult.IGNORED

        voicemails = await self.__voicemailHelper.getAllForTargetUser(
            targetUserId = chatMessage.chatterUserId,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        if len(voicemails) == 0:
            return ChatActionResult.IGNORED

        voicemailsLenStr = locale.format_string("%d", len(voicemails), grouping = True)

        voicemailsPlurality: str
        if len(voicemails) == 1:
            voicemailsPlurality = 'voicemail'
        else:
            voicemailsPlurality = 'voicemails'

        self.__twitchChatMessenger.send(
            text = f'☎️ @{chatMessage.chatterUserName} you\'ve got mail! Use the !playvoicemail command to play the message. You currently have {voicemailsLenStr} {voicemailsPlurality}.',
            twitchChannelId = chatMessage.twitchChannelId,
            delaySeconds = 8,
        )

        self.__timber.log(self.actionName, f'Notified user of voicemail(s) ({voicemails=}) ({chatMessage=})')
        return ChatActionResult.HANDLED
