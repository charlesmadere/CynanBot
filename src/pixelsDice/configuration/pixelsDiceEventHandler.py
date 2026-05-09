from typing import Final

from ..listeners.pixelsDiceEventListener import PixelsDiceEventListener
from ..models.events.absPixelsDiceEvent import AbsPixelsDiceEvent
from ..models.events.pixelsDiceClientConnectedEvent import PixelsDiceClientConnectedEvent
from ..models.events.pixelsDiceClientDisconnectedEvent import PixelsDiceClientDisconnectedEvent
from ..models.events.pixelsDiceRollEvent import PixelsDiceRollEvent
from ..settings.pixelsDiceSettingsInterface import PixelsDiceSettingsInterface
from ...misc.administratorProviderInterface import AdministratorProviderInterface
from ...timber.timberInterface import TimberInterface
from ...twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface


class PixelsDiceEventHandler(PixelsDiceEventListener):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        pixelsDiceSettings: PixelsDiceSettingsInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(pixelsDiceSettings, PixelsDiceSettingsInterface):
            raise TypeError(f'pixelsDiceSettings argument is malformed: \"{pixelsDiceSettings}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__pixelsDiceSettings: Final[PixelsDiceSettingsInterface] = pixelsDiceSettings
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

    async def onNewPixelsDiceEvent(self, event: AbsPixelsDiceEvent):
        if not isinstance(event, AbsPixelsDiceEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        if isinstance(event, PixelsDiceClientConnectedEvent):
            await self.__handleConnectedEvent(
                event = event,
            )

        elif isinstance(event, PixelsDiceClientDisconnectedEvent):
            await self.__handleDisconnectedEvent(
                event = event,
            )

        elif isinstance(event, PixelsDiceRollEvent):
            await self.__handleRollEvent(
                event = event,
            )

        else:
            self.__timber.log('PixelsDiceEventHandler', f'Received unhandled pixels dice event ({event=})')

    async def __handleConnectedEvent(self, event: PixelsDiceClientConnectedEvent):
        self.__timber.log('PixelsDiceEventHandler', f'Pixels Dice connected ({event=})')
        # this method is intentionally rather thin, for now at least

    async def __handleDisconnectedEvent(self, event: PixelsDiceClientDisconnectedEvent):
        self.__timber.log('PixelsDiceEventHandler', f'Pixels Dice disconnected ({event=})')
        # this method is intentionally rather thin, for now at least

    async def __handleRollEvent(self, event: PixelsDiceRollEvent):
        self.__timber.log('PixelsDiceEventHandler', f'Pixels Dice rolled ({event=})')

        if not await self.__pixelsDiceSettings.reportToChat():
            return

        twitchChannelId = await self.__administratorProvider.getAdministratorUserId()

        self.__twitchChatMessenger.send(
            text = f'🎲 You rolled a {event.roll}!',
            twitchChannelId = twitchChannelId,
        )
