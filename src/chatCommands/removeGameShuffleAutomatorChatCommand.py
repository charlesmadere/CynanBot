from typing import Final

from .absChatCommand import AbsChatCommand
from ..crowdControl.automator.crowdControlAutomatorInterface import CrowdControlAutomatorInterface
from ..crowdControl.automator.crowdControlAutomatorRemovalResult import CrowdControlAutomatorRemovalResult
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class RemoveGameShuffleAutomatorChatCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        crowdControlAutomator: CrowdControlAutomatorInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        usersRepository: UsersRepositoryInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        if not isinstance(crowdControlAutomator, CrowdControlAutomatorInterface):
            raise TypeError(f'crowdControlAutomator argument is malformed: \"{crowdControlAutomator}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__crowdControlAutomator: Final[CrowdControlAutomatorInterface] = crowdControlAutomator
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        userId = await ctx.getTwitchChannelId()
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if userId != ctx.getAuthorId() and administrator != ctx.getAuthorId():
            self.__timber.log('RemoveGameShuffleAutomatorChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} tried using this command!')
            return
        elif not user.isCrowdControlEnabled:
            return

        result = await self.__crowdControlAutomator.removeGameShuffleAutomator(
            twitchChannelId = await ctx.getTwitchChannelId(),
        )

        match result:
            case CrowdControlAutomatorRemovalResult.DID_NOT_EXIST:
                self.__twitchChatMessenger.send(
                    text = f'ⓘ Attempted to remove the game shuffle automator, but one did not already exist',
                    twitchChannelId = await ctx.getTwitchChannelId(),
                    replyMessageId = await ctx.getMessageId(),
                )

            case CrowdControlAutomatorRemovalResult.OK:
                self.__twitchChatMessenger.send(
                    text = f'ⓘ Removed game shuffle automator',
                    twitchChannelId = await ctx.getTwitchChannelId(),
                    replyMessageId = await ctx.getMessageId(),
                )

            case _:
                raise RuntimeError(f'Unknown CrowdControlAutomatorRemovalResult: \"{result}\"')

        self.__timber.log('RemoveGameShuffleAutomatorChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
