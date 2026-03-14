import locale
import math
import re
from datetime import datetime
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..chatterInventory.helpers.gashaponRewardHelperInterface import GashaponRewardHelperInterface
from ..chatterInventory.models.chatterItemType import ChatterItemType
from ..chatterInventory.models.gashaponResults.chatterInventoryDisabledGashaponResult import \
    ChatterInventoryDisabledGashaponResult
from ..chatterInventory.models.gashaponResults.gashaponItemDisabledGashaponResult import \
    GashaponItemDisabledGashaponResult
from ..chatterInventory.models.gashaponResults.gashaponRewardedGashaponResult import GashaponRewardedGashaponResult
from ..chatterInventory.models.gashaponResults.notFollowingGashaponResult import NotFollowingGashaponResult
from ..chatterInventory.models.gashaponResults.notReadyGashaponResult import NotReadyGashaponResult
from ..chatterInventory.models.gashaponResults.notSubscribedGashaponResult import NotSubscribedGashaponResult
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..soundPlayerManager.provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ..soundPlayerManager.soundAlert import SoundAlert
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class GetGashaponItemChatCommand(AbsChatCommand2):

    def __init__(
        self,
        gashaponRewardHelper: GashaponRewardHelperInterface,
        soundPlayerManagerProvider: SoundPlayerManagerProviderInterface | None,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(gashaponRewardHelper, GashaponRewardHelperInterface):
            raise TypeError(f'gashaponRewardHelper argument is malformed: \"{gashaponRewardHelper}\"')
        elif soundPlayerManagerProvider is not None and not isinstance(soundPlayerManagerProvider, SoundPlayerManagerProviderInterface):
            raise TypeError(f'soundPlayerManagerProvider argument is malformed: \"{soundPlayerManagerProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__gashaponRewardHelper: Final[GashaponRewardHelperInterface] = gashaponRewardHelper
        self.__soundPlayerManagerProvider: Final[SoundPlayerManagerProviderInterface | None] = soundPlayerManagerProvider
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!(?:get\s*)?chest\b', re.IGNORECASE),
            re.compile(r'^\s*!(?:get\s*)?gacha(?:pon)?\b', re.IGNORECASE),
            re.compile(r'^\s*!(?:get\s*)?gasha(?:pon)?\b', re.IGNORECASE),
            re.compile(r'^\s*!(?:get\s*)?loot(?:box)?\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'GetGashaponItemChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isChatterInventoryEnabled:
            return ChatCommandResult.IGNORED

        gashaponResult = await self.__gashaponRewardHelper.checkAndGiveRewardIfAvailable(
            chatterUserId = chatMessage.chatterUserId,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        if isinstance(gashaponResult, ChatterInventoryDisabledGashaponResult):
            # this branch is intentionally empty
            pass

        elif isinstance(gashaponResult, GashaponItemDisabledGashaponResult):
            # this branch is intentionally empty
            pass

        elif isinstance(gashaponResult, GashaponRewardedGashaponResult):
            await self.__handleRewardedGashaponResult(
                chatMessage = chatMessage,
                gashaponResult = gashaponResult,
            )

        elif isinstance(gashaponResult, NotFollowingGashaponResult):
            self.__twitchChatMessenger.send(
                text = f'⚠ Sorry, you must be following in order to receive a gashapon',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

        elif isinstance(gashaponResult, NotReadyGashaponResult):
            await self.__handleNotReadyGashaponResult(
                chatMessage = chatMessage,
                gashaponResult = gashaponResult,
            )

        elif isinstance(gashaponResult, NotSubscribedGashaponResult):
            self.__twitchChatMessenger.send(
                text = f'⚠ Sorry, you must be subscribed in order to receive a gashapon',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

        else:
            # this branch is intentionally empty
            pass

        self.__timber.log(self.commandName, f'Handled ({chatMessage=}) ({gashaponResult=})')
        return ChatCommandResult.HANDLED

    async def __handleNotReadyGashaponResult(
        self,
        chatMessage: TwitchChatMessage,
        gashaponResult: NotReadyGashaponResult,
    ):
        now = datetime.now(self.__timeZoneRepository.getDefault())
        remainingTime = gashaponResult.nextGashaponAvailability - now
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
            text = f'⚠ Sorry, you can\'t receive your gashapon yet! Your next gashapon will be available in {availableWhen}',
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

    async def __handleRewardedGashaponResult(
        self,
        chatMessage: TwitchChatMessage,
        gashaponResult: GashaponRewardedGashaponResult,
    ):
        if chatMessage.twitchUser.areSoundAlertsEnabled and self.__soundPlayerManagerProvider is not None:
            soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()
            await soundPlayerManager.playSoundAlert(SoundAlert.GASHAPON)

        gashaponAmount = gashaponResult.inventory[ChatterItemType.GASHAPON]
        suffixString = ''

        if gashaponAmount > 1:
            gashaponAmountString = locale.format_string("%d", gashaponAmount, grouping = True)
            suffixString = f'You now have {gashaponAmountString} gashapons.'

        self.__twitchChatMessenger.send(
            text = f'{gashaponResult.hypeEmote} Congrats, gashapon get! {suffixString}',
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )
