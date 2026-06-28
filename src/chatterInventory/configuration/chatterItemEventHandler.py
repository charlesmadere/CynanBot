import locale
import math
from typing import Final

from ..listeners.chatterItemEventListener import ChatterItemEventListener
from ..models.chatterItemType import ChatterItemType
from ..models.events.absChatterItemEvent import AbsChatterItemEvent
from ..models.events.animalPetChatterItemEvent import AnimalPetChatterItemEvent
from ..models.events.cassetteTapeMessageHasNoTargetChatterItemEvent import \
    CassetteTapeMessageHasNoTargetChatterItemEvent
from ..models.events.cassetteTapeTargetIsNotFollowingChatterItemEvent import \
    CassetteTapeTargetIsNotFollowingChatterItemEvent
from ..models.events.disabledFeatureChatterItemEvent import DisabledFeatureChatterItemEvent
from ..models.events.disabledItemTypeChatterItemEvent import DisabledItemTypeChatterItemEvent
from ..models.events.gashaponNotRewardedItemDisabledChatterItemEvent import \
    GashaponNotRewardedItemDisabledChatterItemEvent
from ..models.events.gashaponNotRewardedNotFollowingChatterItemEvent import \
    GashaponNotRewardedNotFollowingChatterItemEvent
from ..models.events.gashaponNotRewardedNotReadyChatterItemEvent import GashaponNotRewardedNotReadyChatterItemEvent
from ..models.events.gashaponNotRewardedNotSubscribedChatterItemEvent import \
    GashaponNotRewardedNotSubscribedChatterItemEvent
from ..models.events.gashaponResultsChatterItemEvent import GashaponResultsChatterItemEvent
from ..models.events.gashaponRewardedChatterItemEvent import GashaponRewardedChatterItemEvent
from ..models.events.giveChatterItemEvent import GiveChatterItemEvent
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
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...soundPlayerManager.provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ...soundPlayerManager.randomizerHelper.soundPlayerRandomizerHelperInterface import \
    SoundPlayerRandomizerHelperInterface
from ...soundPlayerManager.soundAlert import SoundAlert
from ...streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ...timber.timberInterface import TimberInterface
from ...twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface


class ChatterItemEventHandler(ChatterItemEventListener):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        soundPlayerManagerProvider: SoundPlayerManagerProviderInterface,
        soundPlayerRandomizerHelper: SoundPlayerRandomizerHelperInterface,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
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
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__soundPlayerManagerProvider: Final[SoundPlayerManagerProviderInterface] = soundPlayerManagerProvider
        self.__soundPlayerRandomizerHelper: Final[SoundPlayerRandomizerHelperInterface] = soundPlayerRandomizerHelper
        self.__streamAlertsManager: Final[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

    async def onNewChatterItemEvent(self, event: AbsChatterItemEvent):
        if not isinstance(event, AbsChatterItemEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

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

        elif isinstance(event, GashaponNotRewardedItemDisabledChatterItemEvent):
            await self.__handleGashaponNotRewardedItemDisabledChatterItemEvent(
                event = event,
            )

        elif isinstance(event, GashaponNotRewardedNotFollowingChatterItemEvent):
            await self.__handleGashaponNotRewardedNotFollowingChatterItemEvent(
                event = event,
            )

        elif isinstance(event, GashaponNotRewardedNotReadyChatterItemEvent):
            await self.__handleGashaponNotRewardedNotReadyChatterItemEvent(
                event = event,
            )

        elif isinstance(event, GashaponNotRewardedNotSubscribedChatterItemEvent):
            await self.__handleGashaponNotRewardedNotSubscribedChatterItemEvent(
                event = event,
            )

        elif isinstance(event, GashaponResultsChatterItemEvent):
            await self.__handleGashaponResultsChatterItemEvent(
                event = event,
            )

        elif isinstance(event, GashaponRewardedChatterItemEvent):
            await self.__handleGashaponRewardedChatterItemEvent(
                event = event,
            )

        elif isinstance(event, GiveChatterItemEvent):
            await self.__handleGiveChatterItemEvent(
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

    async def __handleGashaponNotRewardedItemDisabledChatterItemEvent(
        self,
        event: GashaponNotRewardedItemDisabledChatterItemEvent,
    ):
        # For now, let's just not output a chat message for this.
        # But maybe this should change in the future.
        pass

    async def __handleGashaponNotRewardedNotFollowingChatterItemEvent(
        self,
        event: GashaponNotRewardedNotFollowingChatterItemEvent,
    ):
        self.__twitchChatMessenger.send(
            text = f'⚠ You must be following in order to receive a {ChatterItemType.GASHAPON.humanName}',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleGashaponNotRewardedNotReadyChatterItemEvent(
        self,
        event: GashaponNotRewardedNotReadyChatterItemEvent,
    ):
        now = self.__timeZoneRepository.getNow()
        remainingTime = event.nextGashaponAvailability - now
        totalRemainingSeconds = int(math.floor(remainingTime.total_seconds()))
        remainingDays = int(math.floor(float(totalRemainingSeconds) / float(24 * 60 * 60)))
        availableWhen: str

        if remainingDays >= 7:
            remainingDaysString = locale.format_string("%d", remainingDays, grouping = True)
            availableWhen = f'{remainingDaysString} days'
        elif remainingDays >= 3:
            availableWhen = utils.secondsToDurationMessage(
                secondsDuration = totalRemainingSeconds,
                includeMinutesAndSeconds = False,
            )
        else:
            availableWhen = utils.secondsToDurationMessage(
                secondsDuration = totalRemainingSeconds,
                includeMinutesAndSeconds = True,
            )

        self.__twitchChatMessenger.send(
            text = f'⚠ Sorry, you can\'t receive your {ChatterItemType.GASHAPON.humanName} yet! Your next will be available in {availableWhen}',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleGashaponNotRewardedNotSubscribedChatterItemEvent(
        self,
        event: GashaponNotRewardedNotSubscribedChatterItemEvent,
    ):
        self.__twitchChatMessenger.send(
            text = f'⚠ Sorry, you must be subscribed in order to receive a {ChatterItemType.GASHAPON.humanName}',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleGashaponResultsChatterItemEvent(
        self,
        event: GashaponResultsChatterItemEvent,
    ):
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
            text = f'{event.hypeEmote} ガチャ!! You received {awardedItemsString}',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleGashaponRewardedChatterItemEvent(
        self,
        event: GashaponRewardedChatterItemEvent,
    ):
        if event.user.areSoundAlertsEnabled:
            soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()
            self.__backgroundTaskHelper.createTask(soundPlayerManager.playSoundAlert(SoundAlert.GASHAPON))

        gashaponAmount = event.chatterInventory[ChatterItemType.GASHAPON]
        suffixString = ''

        if gashaponAmount > 1:
            gashaponAmountString = locale.format_string("%d", gashaponAmount, grouping = True)
            suffixString = f'You now have {gashaponAmountString} {ChatterItemType.GASHAPON.pluralHumanName}.'

        self.__twitchChatMessenger.send(
            text = f'{event.hypeEmote} Congrats, gashapon get! {suffixString}',
            twitchChannelId = event.twitchChannelId,
            replyMessageId = event.twitchChatMessageId,
        )

    async def __handleGiveChatterItemEvent(
        self,
        event: GiveChatterItemEvent,
    ):
        awardedItemsString: str

        if event.changeAmount == 1:
            awardedItemsString = f'{event.changeAmountString} {event.getItemType().humanName}'
        else:
            awardedItemsString = f'{event.changeAmountString} {event.getItemType().pluralHumanName}'

        self.__twitchChatMessenger.send(
            text = f'🪎 @{event.chatterUserName} you received {awardedItemsString}',
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
            text = f'ⓘ New {event.getItemType().humanName} counts — @{event.fromChatterUserName} {fromChatterQuantityString}, @{event.toChatterUserName} {toChatterQuantityString}',
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
