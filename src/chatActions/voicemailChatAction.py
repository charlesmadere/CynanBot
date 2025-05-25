import locale
from datetime import datetime, timedelta
from typing import Final

from .absChatAction import AbsChatAction
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ..twitch.configuration.twitchMessage import TwitchMessage
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.userInterface import UserInterface
from ..voicemail.helpers.voicemailHelperInterface import VoicemailHelperInterface
from ..voicemail.settings.voicemailSettingsRepositoryInterface import VoicemailSettingsRepositoryInterface


class VoicemailChatAction(AbsChatAction):

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchUtils: TwitchUtilsInterface,
        voicemailHelper: VoicemailHelperInterface,
        voicemailSettingsRepository: VoicemailSettingsRepositoryInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(voicemailHelper, VoicemailHelperInterface):
            raise TypeError(f'voicemailHelper argument is malformed: \"{voicemailHelper}\"')
        elif not isinstance(voicemailSettingsRepository, VoicemailSettingsRepositoryInterface):
            raise TypeError(f'voicemailSettingsRepository argument is malformed: \"{voicemailSettingsRepository}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchUtils: Final[TwitchUtilsInterface] = twitchUtils
        self.__voicemailHelper: Final[VoicemailHelperInterface] = voicemailHelper
        self.__voicemailSettingsRepository: Final[VoicemailSettingsRepositoryInterface] = voicemailSettingsRepository

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

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
            twitchChannelId = await message.getTwitchChannelId()
        )

        if len(voicemails) == 0:
            return False

        twitchChannelProvider = self.__twitchChannelProvider

        if twitchChannelProvider is None:
            self.__timber.log('VoicemailChatAction', f'The TwitchChannelProvider instance has not yet been set! ({twitchChannelProvider=})')
            return False

        twitchChannel = await twitchChannelProvider.getTwitchChannel(user.handle)
        voicemailsLenStr = locale.format_string("%d", len(voicemails), grouping = True)

        voicemailsPlurality: str
        if len(voicemails) == 1:
            voicemailsPlurality = 'voicemail'
        else:
            voicemailsPlurality = 'voicemails'

        await self.__twitchUtils.waitThenSend(
            messageable = twitchChannel,
            delaySeconds = 8,
            message = f'☎️ @{message.getAuthorName()} you\'ve got mail! Use the !playvoicemail command to play the message. You currently have {voicemailsLenStr} {voicemailsPlurality}.'
        )

        return True

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider
