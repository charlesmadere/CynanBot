import asyncio
import locale
import random
from typing import Final

from frozendict import frozendict
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
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...soundPlayerManager.provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ...soundPlayerManager.soundAlert import SoundAlert
from ...streamAlertsManager.streamAlert import StreamAlert
from ...streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ...timber.timberInterface import TimberInterface
from ...tts.models.ttsEvent import TtsEvent
from ...tts.models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
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

    async def __getInventoryRemainingString(
        self,
        itemType: ChatterItemType,
        inventory: frozendict[ChatterItemType, int],
    ) -> str:
        remainingCount = locale.format_string("%d", inventory[itemType], grouping = True)

        itemPlurality: str
        if inventory[itemType] == 1:
            itemPlurality = itemType.humanName
        else:
            itemPlurality = itemType.pluralHumanName

        return f'({remainingCount} {itemPlurality.lower()} remaining)'

    async def __handleAirStrikeTimeoutEvent(
        self,
        event: AirStrikeTimeoutEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        if len(event.targets) < 1:
            # this should absolutely never happen... but let's check for it just to be safe
            return

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

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = message,
            replyMessageId = event.twitchChatMessageId,
        )

        if not event.user.areSoundAlertsEnabled:
            return

        self.__backgroundTaskHelper.createTask(self.__handleAirStrikeSoundAlerts(
            targets = len(event.targets),
        ))

    async def __handleAirStrikeSoundAlerts(self, targets: int):
        if targets < 1:
            # this should absolutely never happen... but let's check for it just to be safe
            return

        baseSoundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()
        await baseSoundPlayerManager.playSoundAlert(SoundAlert.LAUNCH_AIR_STRIKE)
        await baseSoundPlayerManager.playSoundAlert(SoundAlert.AIR_STRIKE)

        for _ in range(targets):
            grenadeSoundAlert = self.__chooseRandomGrenadeSoundAlert()
            temporarySoundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()
            self.__backgroundTaskHelper.createTask(temporarySoundPlayerManager.playSoundAlert(grenadeSoundAlert))
            await asyncio.sleep(0.75)

        await baseSoundPlayerManager.playSoundAlert(SoundAlert.SPLAT)

    async def __handleBananaTimeoutDiceRollFailedEvent(
        self,
        event: BananaTimeoutDiceRollFailedEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = f'{event.ripBozoEmote} Sorry @{event.instigatorUserName}, your timeout of @{event.target.targetUserName} failed {event.ripBozoEmote} (rolled a d{event.diceRoll.dieSize} and got a {event.diceRoll.roll}, but needed greater than {event.diceRollFailureData.failureRoll}) {event.ripBozoEmote}',
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleBananaTimeoutEvent(
        self,
        event: BananaTimeoutEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        message: str
        if event.diceRoll is not None and event.diceRollFailureData is not None:
            if event.isReverse:
                message = f'{event.ripBozoEmote} Oh no! @{event.instigatorUserName} dropped a banana but they tripped themselves up! {event.ripBozoEmote} (rolled a d{event.diceRoll.dieSize} but got a {event.diceRoll.roll})'
            else:
                message = f'{event.ripBozoEmote} @{event.instigatorUserName} dropped a banana that tripped up @{event.target.targetUserName}! {event.ripBozoEmote} (rolled a d{event.diceRoll.dieSize} and got a {event.diceRoll.roll}, needed greater than {event.diceRollFailureData.reverseRoll})'
        elif event.isReverse:
            message = f'{event.ripBozoEmote} Oh no! @{event.instigatorUserName} dropped a banana but they tripped themselves up! {event.ripBozoEmote}'
        else:
            message = f'{event.ripBozoEmote} @{event.instigatorUserName} dropped a banana that tripped up @{event.target.targetUserName}! {event.ripBozoEmote}'

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = message,
            replyMessageId = event.twitchChatMessageId,
        )

        soundAlert: SoundAlert | None = None
        if event.user.areSoundAlertsEnabled:
            soundAlert = self.__chooseRandomGrenadeSoundAlert()

        ttsEvent: TtsEvent | None = None
        if event.user.isTtsEnabled:
            ttsMessage: str

            if event.isReverse:
                ttsMessage = f'Oh no! {event.instigatorUserName} got hit with a reverse! Rip bozo!'
            else:
                ttsMessage = f'{event.instigatorUserName} timed out {event.target.targetUserName} for {event.timeoutDuration.message}! Rip bozo!'

            providerOverridableStatus: TtsProviderOverridableStatus

            if event.user.isChatterPreferredTtsEnabled:
                providerOverridableStatus = TtsProviderOverridableStatus.CHATTER_OVERRIDABLE
            else:
                providerOverridableStatus = TtsProviderOverridableStatus.TWITCH_CHANNEL_DISABLED

            ttsEvent = TtsEvent(
                message = ttsMessage,
                twitchChannel = event.twitchChannel,
                twitchChannelId = event.twitchChannelId,
                userId = event.originatingAction.instigatorUserId,
                userName = event.instigatorUserName,
                donation = None,
                provider = event.user.defaultTtsProvider,
                providerOverridableStatus = providerOverridableStatus,
                raidInfo = None,
            )

        if soundAlert is None and ttsEvent is None:
            return

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = soundAlert,
            twitchChannel = event.twitchChannel,
            twitchChannelId = event.twitchChannelId,
            ttsEvent = ttsEvent,
        ))

    async def __handleBananaTimeoutFailedTimeoutEvent(
        self,
        event: BananaTimeoutFailedTimeoutEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        # this method is intentionally empty
        pass

    async def __handleBasicTimeoutEvent(
        self,
        event: BasicTimeoutEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        if utils.isValidStr(event.chatMessage):
            await self.__twitchUtils.safeSend(
                messageable = twitchChannel,
                message = event.chatMessage,
                replyMessageId = event.twitchChatMessageId,
            )

    async def __handleBasicTimeoutFailedTimeoutEvent(
        self,
        event: BasicTimeoutFailedTimeoutEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        # this method is intentionally empty
        pass

    async def __handleBasicTimeoutTargetUnavailableTimeoutEvent(
        self,
        event: BasicTimeoutTargetUnavailableTimeoutEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        # this method is intentionally empty
        pass

    async def __handleGrenadeTimeoutEvent(
        self,
        event: GrenadeTimeoutEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        if event.user.areSoundAlertsEnabled:
            soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()
            await soundPlayerManager.playSoundAlert(self.__chooseRandomGrenadeSoundAlert())

        remainingInventoryString = ''
        if event.updatedInventory is not None:
            remainingInventoryString = await self.__getInventoryRemainingString(
                itemType = ChatterItemType.GRENADE,
                inventory = event.updatedInventory.inventory,
            )

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
        # this method is intentionally empty
        pass

    async def __handleIncorrectLiveStatusTimeoutEvent(
        self,
        event: IncorrectLiveStatusTimeoutEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        # this method is intentionally empty
        pass

    async def __handleNoAirStrikeInventoryAvailableTimeoutEvent(
        self,
        event: NoAirStrikeInventoryAvailableTimeoutEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = f'Sorry, you have no air strikes!',
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleNoAirStrikeTargetsAvailableTimeoutEvent(
        self,
        event: NoAirStrikeTargetsAvailableTimeoutEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = f'Sorry, there are no air strike targets available!',
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleNoBananaInventoryAvailableTimeoutEvent(
        self,
        event: NoBananaInventoryAvailableTimeoutEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = f'Sorry, you have no bananas!',
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleNoBananaTargetAvailableTimeoutEvent(
        self,
        event: NoBananaTargetAvailableTimeoutEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = f'Sorry, your banana target is not available!',
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleNoGrenadeInventoryAvailableTimeoutEvent(
        self,
        event: NoGrenadeInventoryAvailableTimeoutEvent,
        twitchChannelProvider: TwitchChannelProvider,
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        await self.__twitchUtils.safeSend(
            messageable = twitchChannel,
            message = f'Sorry, you have no grenades!',
            replyMessageId = event.twitchChatMessageId,
        )

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
        soundAlerts: FrozenList[SoundAlert] = FrozenList([
            SoundAlert.GRENADE_1,
            SoundAlert.GRENADE_2,
            SoundAlert.GRENADE_3,
        ])
        soundAlerts.freeze()
        return random.choice(soundAlerts)

    def __chooseRandomMegaGrenadeSoundAlert(self) -> SoundAlert:
        soundAlerts: FrozenList[SoundAlert] = FrozenList([
            SoundAlert.MEGA_GRENADE_1,
            SoundAlert.MEGA_GRENADE_2,
            SoundAlert.MEGA_GRENADE_3,
        ])
        soundAlerts.freeze()
        return random.choice(soundAlerts)

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider

    def setTwitchConnectionReadinessProvider(self, provider: TwitchConnectionReadinessProvider | None):
        if provider is not None and not isinstance(provider, TwitchConnectionReadinessProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchConnectionReadinessProvider = provider
