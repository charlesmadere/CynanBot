from typing import Final

from .absChannelPointRedemption import AbsChannelPointRedemption
from ..chatterPreferredName.helpers.chatterPreferredNameHelperInterface import ChatterPreferredNameHelperInterface
from ..chatterPreferredName.helpers.chatterPreferredNameStringCleaner import ChatterPreferredNameStringCleaner
from ..chatterPreferredName.settings.chatterPreferredNameSettingsInterface import ChatterPreferredNameSettingsInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchChannel import TwitchChannel
from ..twitch.configuration.twitchChannelPointsMessage import TwitchChannelPointsMessage


class ChatterPreferredNamePointRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        chatterPreferredNameHelper: ChatterPreferredNameHelperInterface,
        chatterPreferredNameSettings: ChatterPreferredNameSettingsInterface,
        chatterPreferredNameStringCleaner: ChatterPreferredNameStringCleaner,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(chatterPreferredNameHelper, ChatterPreferredNameHelperInterface):
            raise TypeError(f'chatterPreferredNameHelper argument is malformed: \"{chatterPreferredNameHelper}\"')
        elif not isinstance(chatterPreferredNameSettings, ChatterPreferredNameSettingsInterface):
            raise TypeError(f'chatterPreferredNameSettings argument is malformed: \"{chatterPreferredNameSettings}\"')
        elif not isinstance(chatterPreferredNameStringCleaner, ChatterPreferredNameStringCleaner):
            raise TypeError(f'chatterPreferredNameStringCleaner argument is malformed: \"{chatterPreferredNameStringCleaner}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__chatterPreferredTtsHelper: Final[ChatterPreferredNameHelperInterface] = chatterPreferredNameHelper
        self.__chatterPreferredTtsSettingsRepository: Final[ChatterPreferredNameSettingsInterface] = chatterPreferredNameSettings
        self.__chatterPreferredNameStringCleaner: Final[ChatterPreferredNameStringCleaner] = chatterPreferredNameStringCleaner
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage,
    ) -> bool:
        if not await self.__chatterPreferredTtsSettingsRepository.isEnabled():
            return False

        twitchUser = twitchChannelPointsMessage.twitchUser

        preferredName = await self.__chatterPreferredNameStringCleaner.clean(
            name = twitchChannelPointsMessage.redemptionMessage,
        )

        # TODO

        self.__timber.log('ChatterPreferredNamePointRedemption', f'Redeemed for {twitchChannelPointsMessage.userName}:{twitchChannelPointsMessage.userId} in {twitchUser.handle}')
        return True
