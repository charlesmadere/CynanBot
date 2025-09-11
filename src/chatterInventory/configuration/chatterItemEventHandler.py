from typing import Final

from .absChatterItemEventHandler import AbsChatterItemEventHandler
from ..models.events.absChatterItemEvent import AbsChatterItemEvent
from ..models.events.disabledFeatureChatterItemEvent import DisabledFeatureChatterItemEvent
from ..models.events.disabledItemTypeChatterItemEvent import DisabledItemTypeChatterItemEvent
from ..models.events.notEnoughInventoryChatterItemEvent import NotEnoughInventoryChatterItemEvent
from ..models.events.tradeChatterItemEvent import TradeChatterItemEvent
from ..models.events.useAirStrikeChatterItemEvent import UseAirStrikeChatterItemEvent
from ..models.events.useBananaChatterItemEvent import UseBananaChatterItemEvent
from ..models.events.useCassetteTapeChatterItemEvent import UseCassetteTapeChatterItemEvent
from ..models.events.useGrenadeChatterItemEvent import UseGrenadeChatterItemEvent
from ...soundPlayerManager.provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ...streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ...timber.timberInterface import TimberInterface
from ...twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ...twitch.configuration.twitchConnectionReadinessProvider import TwitchConnectionReadinessProvider


class ChatterItemEventHandler(AbsChatterItemEventHandler):

    def __init__(
        self,
        soundPlayerManagerProvider: SoundPlayerManagerProviderInterface,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(soundPlayerManagerProvider, SoundPlayerManagerProviderInterface):
            raise TypeError(f'soundPlayerManagerProvider argument is malformed: \"{soundPlayerManagerProvider}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__soundPlayerManagerProvider: Final[SoundPlayerManagerProviderInterface] = soundPlayerManagerProvider
        self.__streamAlertsManager: Final[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

        self.__twitchConnectionReadinessProvider: TwitchConnectionReadinessProvider | None = None

    async def onNewChatterItemEvent(self, event: AbsChatterItemEvent):
        if not isinstance(event, AbsChatterItemEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        self.__timber.log('AbsChatterItemEventHandler', f'Received new chatter item event ({event=})')

        twitchConnectionReadinessProvider = self.__twitchConnectionReadinessProvider

        if twitchConnectionReadinessProvider is None:
            self.__timber.log('AbsChatterItemEventHandler', f'Received new chatter item event event, but it won\'t be handled, as the twitchChannelProvider and/or twitchConnectionReadinessProvider instances have not been set ({event=}) ({twitchConnectionReadinessProvider=})')
            return

        await twitchConnectionReadinessProvider.waitForReady()

        if isinstance(event, DisabledFeatureChatterItemEvent):
            await self.__handleDisabledFeatureChatterItemEvent(
                event = event,
            )

        elif isinstance(event, DisabledItemTypeChatterItemEvent):
            await self.__handleDisabledItemTypeChatterItemEvent(
                event = event,
            )

        elif isinstance(event, NotEnoughInventoryChatterItemEvent):
            await self.__handleNotEnoughInventoryChatterItemEvent(
                event = event,
            )

        elif isinstance(event, TradeChatterItemEvent):
            await self.__handleTradeChatterItemEvent(
                event = event,
            )

        elif isinstance(event, UseAirStrikeChatterItemEvent):
            await self.__handleAirStrikeChatterItemEvent(
                event = event,
            )

        elif isinstance(event, UseBananaChatterItemEvent):
            await self.__handleBananaChatterItemEvent(
                event = event,
            )

        elif isinstance(event, UseCassetteTapeChatterItemEvent):
            await self.__handleCassetteTapeChatterItemEvent(
                event = event,
            )

        elif isinstance(event, UseGrenadeChatterItemEvent):
            await self.__handleGrenadeChatterItemEvent(
                event = event,
            )

        else:
            self.__timber.log('ChatterItemEventHandler', f'Received unhandled chatter item event ({event=})')

    async def __handleAirStrikeChatterItemEvent(
        self,
        event: UseAirStrikeChatterItemEvent,
    ):
        # We don't handle this item use here. Instead, we handle this within the
        # TimeoutEventHandler class. It's a bit of a weird flow but... whatever :P
        pass

    async def __handleBananaChatterItemEvent(
        self,
        event: UseBananaChatterItemEvent,
    ):
        # We don't handle this item use here. Instead, we handle this within the
        # TimeoutEventHandler class. It's a bit of a weird flow but... whatever :P
        pass

    async def __handleCassetteTapeChatterItemEvent(
        self,
        event: UseCassetteTapeChatterItemEvent,
    ):
        # TODO Will handle this in the future when the cassette tape item logic is implemented
        #  within the item machine class.
        pass

    async def __handleDisabledFeatureChatterItemEvent(
        self,
        event: DisabledFeatureChatterItemEvent,
    ):
        # For now, let's just not output a chat message for this.
        # But maybe this should change in the future.
        pass

    async def __handleDisabledItemTypeChatterItemEvent(
        self,
        event: DisabledItemTypeChatterItemEvent,
    ):
        # For now, let's just not output a chat message for this.
        # But maybe this should change in the future.
        pass

    async def __handleGrenadeChatterItemEvent(
        self,
        event: UseGrenadeChatterItemEvent,
    ):
        # We don't handle this item use here. Instead, we handle this within the
        # TimeoutEventHandler class. It's a bit of a weird flow but... whatever :P
        pass

    async def __handleNotEnoughInventoryChatterItemEvent(
        self,
        event: NotEnoughInventoryChatterItemEvent,
    ):
        self.__twitchChatMessenger.send(
            text = f'⚠ Sorry, you don\'t have any {event.getItemType().pluralHumanName}',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleTradeChatterItemEvent(
        self,
        event: TradeChatterItemEvent,
    ):
        # TODO
        pass

    def setTwitchConnectionReadinessProvider(self, provider: TwitchConnectionReadinessProvider | None):
        if provider is not None and not isinstance(provider, TwitchConnectionReadinessProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchConnectionReadinessProvider = provider
