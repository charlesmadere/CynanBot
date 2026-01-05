from datetime import datetime
from typing import Final

from .absChatCommand import AbsChatCommand
from ..chatterInventory.helpers.gashaponRewardHelperInterface import GashaponRewardHelperInterface
from ..chatterInventory.models.gashaponResults.chatterInventoryDisabledGashaponResult import \
    ChatterInventoryDisabledGashaponResult
from ..chatterInventory.models.gashaponResults.gashaponItemDisabledGashaponResult import \
    GashaponItemDisabledGashaponResult
from ..chatterInventory.models.gashaponResults.gashaponRewardedGashaponResult import GashaponRewardedGashaponResult
from ..chatterInventory.models.gashaponResults.notFollowingGashaponResult import NotFollowingGashaponResult
from ..chatterInventory.models.gashaponResults.notReadyGashaponResult import NotReadyGashaponResult
from ..chatterInventory.models.gashaponResults.notSubscribedGashaponResult import NotSubscribedGashaponResult
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..soundPlayerManager.provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class GetGashaponItemChatCommand(AbsChatCommand):

    def __init__(
        self,
        gashaponRewardHelper: GashaponRewardHelperInterface,
        soundPlayerManagerProvider: SoundPlayerManagerProviderInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        usersRepository: UsersRepositoryInterface,
    ):
        if not isinstance(gashaponRewardHelper, GashaponRewardHelperInterface):
            raise TypeError(f'gashaponRewardHelper argument is malformed: \"{gashaponRewardHelper}\"')
        elif not isinstance(soundPlayerManagerProvider, SoundPlayerManagerProviderInterface):
            raise TypeError(f'soundPlayerManagerProvider argument is malformed: \"{soundPlayerManagerProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__gashaponRewardHelper: Final[GashaponRewardHelperInterface] = gashaponRewardHelper
        self.__soundPlayerManagerProvider: Final[SoundPlayerManagerProviderInterface] = soundPlayerManagerProvider
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isChatterInventoryEnabled:
            return

        gashaponResult = await self.__gashaponRewardHelper.checkAndGiveRewardIfAvailable(
            chatterUserId = ctx.getAuthorId(),
            twitchChannelId = await ctx.getTwitchChannelId(),
        )

        if isinstance(gashaponResult, ChatterInventoryDisabledGashaponResult):
            # this branch is intentionally empty
            pass

        elif isinstance(gashaponResult, GashaponItemDisabledGashaponResult):
            # this branch is intentionally empty
            pass

        elif isinstance(gashaponResult, GashaponRewardedGashaponResult):
            await self.__handleRewardedGashaponResult(
                ctx = ctx,
                gashaponResult = gashaponResult,
            )

        elif isinstance(gashaponResult, NotFollowingGashaponResult):
            self.__twitchChatMessenger.send(
                text = f'⚠ Sorry, you must be following in order to receive a gashapon',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )

        elif isinstance(gashaponResult, NotReadyGashaponResult):
            await self.__handleNotReadyGashaponResult(
                ctx = ctx,
                gashaponResult = gashaponResult,
            )

        elif isinstance(gashaponResult, NotSubscribedGashaponResult):
            self.__twitchChatMessenger.send(
                text = f'⚠ Sorry, you must be subscribed in order to receive a gashapon',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )

        else:
            self.__timber.log('GetGashaponItemChatCommand', f'Received unhandled gashapon result ({gashaponResult=}) when handling command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')

        self.__timber.log('GetGashaponItemChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')

    async def __handleNotReadyGashaponResult(
        self,
        ctx: TwitchContext,
        gashaponResult: NotReadyGashaponResult,
    ):
        now = datetime.now(self.__timeZoneRepository.getDefault())
        remainingTime = gashaponResult.nextGashaponAvailability - now

        # TODO

        self.__twitchChatMessenger.send(
            text = f'⚠ Sorry, you can\'t receive another gashapon yet! Your next gashapon will be available on ',
            twitchChannelId = await ctx.getTwitchChannelId(),
            replyMessageId = await ctx.getMessageId(),
        )

    async def __handleRewardedGashaponResult(
        self,
        ctx: TwitchContext,
        gashaponResult: GashaponRewardedGashaponResult,
    ):
        # TODO
        pass
