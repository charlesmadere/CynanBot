from typing import Final

from .absUseChatterItemEventHandler import AbsUseChatterItemEventHandler
from ..models.events.disabledFeatureChatterItemEvent import DisabledFeatureChatterItemEvent
from ..models.events.disabledItemTypeChatterItemEvent import DisabledItemTypeChatterItemEvent
from ..models.events.notEnoughInventoryChatterItemEvent import NotEnoughInventoryChatterItemEvent
from ..models.events.useAirStrikeChatterItemEvent import UseAirStrikeChatterItemEvent
from ..models.events.useBananaChatterItemEvent import UseBananaChatterItemEvent
from ..models.events.useCassetteTapeChatterItemEvent import UseCassetteTapeChatterItemEvent
from ..models.events.useChatterItemEvent import UseChatterItemEvent
from ..models.events.useGrenadeChatterItemEvent import UseGrenadeChatterItemEvent
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...soundPlayerManager.provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ...streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ...timber.timberInterface import TimberInterface
from ...twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ...twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ...twitch.configuration.twitchConnectionReadinessProvider import TwitchConnectionReadinessProvider


class UseChatterItemEventHandler(AbsUseChatterItemEventHandler):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        soundPlayerManagerProvider: SoundPlayerManagerProviderInterface,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(soundPlayerManagerProvider, SoundPlayerManagerProviderInterface):
            raise TypeError(f'soundPlayerManagerProvider argument is malformed: \"{soundPlayerManagerProvider}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__soundPlayerManagerProvider: Final[SoundPlayerManagerProviderInterface] = soundPlayerManagerProvider
        self.__streamAlertsManager: Final[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

        self.__twitchChannelProvider: TwitchChannelProvider | None = None
        self.__twitchConnectionReadinessProvider: TwitchConnectionReadinessProvider | None = None

    async def onNewUseChatterItemEvent(self, event: UseChatterItemEvent):
        if not isinstance(event, UseChatterItemEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        self.__timber.log('UseChatterItemEventHandler', f'Received new chatter item event ({event=})')

        twitchChannelProvider = self.__twitchChannelProvider
        twitchConnectionReadinessProvider = self.__twitchConnectionReadinessProvider

        if twitchChannelProvider is None or twitchConnectionReadinessProvider is None:
            self.__timber.log('UseChatterItemEventHandler', f'Received new chatter item event event, but it won\'t be handled, as the twitchChannelProvider and/or twitchConnectionReadinessProvider instances have not been set ({event=}) ({twitchChannelProvider=}) ({twitchConnectionReadinessProvider=})')
            return

        await twitchConnectionReadinessProvider.waitForReady()

        if isinstance(event, DisabledFeatureChatterItemEvent):
            await self.__handleDisabledFeatureChatterItemEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider,
            )

        elif isinstance(event, DisabledItemTypeChatterItemEvent):
            await self.__handleDisabledItemTypeChatterItemEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider,
            )

        elif isinstance(event, NotEnoughInventoryChatterItemEvent):
            await self.__handleNotEnoughInventoryChatterItemEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider,
            )

        elif isinstance(event, UseAirStrikeChatterItemEvent):
            await self.__handleAirStrikeChatterItemEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider,
            )

        elif isinstance(event, UseBananaChatterItemEvent):
            await self.__handleBananaChatterItemEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider,
            )

        elif isinstance(event, UseCassetteTapeChatterItemEvent):
            await self.__handleCassetteTapeChatterItemEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider,
            )

        elif isinstance(event, UseGrenadeChatterItemEvent):
            await self.__handleGrenadeChatterItemEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider,
            )

        else:
            self.__timber.log('UseChatterItemEventHandler', f'Received unhandled chatter item event ({event=})')

    async def __handleAirStrikeChatterItemEvent(
        self,
        event: UseAirStrikeChatterItemEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        # We don't handle this item use here. Instead, we handle this within the
        # TimeoutEventHandler class. It's a bit of a weird flow but... whatever :P
        pass

    async def __handleBananaChatterItemEvent(
        self,
        event: UseBananaChatterItemEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        # We don't handle this item use here. Instead, we handle this within the
        # TimeoutEventHandler class. It's a bit of a weird flow but... whatever :P
        pass

    async def __handleCassetteTapeChatterItemEvent(
        self,
        event: UseCassetteTapeChatterItemEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        # TODO Will handle this in the future when the cassette tape item logic is implemented
        #  within the item machine class.
        pass

    async def __handleDisabledFeatureChatterItemEvent(
        self,
        event: DisabledFeatureChatterItemEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        # For now, let's just not output a chat message for this.
        # But maybe this should change in the future.
        pass

    async def __handleDisabledItemTypeChatterItemEvent(
        self,
        event: DisabledItemTypeChatterItemEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        # For now, let's just not output a chat message for this.
        # But maybe this should change in the future.
        pass

    async def __handleGrenadeChatterItemEvent(
        self,
        event: UseGrenadeChatterItemEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        # We don't handle this item use here. Instead, we handle this within the
        # TimeoutEventHandler class. It's a bit of a weird flow but... whatever :P
        pass

    async def __handleNotEnoughInventoryChatterItemEvent(
        self,
        event: NotEnoughInventoryChatterItemEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        await self.__twitchChatMessenger.send(
            text = f'⚠ Sorry, you don\'t have an {event.itemType.humanName}',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider

    def setTwitchConnectionReadinessProvider(self, provider: TwitchConnectionReadinessProvider | None):
        if provider is not None and not isinstance(provider, TwitchConnectionReadinessProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchConnectionReadinessProvider = provider
