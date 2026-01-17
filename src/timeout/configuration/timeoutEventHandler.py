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
from ..models.events.bananaTimeoutDiceRollQueuedEvent import BananaTimeoutDiceRollQueuedEvent
from ..models.events.bananaTimeoutEvent import BananaTimeoutEvent
from ..models.events.bananaTimeoutFailedTimeoutEvent import BananaTimeoutFailedTimeoutEvent
from ..models.events.basicTimeoutEvent import BasicTimeoutEvent
from ..models.events.basicTimeoutFailedTimeoutEvent import BasicTimeoutFailedTimeoutEvent
from ..models.events.basicTimeoutTargetUnavailableTimeoutEvent import BasicTimeoutTargetUnavailableTimeoutEvent
from ..models.events.copyAnivMessageTimeoutEvent import CopyAnivMessageTimeoutEvent
from ..models.events.copyAnivMessageTimeoutFailedTimeoutEvent import CopyAnivMessageTimeoutFailedTimeoutEvent
from ..models.events.grenadeTimeoutEvent import GrenadeTimeoutEvent
from ..models.events.grenadeTimeoutFailedTimeoutEvent import GrenadeTimeoutFailedTimeoutEvent
from ..models.events.incorrectLiveStatusTimeoutEvent import IncorrectLiveStatusTimeoutEvent
from ..models.events.noAirStrikeInventoryAvailableTimeoutEvent import NoAirStrikeInventoryAvailableTimeoutEvent
from ..models.events.noAirStrikeTargetsAvailableTimeoutEvent import NoAirStrikeTargetsAvailableTimeoutEvent
from ..models.events.noBananaInventoryAvailableTimeoutEvent import NoBananaInventoryAvailableTimeoutEvent
from ..models.events.noBananaTargetAvailableTimeoutEvent import NoBananaTargetAvailableTimeoutEvent
from ..models.events.noGrenadeInventoryAvailableTimeoutEvent import NoGrenadeInventoryAvailableTimeoutEvent
from ..models.events.noGrenadeTargetAvailableTimeoutEvent import NoGrenadeTargetAvailableTimeoutEvent
from ..models.events.noTm36InventoryAvailableTimeoutEvent import NoTm36InventoryAvailableTimeoutEvent
from ..models.events.noVoreInventoryAvailableTimeoutEvent import NoVoreInventoryAvailableTimeoutEvent
from ..models.events.noVoreTargetAvailableTimeoutEvent import NoVoreTargetAvailableTimeoutEvent
from ..models.events.tm36TimeoutEvent import Tm36TimeoutEvent
from ..models.events.tm36TimeoutFailedTimeoutEvent import Tm36TimeoutFailedTimeoutEvent
from ..models.events.voreTargetIsImmuneTimeoutEvent import VoreTargetIsImmuneTimeoutEvent
from ..models.events.voreTimeoutEvent import VoreTimeoutEvent
from ..models.events.voreTimeoutFailedTimeoutEvent import VoreTimeoutFailedTimeoutEvent
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
from ...twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ...twitch.configuration.twitchConnectionReadinessProvider import TwitchConnectionReadinessProvider


class TimeoutEventHandler(AbsTimeoutEventHandler):

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

        self.__twitchConnectionReadinessProvider: TwitchConnectionReadinessProvider | None = None

    async def onNewTimeoutEvent(self, event: AbsTimeoutEvent):
        if not isinstance(event, AbsTimeoutEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        twitchConnectionReadinessProvider = self.__twitchConnectionReadinessProvider

        if twitchConnectionReadinessProvider is None:
            self.__timber.log('TimeoutEventHandler', f'Received new timeout event, but it won\'t be handled, as the twitchConnectionReadinessProvider instance has not been set ({event=}) ({twitchConnectionReadinessProvider=})')
            return

        await twitchConnectionReadinessProvider.waitForReady()

        if isinstance(event, AirStrikeTimeoutEvent):
            await self.__handleAirStrikeTimeoutEvent(
                event = event,
            )

        elif isinstance(event, BananaTimeoutDiceRollFailedEvent):
            await self.__handleBananaTimeoutDiceRollFailedEvent(
                event = event,
            )

        elif isinstance(event, BananaTimeoutDiceRollQueuedEvent):
            await self.__handleBananaTimeoutDiceRollQueuedEvent(
                event = event,
            )

        elif isinstance(event, BananaTimeoutEvent):
            await self.__handleBananaTimeoutEvent(
                event = event,
            )

        elif isinstance(event, BananaTimeoutFailedTimeoutEvent):
            await self.__handleBananaTimeoutFailedTimeoutEvent(
                event = event,
            )

        elif isinstance(event, BasicTimeoutEvent):
            await self.__handleBasicTimeoutEvent(
                event = event,
            )

        elif isinstance(event, BasicTimeoutFailedTimeoutEvent):
            await self.__handleBasicTimeoutFailedTimeoutEvent(
                event = event,
            )

        elif isinstance(event, BasicTimeoutTargetUnavailableTimeoutEvent):
            await self.__handleBasicTimeoutTargetUnavailableTimeoutEvent(
                event = event,
            )

        elif isinstance(event, CopyAnivMessageTimeoutEvent):
            await self.__handleCopyAnivMessageTimeoutEvent(
                event = event,
            )

        elif isinstance(event, CopyAnivMessageTimeoutFailedTimeoutEvent):
            await self.__handleCopyAnivMessageFailedTimeoutEvent(
                event = event,
            )

        elif isinstance(event, GrenadeTimeoutEvent):
            await self.__handleGrenadeTimeoutEvent(
                event = event,
            )

        elif isinstance(event, GrenadeTimeoutFailedTimeoutEvent):
            await self.__handleGrenadeTimeoutFailedTimeoutEvent(
                event = event,
            )

        elif isinstance(event, IncorrectLiveStatusTimeoutEvent):
            await self.__handleIncorrectLiveStatusTimeoutEvent(
                event = event,
            )

        elif isinstance(event, NoAirStrikeInventoryAvailableTimeoutEvent):
            await self.__handleNoAirStrikeInventoryAvailableTimeoutEvent(
                event = event,
            )

        elif isinstance(event, NoAirStrikeTargetsAvailableTimeoutEvent):
            await self.__handleNoAirStrikeTargetsAvailableTimeoutEvent(
                event = event,
            )

        elif isinstance(event, NoBananaInventoryAvailableTimeoutEvent):
            await self.__handleNoBananaInventoryAvailableTimeoutEvent(
                event = event,
            )

        elif isinstance(event, NoBananaTargetAvailableTimeoutEvent):
            await self.__handleNoBananaTargetAvailableTimeoutEvent(
                event = event,
            )

        elif isinstance(event, NoGrenadeInventoryAvailableTimeoutEvent):
            await self.__handleNoGrenadeInventoryAvailableTimeoutEvent(
                event = event,
            )

        elif isinstance(event, NoGrenadeTargetAvailableTimeoutEvent):
            await self.__handleNoGrenadeTargetAvailableTimeoutEvent(
                event = event,
            )

        elif isinstance(event, NoTm36InventoryAvailableTimeoutEvent):
            await self.__handleNoTm36InventoryAvailableTimeoutEvent(
                event = event,
            )

        elif isinstance(event, NoVoreInventoryAvailableTimeoutEvent):
            await self.__handleNoVoreInventoryAvailableTimeoutEvent(
                event = event,
            )

        elif isinstance(event, NoVoreTargetAvailableTimeoutEvent):
            await self.__handleNoVoreTargetAvailableTimeoutEvent(
                event = event,
            )

        elif isinstance(event, Tm36TimeoutEvent):
            await self.__handleTm36TimeoutEvent(
                event = event,
            )

        elif isinstance(event, Tm36TimeoutFailedTimeoutEvent):
            await self.__handleTm36TimeoutFailedTimeoutEvent(
                event = event,
            )

        elif isinstance(event, VoreTargetIsImmuneTimeoutEvent):
            await self.__handleVoreTargetIsImmuneTimeoutEvent(
                event = event,
            )

        elif isinstance(event, VoreTimeoutEvent):
            await self.__handleVoreTimeoutEvent(
                event = event,
            )

        elif isinstance(event, VoreTimeoutFailedTimeoutEvent):
            await self.__handleVoreTimeoutFailedTimeoutEvent(
                event = event,
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
    ):
        if len(event.targets) < 1:
            # this should absolutely never happen... but let's check for it just to be safe
            return

        userNames: list[str] = list()

        for target in event.targets:
            userNames.append(f'@{target.userName}')

        userNames.sort(key = lambda userName: userName.casefold())
        userNamesString = ', '.join(userNames)

        peopleCountString = locale.format_string("%d", len(userNames), grouping = True)

        peoplePluralityString: str
        if len(event.targets) == 1:
            peoplePluralityString = f'{peopleCountString} chatter was hit'
        else:
            peoplePluralityString = f'{peopleCountString} chatters hit'

        message = f'{event.explodedEmote} {peoplePluralityString} by @{event.instigatorUserName} with a {event.timeoutDuration.secondsStr}s timeout! {userNamesString} {event.bombEmote}'

        self.__twitchChatMessenger.send(
            text = message,
            twitchChannelId = event.twitchChannelId,
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
            await asyncio.sleep(0.50)

        await baseSoundPlayerManager.playSoundAlert(SoundAlert.SPLAT)

    async def __handleBananaTimeoutDiceRollFailedEvent(
        self,
        event: BananaTimeoutDiceRollFailedEvent,
    ):
        self.__twitchChatMessenger.send(
            text = f'{event.ripBozoEmote} Sorry @{event.instigatorUserName}, your timeout of @{event.timeoutTarget.userName} failed {event.ripBozoEmote} (rolled a d{event.diceRoll.dieSize} and got a {event.diceRoll.roll}, but needed greater than {event.diceRollFailureData.failureRoll}) {event.ripBozoEmote}',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleBananaTimeoutDiceRollQueuedEvent(
        self,
        event: BananaTimeoutDiceRollQueuedEvent,
    ):
        self.__twitchChatMessenger.send(
            text = f'🎲 @{event.instigatorUserName} queued up a dice roll versus @{event.timeoutTarget.userName}! (queue size is now {event.requestQueueSizeStr})',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleBananaTimeoutEvent(
        self,
        event: BananaTimeoutEvent,
    ):
        chatMessage: str
        if event.diceRoll is not None and event.diceRollFailureData is not None:
            if event.isReverse:
                chatMessage = f'{event.ripBozoEmote} Oh no! @{event.instigatorUserName} dropped a banana but they tripped themselves up! {event.ripBozoEmote} (rolled a d{event.diceRoll.dieSize} but got a {event.diceRoll.roll})'
            else:
                chatMessage = f'{event.ripBozoEmote} @{event.instigatorUserName} dropped a banana that tripped up @{event.timeoutTarget.userName}! {event.ripBozoEmote} (rolled a d{event.diceRoll.dieSize} and got a {event.diceRoll.roll}, needed greater than {event.diceRollFailureData.reverseRoll})'
        elif event.isReverse:
            chatMessage = f'{event.ripBozoEmote} Oh no! @{event.instigatorUserName} dropped a banana but they tripped themselves up! {event.ripBozoEmote}'
        else:
            chatMessage = f'{event.ripBozoEmote} @{event.instigatorUserName} dropped a banana that tripped up @{event.timeoutTarget.userName}! {event.ripBozoEmote}'

        self.__twitchChatMessenger.send(
            text = chatMessage,
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

        soundAlert: SoundAlert | None = None
        if event.user.areSoundAlertsEnabled:
            soundAlert = self.__chooseRandomGrenadeSoundAlert()

        ttsEvent: TtsEvent | None = None
        if event.user.isTtsEnabled:
            ttsMessage: str

            if event.isReverse:
                ttsMessage = f'Oh no! {event.instigatorUserName} got hit with a reverse! What a dumb idiot! Rip bozo!'
            else:
                ttsMessage = f'{event.instigatorUserName} timed out {event.timeoutTarget.userName} for {event.timeoutDuration.message}! Rip bozo!'

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
    ):
        # this method is intentionally empty
        pass

    async def __handleBasicTimeoutEvent(
        self,
        event: BasicTimeoutEvent,
    ):
        if utils.isValidStr(event.chatMessage):
            self.__twitchChatMessenger.send(
                text = event.chatMessage,
                twitchChannelId = event.twitchChannelId,
                replyMessageId = event.twitchChatMessageId,
            )

    async def __handleBasicTimeoutFailedTimeoutEvent(
        self,
        event: BasicTimeoutFailedTimeoutEvent,
    ):
        # this method is intentionally empty
        pass

    async def __handleBasicTimeoutTargetUnavailableTimeoutEvent(
        self,
        event: BasicTimeoutTargetUnavailableTimeoutEvent,
    ):
        # this method is intentionally empty
        pass

    async def __handleCopyAnivMessageTimeoutEvent(
        self,
        event: CopyAnivMessageTimeoutEvent,
    ):
        if not event.user.isAnivMessageCopyTimeoutChatReportingEnabled:
            return

        statsString = f'{event.copyMessageTimeoutScore.dodgeScoreStr}D-{event.copyMessageTimeoutScore.timeoutScoreStr}T'

        dodgePercentString: str
        if event.copyMessageTimeoutScore.dodgeScore == 0:
            dodgePercentString = f'0% dodge rate'
        elif event.copyMessageTimeoutScore.timeoutScore == 0:
            dodgePercentString = f'100% dodge rate'
        else:
            totalDodgesAndTimeouts = event.copyMessageTimeoutScore.dodgeScore + event.copyMessageTimeoutScore.timeoutScore
            dodgePercent = round((float(event.copyMessageTimeoutScore.dodgeScore) / float(totalDodgesAndTimeouts)) * float(100), 2)
            dodgePercentString = f'{dodgePercent}% dodge rate'

        timeoutScoreString = f'({statsString}, {dodgePercentString})'

        self.__twitchChatMessenger.send(
            text = f'@{event.targetUserName} {event.ripBozoEmote} {event.timeoutDuration.message} {event.ripBozoEmote} {timeoutScoreString}',
            twitchChannelId = event.twitchChannelId,
        )

    async def __handleCopyAnivMessageFailedTimeoutEvent(
        self,
        event: CopyAnivMessageTimeoutFailedTimeoutEvent,
    ):
        # this event type is intentionally ignored
        pass

    async def __handleGrenadeTimeoutEvent(
        self,
        event: GrenadeTimeoutEvent,
    ):
        if event.user.areSoundAlertsEnabled:
            soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()
            self.__backgroundTaskHelper.createTask(soundPlayerManager.playSoundAlert(
                alert = self.__chooseRandomGrenadeSoundAlert(),
            ))

        remainingInventoryString = ''
        if event.updatedInventory is not None:
            remainingInventoryString = await self.__getInventoryRemainingString(
                itemType = ChatterItemType.GRENADE,
                inventory = event.updatedInventory.inventory,
            )

        self.__twitchChatMessenger.send(
            text = f'{event.explodedEmote} @{event.timeoutTarget.userName} {event.bombEmote} {remainingInventoryString}',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleGrenadeTimeoutFailedTimeoutEvent(
        self,
        event: GrenadeTimeoutFailedTimeoutEvent,
    ):
        # this event type is intentionally ignored
        pass

    async def __handleIncorrectLiveStatusTimeoutEvent(
        self,
        event: IncorrectLiveStatusTimeoutEvent,
    ):
        # this event type is intentionally ignored
        pass

    async def __handleNoAirStrikeInventoryAvailableTimeoutEvent(
        self,
        event: NoAirStrikeInventoryAvailableTimeoutEvent,
    ):
        self.__twitchChatMessenger.send(
            text = f'Sorry, you have no {ChatterItemType.AIR_STRIKE.pluralHumanName}!',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleNoAirStrikeTargetsAvailableTimeoutEvent(
        self,
        event: NoAirStrikeTargetsAvailableTimeoutEvent,
    ):
        self.__twitchChatMessenger.send(
            text = f'Sorry, there are no {ChatterItemType.AIR_STRIKE.humanName} targets available!',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleNoBananaInventoryAvailableTimeoutEvent(
        self,
        event: NoBananaInventoryAvailableTimeoutEvent,
    ):
        self.__twitchChatMessenger.send(
            text = f'Sorry, you have no {ChatterItemType.BANANA.pluralHumanName}!',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleNoBananaTargetAvailableTimeoutEvent(
        self,
        event: NoBananaTargetAvailableTimeoutEvent,
    ):
        self.__twitchChatMessenger.send(
            text = f'Sorry, your {ChatterItemType.BANANA.humanName} target is not available!',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleNoGrenadeInventoryAvailableTimeoutEvent(
        self,
        event: NoGrenadeInventoryAvailableTimeoutEvent,
    ):
        self.__twitchChatMessenger.send(
            text = f'Sorry, you have no {ChatterItemType.GRENADE.pluralHumanName}!',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleNoGrenadeTargetAvailableTimeoutEvent(
        self,
        event: NoGrenadeTargetAvailableTimeoutEvent,
    ):
        self.__twitchChatMessenger.send(
            text = f'Sorry, there are no {ChatterItemType.GRENADE.humanName} targets available',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleNoTm36InventoryAvailableTimeoutEvent(
        self,
        event: NoTm36InventoryAvailableTimeoutEvent,
    ):
        self.__twitchChatMessenger.send(
            text = f'Sorry @{event.thumbsDownEmote}, you don\'t have any {ChatterItemType.TM_36.pluralHumanName} available',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleNoVoreInventoryAvailableTimeoutEvent(
        self,
        event: NoVoreInventoryAvailableTimeoutEvent,
    ):
        self.__twitchChatMessenger.send(
            text = f'Sorry @{event.thumbsDownEmote}, you don\'t have any {ChatterItemType.VORE.pluralHumanName} available',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleNoVoreTargetAvailableTimeoutEvent(
        self,
        event: NoVoreTargetAvailableTimeoutEvent,
    ):
        self.__twitchChatMessenger.send(
            text = f'Sorry, your {ChatterItemType.VORE.humanName} target is not available!',
            twitchChannelId = event.twitchChannelId,
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

    async def __handleTm36TimeoutEvent(
        self,
        event: Tm36TimeoutEvent,
    ):
        if event.user.areSoundAlertsEnabled:
            soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()
            self.__backgroundTaskHelper.createTask(soundPlayerManager.playSoundAlert(SoundAlert.MEGA_GRENADE))

        remainingInventoryString = ''
        if event.updatedInventory is not None:
            remainingInventoryString = await self.__getInventoryRemainingString(
                itemType = ChatterItemType.TM_36,
                inventory = event.updatedInventory.inventory,
            )

        self.__twitchChatMessenger.send(
            text = f'{event.explodedEmote} @{event.targetUserName} used {ChatterItemType.TM_36.humanName}, its self destruct! {event.bombEmote} {remainingInventoryString}',
            twitchChannelId = event.twitchChannelId,
        )

        if event.splashTimeoutTarget is None:
            return

        self.__twitchChatMessenger.send(
            text = f'{event.explodedEmote} @{event.splashTimeoutTarget.userName} was also hit with splash damage! {event.bombEmote}',
            twitchChannelId = event.twitchChannelId,
        )

    async def __handleTm36TimeoutFailedTimeoutEvent(
        self,
        event: Tm36TimeoutFailedTimeoutEvent,
    ):
        # this event type is intentionally ignored
        pass

    async def __handleVoreTargetIsImmuneTimeoutEvent(
        self,
        event: VoreTargetIsImmuneTimeoutEvent,
    ):
        self.__twitchChatMessenger.send(
            text = f'Sorry, your {ChatterItemType.VORE.humanName} target is immune!',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleVoreTimeoutEvent(
        self,
        event: VoreTimeoutEvent,
    ):
        if event.user.areSoundAlertsEnabled:
            soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()
            self.__backgroundTaskHelper.createTask(soundPlayerManager.playSoundAlert(SoundAlert.VORE))

        remainingInventoryString = ''
        if event.updatedInventory is not None:
            remainingInventoryString = await self.__getInventoryRemainingString(
                itemType = ChatterItemType.VORE,
                inventory = event.updatedInventory.inventory,
            )

        self.__twitchChatMessenger.send(
            text = f'{event.ripBozoEmote} @{event.instigatorUserName} used {ChatterItemType.VORE.humanName} on @{event.timeoutTarget.userName}! {remainingInventoryString}',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleVoreTimeoutFailedTimeoutEvent(
        self,
        event: VoreTimeoutFailedTimeoutEvent,
    ):
        # this event type is intentionally ignored
        pass

    def setTwitchConnectionReadinessProvider(self, provider: TwitchConnectionReadinessProvider | None):
        if provider is not None and not isinstance(provider, TwitchConnectionReadinessProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchConnectionReadinessProvider = provider
