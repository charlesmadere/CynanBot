import asyncio
import locale
import random
from typing import Final

from frozenlist import FrozenList

from .absTimeoutEventHandler import AbsTimeoutEventHandler
from ..models.events.absTimeoutEvent import AbsTimeoutEvent
from ..models.events.airStrikeTimeoutEvent import AirStrikeTimeoutEvent
from ..models.events.bananaTimeoutDiceRollFailedEvent import BananaTimeoutDiceRollFailedEvent
from ..models.events.bananaTimeoutEvent import BananaTimeoutEvent
from ..models.events.bananaTimeoutFailedTimeoutEvent import BananaTimeoutFailedTimeoutEvent
from ..models.events.basicTimeoutEvent import BasicTimeoutEvent
from ..models.events.basicTimeoutFailedTimeoutEvent import BasicTimeoutFailedTimeoutEvent
from ..models.events.basicTimeoutTargetUnavailableTimeoutEvent import BasicTimeoutTargetUnavailableTimeoutEvent
from ..models.events.grenadeTimeoutEvent import GrenadeTimeoutEvent
from ..models.events.grenadeTimeoutFailedTimeoutEvent import GrenadeTimeoutFailedTimeoutEvent
from ..models.events.incorrectLiveStatusTimeoutEvent import IncorrectLiveStatusTimeoutEvent
from ..models.events.noAirStrikeInventoryAvailableTimeoutEvent import NoAirStrikeInventoryAvailableTimeoutEvent
from ..models.events.noAirStrikeTargetsAvailableTimeoutEvent import NoAirStrikeTargetsAvailableTimeoutEvent
from ..models.events.noBananaInventoryAvailableTimeoutEvent import NoBananaInventoryAvailableTimeoutEvent
from ..models.events.noBananaTargetAvailableTimeoutEvent import NoBananaTargetAvailableTimeoutEvent
from ..models.events.noGrenadeInventoryAvailableTimeoutEvent import NoGrenadeInventoryAvailableTimeoutEvent
from ..models.events.noGrenadeTargetAvailableTimeoutEvent import NoGrenadeTargetAvailableTimeoutEvent
from ...chatterInventory.models.chatterItemType import ChatterItemType
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...soundPlayerManager.provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ...soundPlayerManager.soundAlert import SoundAlert
from ...streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ...timber.timberInterface import TimberInterface
from ...twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ...twitch.configuration.twitchConnectionReadinessProvider import TwitchConnectionReadinessProvider
from ...twitch.twitchUtilsInterface import TwitchUtilsInterface


class TimeoutEventHandler(AbsTimeoutEventHandler):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        soundPlayerManagerProvider: SoundPlayerManagerProviderInterface,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(soundPlayerManagerProvider, SoundPlayerManagerProviderInterface):
            raise TypeError(f'soundPlayerManagerProvider argument is malformed: \"{soundPlayerManagerProvider}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__soundPlayerManagerProvider: Final[SoundPlayerManagerProviderInterface] = soundPlayerManagerProvider
        self.__streamAlertsManager: Final[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: Final[TimberInterface] = timber
        self.__twitchUtils: Final[TwitchUtilsInterface] = twitchUtils

        self.__twitchChannelProvider: TwitchChannelProvider | None = None
        self.__twitchConnectionReadinessProvider: TwitchConnectionReadinessProvider | None = None

    async def onNewTimeoutEvent(self, event: AbsTimeoutEvent):
        if not isinstance(event, AbsTimeoutEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        self.__timber.log('TimeoutEventHandler', f'Received new timeout event ({event=})')

        twitchChannelProvider = self.__twitchChannelProvider
        twitchConnectionReadinessProvider = self.__twitchConnectionReadinessProvider

        if twitchChannelProvider is None or twitchConnectionReadinessProvider is None:
            self.__timber.log('TimeoutEventHandler', f'Received new timeout event, but it won\'t be handled, as the twitchChannelProvider and/or twitchConnectionReadinessProvider instances have not been set ({event=}) ({twitchChannelProvider=}) ({twitchConnectionReadinessProvider=})')
            return

        await twitchConnectionReadinessProvider.waitForReady()

        if isinstance(event, AirStrikeTimeoutEvent):
            await self.__handleAirStrikeTimeoutEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider,
            )

        elif isinstance(event, BananaTimeoutDiceRollFailedEvent):
            await self.__handleBananaTimeoutDiceRollFailedEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider,
            )

        elif isinstance(event, BananaTimeoutEvent):
            await self.__handleBananaTimeoutEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider,
            )

        elif isinstance(event, BananaTimeoutFailedTimeoutEvent):
            await self.__handleBananaTimeoutFailedTimeoutEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider,
            )

        elif isinstance(event, BasicTimeoutEvent):
            await self.__handleBasicTimeoutEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider,
            )

        elif isinstance(event, BasicTimeoutFailedTimeoutEvent):
            await self.__handleBasicTimeoutFailedTimeoutEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider,
            )

        elif isinstance(event, BasicTimeoutTargetUnavailableTimeoutEvent):
            await self.__handleBasicTimeoutTargetUnavailableTimeoutEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider,
            )

        elif isinstance(event, GrenadeTimeoutEvent):
            await self.__handleGrenadeTimeoutEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider,
            )

        elif isinstance(event, GrenadeTimeoutFailedTimeoutEvent):
            await self.__handleGrenadeTimeoutFailedTimeoutEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider,
            )

        elif isinstance(event, IncorrectLiveStatusTimeoutEvent):
            await self.__handleIncorrectLiveStatusTimeoutEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider,
            )

        elif isinstance(event, NoAirStrikeInventoryAvailableTimeoutEvent):
            await self.__handleNoAirStrikeInventoryAvailableTimeoutEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider,
            )

        elif isinstance(event, NoAirStrikeTargetsAvailableTimeoutEvent):
            await self.__handleNoAirStrikeTargetsAvailableTimeoutEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider,
            )

        elif isinstance(event, NoBananaInventoryAvailableTimeoutEvent):
            await self.__handleNoBananaInventoryAvailableTimeoutEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider,
            )

        elif isinstance(event, NoBananaTargetAvailableTimeoutEvent):
            await self.__handleNoBananaTargetAvailableTimeoutEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider,
            )

        elif isinstance(event, NoGrenadeInventoryAvailableTimeoutEvent):
            await self.__handleNoGrenadeInventoryAvailableTimeoutEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider,
            )

        elif isinstance(event, NoGrenadeTargetAvailableTimeoutEvent):
            await self.__handleNoGrenadeTargetAvailableTimeoutEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider,
            )

        else:
            self.__timber.log('TimeoutEventHandler', f'Received unhandled timeout event ({event=})')

    async def __handleAirStrikeTimeoutEvent(
        self,
        event: AirStrikeTimeoutEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        userNames: list[str] = list()

        for target in event.targets:
            userNames.append(f'@{target.targetUserName}')

        userNames.sort(key = lambda userName: userName.casefold())
        userNamesString = ', '.join(userNames)

        peopleCountString = locale.format_string("%d", len(userNames), grouping = True)

        peoplePluralityString: str
        if len(event.targets) == 1:
            peoplePluralityString = f'{peopleCountString} chatter was hit'
        else:
            peoplePluralityString = f'{peopleCountString} chatters hit'

        message = f'{event.explodedEmote} {peoplePluralityString} by @{event.instigatorUserName} with a {event.timeoutDuration.secondsStr}s timeout! {userNamesString} {event.bombEmote}'

        if event.user.areSoundAlertsEnabled:
            self.__backgroundTaskHelper.createTask(self.__handleAirStrikeSoundAlerts(
                targets = len(event.targets),
            ))

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = message,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleAirStrikeSoundAlerts(self, targets: int):
        if targets < 1:
            return

        soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()
        self.__backgroundTaskHelper.createTask(soundPlayerManager.playSoundAlert(SoundAlert.LAUNCH_AIR_STRIKE))
        await asyncio.sleep(2.0)

        soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()
        self.__backgroundTaskHelper.createTask(soundPlayerManager.playSoundAlert(SoundAlert.AIR_STRIKE))
        await asyncio.sleep(0.5)

        for _ in range(targets):
            grenadeSoundAlert = self.__chooseRandomGrenadeSoundAlert()
            soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()
            self.__backgroundTaskHelper.createTask(soundPlayerManager.playSoundAlert(grenadeSoundAlert))
            await asyncio.sleep(0.75)

        soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()
        self.__backgroundTaskHelper.createTask(soundPlayerManager.playSoundAlert(SoundAlert.SPLAT))

    async def __handleBananaTimeoutDiceRollFailedEvent(
        self,
        event: BananaTimeoutDiceRollFailedEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        # TODO
        pass

    async def __handleBananaTimeoutEvent(
        self,
        event: BananaTimeoutEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        # TODO
        pass

    async def __handleBananaTimeoutFailedTimeoutEvent(
        self,
        event: BananaTimeoutFailedTimeoutEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        # TODO
        pass

    async def __handleBasicTimeoutEvent(
        self,
        event: BasicTimeoutEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        # TODO
        pass

    async def __handleBasicTimeoutFailedTimeoutEvent(
        self,
        event: BasicTimeoutFailedTimeoutEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        # TODO
        pass

    async def __handleBasicTimeoutTargetUnavailableTimeoutEvent(
        self,
        event: BasicTimeoutTargetUnavailableTimeoutEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        # TODO
        pass

    async def __handleGrenadeTimeoutEvent(
        self,
        event: GrenadeTimeoutEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()
        await soundPlayerManager.playSoundAlert(self.__chooseRandomGrenadeSoundAlert())

        remainingInventoryString = ''

        if event.updatedInventory is not None:
            remainingGrenades = locale.format_string("%d", event.updatedInventory[ChatterItemType.GRENADE], grouping = True)

            grenadesPlurality: str
            if event.updatedInventory[ChatterItemType.GRENADE] == 1:
                grenadesPlurality = 'grenade'
            else:
                grenadesPlurality = 'grenades'

            remainingInventoryString = f'({remainingGrenades} {grenadesPlurality} remaining)'

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = f'{event.explodedEmote} @{event.target.targetUserName} {event.bombEmote} {remainingInventoryString}',
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleGrenadeTimeoutFailedTimeoutEvent(
        self,
        event: GrenadeTimeoutFailedTimeoutEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        # TODO
        pass

    async def __handleIncorrectLiveStatusTimeoutEvent(
        self,
        event: IncorrectLiveStatusTimeoutEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        # TODO
        pass

    async def __handleNoAirStrikeInventoryAvailableTimeoutEvent(
        self,
        event: NoAirStrikeInventoryAvailableTimeoutEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        # TODO
        pass

    async def __handleNoAirStrikeTargetsAvailableTimeoutEvent(
        self,
        event: NoAirStrikeTargetsAvailableTimeoutEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        # TODO
        pass

    async def __handleNoBananaInventoryAvailableTimeoutEvent(
        self,
        event: NoBananaInventoryAvailableTimeoutEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        # TODO
        pass

    async def __handleNoBananaTargetAvailableTimeoutEvent(
        self,
        event: NoBananaTargetAvailableTimeoutEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        # TODO
        pass

    async def __handleNoGrenadeInventoryAvailableTimeoutEvent(
        self,
        event: NoGrenadeInventoryAvailableTimeoutEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        # TODO
        pass

    async def __handleNoGrenadeTargetAvailableTimeoutEvent(
        self,
        event: NoGrenadeTargetAvailableTimeoutEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = f'Sorry @{event.thumbsDownEmote}, you don\'t have any grenades available',
            replyMessageId = event.twitchChatMessageId,
        )

    def __chooseRandomGrenadeSoundAlert(self) -> SoundAlert:
        grenadeSoundAlerts: FrozenList[SoundAlert] = FrozenList([
            SoundAlert.GRENADE_1,
            SoundAlert.GRENADE_2,
            SoundAlert.GRENADE_3,
        ])

        grenadeSoundAlerts.freeze()
        return random.choice(grenadeSoundAlerts)

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider

    def setTwitchConnectionReadinessProvider(self, provider: TwitchConnectionReadinessProvider | None):
        if provider is not None and not isinstance(provider, TwitchConnectionReadinessProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchConnectionReadinessProvider = provider
