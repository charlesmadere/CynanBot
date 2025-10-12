import locale
from typing import Final

from .absChatterItemEventHandler import AbsChatterItemEventHandler
from ..models.chatterItemType import ChatterItemType
from ..models.events.absChatterItemEvent import AbsChatterItemEvent
from ..models.events.animalPetChatterItemEvent import AnimalPetChatterItemEvent
from ..models.events.cassetteTapeMessageHasNoTargetChatterItemEvent import \
    CassetteTapeMessageHasNoTargetChatterItemEvent
from ..models.events.cassetteTapeTargetIsNotFollowingChatterItemEvent import \
    CassetteTapeTargetIsNotFollowingChatterItemEvent
from ..models.events.disabledFeatureChatterItemEvent import DisabledFeatureChatterItemEvent
from ..models.events.disabledItemTypeChatterItemEvent import DisabledItemTypeChatterItemEvent
from ..models.events.gashaponResultsChatterItemEvent import GashaponResultsChatterItemEvent
from ..models.events.noGashaponResultsChatterItemEvent import NoGashaponResultsChatterItemEvent
from ..models.events.notEnoughInventoryChatterItemEvent import NotEnoughInventoryChatterItemEvent
from ..models.events.tradeChatterItemEvent import TradeChatterItemEvent
from ..models.events.useAirStrikeChatterItemEvent import UseAirStrikeChatterItemEvent
from ..models.events.useBananaChatterItemEvent import UseBananaChatterItemEvent
from ..models.events.useCassetteTapeChatterItemEvent import UseCassetteTapeChatterItemEvent
from ..models.events.useGrenadeChatterItemEvent import UseGrenadeChatterItemEvent
from ..models.events.useTm36ChatterItemEvent import UseTm36ChatterItemEvent
from ..models.events.useVoreChatterItemEvent import UseVoreChatterItemEvent
from ..models.events.voicemailMessageIsEmptyChatterItemEvent import VoicemailMessageIsEmptyChatterItemEvent
from ..models.events.voicemailTargetIsOriginatingUserChatterItemEvent import \
    VoicemailTargetIsOriginatingUserChatterItemEvent
from ..models.events.voicemailTargetIsStreamerChatterItemEvent import VoicemailTargetIsStreamerChatterItemEvent
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...soundPlayerManager.provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ...soundPlayerManager.randomizerHelper.soundPlayerRandomizerHelperInterface import \
    SoundPlayerRandomizerHelperInterface
from ...soundPlayerManager.soundAlert import SoundAlert
from ...streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ...timber.timberInterface import TimberInterface
from ...twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ...twitch.configuration.twitchConnectionReadinessProvider import TwitchConnectionReadinessProvider


class ChatterItemEventHandler(AbsChatterItemEventHandler):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        soundPlayerManagerProvider: SoundPlayerManagerProviderInterface,
        soundPlayerRandomizerHelper: SoundPlayerRandomizerHelperInterface,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(soundPlayerManagerProvider, SoundPlayerManagerProviderInterface):
            raise TypeError(f'soundPlayerManagerProvider argument is malformed: \"{soundPlayerManagerProvider}\"')
        elif not isinstance(soundPlayerRandomizerHelper, SoundPlayerRandomizerHelperInterface):
            raise TypeError(f'soundPlayerRandomizerHelper argument is malformed: \"{soundPlayerRandomizerHelper}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__soundPlayerManagerProvider: Final[SoundPlayerManagerProviderInterface] = soundPlayerManagerProvider
        self.__soundPlayerRandomizerHelper: Final[SoundPlayerRandomizerHelperInterface] = soundPlayerRandomizerHelper
        self.__streamAlertsManager: Final[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

        self.__twitchConnectionReadinessProvider: TwitchConnectionReadinessProvider | None = None

    async def onNewChatterItemEvent(self, event: AbsChatterItemEvent):
        if not isinstance(event, AbsChatterItemEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        self.__timber.log('ChatterItemEventHandler', f'Received new chatter item event ({event=})')

        twitchConnectionReadinessProvider = self.__twitchConnectionReadinessProvider

        if twitchConnectionReadinessProvider is None:
            self.__timber.log('ChatterItemEventHandler', f'Received new chatter item event event, but it won\'t be handled, as the twitchChannelProvider and/or twitchConnectionReadinessProvider instances have not been set ({event=}) ({twitchConnectionReadinessProvider=})')
            return

        await twitchConnectionReadinessProvider.waitForReady()

        if isinstance(event, AnimalPetChatterItemEvent):
            await self.__handleAnimalPetChatterItemEvent(
                event = event,
            )

        elif isinstance(event, CassetteTapeMessageHasNoTargetChatterItemEvent):
            await self.__handleCassetteTapeMessageHasNoTargetChatterItemEvent(
                event = event,
            )

        elif isinstance(event, CassetteTapeTargetIsNotFollowingChatterItemEvent):
            await self.__handleCassetteTapeTargetIsNotFollowingChatterItemEvent(
                event = event,
            )

        elif isinstance(event, DisabledFeatureChatterItemEvent):
            await self.__handleDisabledFeatureChatterItemEvent(
                event = event,
            )

        elif isinstance(event, DisabledItemTypeChatterItemEvent):
            await self.__handleDisabledItemTypeChatterItemEvent(
                event = event,
            )

        elif isinstance(event, GashaponResultsChatterItemEvent):
            await self.__handleGashaponResultsChatterItemEvent(
                event = event,
            )

        elif isinstance(event, NoGashaponResultsChatterItemEvent):
            await self.__handleNoGashaponResultsChatterItemEvent(
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

        elif isinstance(event, UseTm36ChatterItemEvent):
            await self.__handleTm36ChatterItemEvent(
                event = event,
            )

        elif isinstance(event, UseVoreChatterItemEvent):
            await self.__handleVoreChatterItemEvent(
                event = event,
            )

        elif isinstance(event, VoicemailMessageIsEmptyChatterItemEvent):
            await self.__handleVoicemailMessageIsEmptyChatterItemEvent(
                event = event,
            )

        elif isinstance(event, VoicemailTargetIsOriginatingUserChatterItemEvent):
            await self.__handleVoicemailTargetIsOriginatingUserChatterItemEvent(
                event = event,
            )

        elif isinstance(event, VoicemailTargetIsStreamerChatterItemEvent):
            await self.__handleVoicemailTargetIsStreamerChatterItemEvent(
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

    async def __handleAnimalPetChatterItemEvent(
        self,
        event: AnimalPetChatterItemEvent,
    ):
        if event.user.areSoundAlertsEnabled:
            soundAlert = await self.__soundPlayerRandomizerHelper.chooseRandomFromDirectorySoundAlert(
                directoryPath = event.itemDetails.soundDirectory,
            )

            if utils.isValidStr(soundAlert):
                soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()
                self.__backgroundTaskHelper.createTask(soundPlayerManager.playSoundFile(soundAlert))

        animal = utils.getRandomAnimalEmoji()

        self.__twitchChatMessenger.send(
            text = f'You pet a {animal}! It seems to have enjoyed that!',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

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
        inventoryString = ''

        if event.updatedInventory is not None:
            amount = event.updatedInventory[ChatterItemType.CASSETTE_TAPE]
            amountString = locale.format_string("%d", amount, grouping = True)

            if amount == 1:
                inventoryString = f'({amountString} {ChatterItemType.CASSETTE_TAPE.humanName})'
            else:
                inventoryString = f'({amountString} {ChatterItemType.CASSETTE_TAPE.pluralHumanName})'

        self.__twitchChatMessenger.send(
            text = f'☎️ Your voicemail message for @{event.targetUserName} has been sent! {inventoryString}',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleCassetteTapeMessageHasNoTargetChatterItemEvent(
        self,
        event: CassetteTapeMessageHasNoTargetChatterItemEvent,
    ):
        self.__twitchChatMessenger.send(
            text = f'⚠ Sorry, the first word in the voicemail message must be a username (including the @ character is OK)',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleCassetteTapeTargetIsNotFollowingChatterItemEvent(
        self,
        event: CassetteTapeTargetIsNotFollowingChatterItemEvent,
    ):
        self.__twitchChatMessenger.send(
            text = f'⚠ Sorry, you can\'t send a voicemail to someone who isn\'t following the channel',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

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

    async def __handleGashaponResultsChatterItemEvent(
        self,
        event: GashaponResultsChatterItemEvent,
    ):
        if event.user.areSoundAlertsEnabled:
            soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()
            self.__backgroundTaskHelper.createTask(soundPlayerManager.playSoundAlert(SoundAlert.GASHAPON))

        awardedItemsStrings: list[str] = list()

        for itemType, amount in event.awardedItems.items():
            if amount == 0:
                continue

            amountString = locale.format_string("%d", amount, grouping = True)

            if amount == 1:
                awardedItemsStrings.append(f'{amountString} {itemType.humanName}')
            else:
                awardedItemsStrings.append(f'{amountString} {itemType.pluralHumanName}')

        awardedItemsString = ', '.join(awardedItemsStrings)

        self.__twitchChatMessenger.send(
            text = f'📮 ガチャ! {event.hypeEmote} You received {awardedItemsString}',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleGrenadeChatterItemEvent(
        self,
        event: UseGrenadeChatterItemEvent,
    ):
        # We don't handle this item use here. Instead, we handle this within the
        # TimeoutEventHandler class. It's a bit of a weird flow but... whatever :P
        pass

    async def __handleNoGashaponResultsChatterItemEvent(
        self,
        event: NoGashaponResultsChatterItemEvent,
    ):
        self.__twitchChatMessenger.send(
            text = f'📮 ガチャ! But… you got nothing… {event.ripBozoEmote}',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleNotEnoughInventoryChatterItemEvent(
        self,
        event: NotEnoughInventoryChatterItemEvent,
    ):
        self.__twitchChatMessenger.send(
            text = f'⚠ Sorry, you don\'t have any {event.getItemType().pluralHumanName}',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleTm36ChatterItemEvent(
        self,
        event: UseTm36ChatterItemEvent,
    ):
        # We don't handle this item use here. Instead, we handle this within the
        # TimeoutEventHandler class. It's a bit of a weird flow but... whatever :P
        pass

    async def __handleTradeChatterItemEvent(
        self,
        event: TradeChatterItemEvent,
    ):
        fromChatterQuantity = event.fromChatterInventory[event.getItemType()]
        fromChatterQuantityString = locale.format_string("%d", fromChatterQuantity, grouping = True)

        toChatterQuantity = event.toChatterInventory[event.getItemType()]
        toChatterQuantityString = locale.format_string("%d", toChatterQuantity, grouping = True)

        self.__twitchChatMessenger.send(
            text = f'ⓘ New {event.getItemType().humanName} counts — @{event.fromChatterInventory} {fromChatterQuantityString}, @{event.toChatterUserName} {toChatterQuantityString}',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleVoicemailMessageIsEmptyChatterItemEvent(
        self,
        event: VoicemailMessageIsEmptyChatterItemEvent,
    ):
        self.__twitchChatMessenger.send(
            text = f'⚠ Sorry, you can\'t send an empty voicemail',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleVoicemailTargetIsOriginatingUserChatterItemEvent(
        self,
        event: VoicemailTargetIsOriginatingUserChatterItemEvent,
    ):
        self.__twitchChatMessenger.send(
            text = f'⚠ Sorry, you can\'t send yourself a voicemail',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleVoicemailTargetIsStreamerChatterItemEvent(
        self,
        event: VoicemailTargetIsStreamerChatterItemEvent,
    ):
        self.__twitchChatMessenger.send(
            text = f'⚠ Sorry, you can\'t send the streamer a voicemail',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleVoreChatterItemEvent(
        self,
        event: UseVoreChatterItemEvent,
    ):
        # We don't handle this item use here. Instead, we handle this within the
        # TimeoutEventHandler class. It's a bit of a weird flow but... whatever :P
        pass

    def setTwitchConnectionReadinessProvider(self, provider: TwitchConnectionReadinessProvider | None):
        if provider is not None and not isinstance(provider, TwitchConnectionReadinessProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchConnectionReadinessProvider = provider
