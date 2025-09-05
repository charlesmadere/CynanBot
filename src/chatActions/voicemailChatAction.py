import locale
from datetime import datetime, timedelta
from typing import Final

from .absChatAction import AbsChatAction
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchMessage import TwitchMessage
from ..users.userInterface import UserInterface
from ..voicemail.helpers.voicemailHelperInterface import VoicemailHelperInterface
from ..voicemail.settings.voicemailSettingsRepositoryInterface import VoicemailSettingsRepositoryInterface


class VoicemailChatAction(AbsChatAction):

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

    async def handleChat(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface
    ) -> bool:
        if not await self.__voicemailSettingsRepository.isEnabled():
            return False
        elif not user.isVoicemailEnabled or not user.isTtsEnabled:
            return False

        now = datetime.now(self.__timeZoneRepository.getDefault())

        hoursBetweenNotifications = timedelta(
            hours = await self.__voicemailSettingsRepository.getHoursBetweenAutomaticVoicemailChatNotifications()
        )

        if mostRecentChat is not None and (mostRecentChat.mostRecentChat + hoursBetweenNotifications) > now:
            return False

        voicemails = await self.__voicemailHelper.getAllForTargetUser(
            targetUserId = message.getAuthorId(),
            twitchChannelId = await message.getTwitchChannelId(),
        )

        if len(voicemails) == 0:
            return False

        voicemailsLenStr = locale.format_string("%d", len(voicemails), grouping = True)

        voicemailsPlurality: str
        if len(voicemails) == 1:
            voicemailsPlurality = 'voicemail'
        else:
            voicemailsPlurality = 'voicemails'

        self.__twitchChatMessenger.send(
            text = f'☎️ @{message.getAuthorName()} you\'ve got mail! Use the !playvoicemail command to play the message. You currently have {voicemailsLenStr} {voicemailsPlurality}.',
            twitchChannelId = await message.getTwitchChannelId(),
            delaySeconds = 8,
        )

        return True
