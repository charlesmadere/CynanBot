import locale
import traceback
from typing import Final

from .absChatCommand import AbsChatCommand
from ..crowdControl.automator.crowdControlAutomatorAddResult import CrowdControlAutomatorAddResult
from ..crowdControl.automator.crowdControlAutomatorData import CrowdControlAutomatorData
from ..crowdControl.automator.crowdControlAutomatorInterface import CrowdControlAutomatorInterface
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class AddGameShuffleAutomatorChatCommand(AbsChatCommand):

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
            self.__timber.log('AddGameShuffleAutomatorChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} tried using this command!')
            return
        elif not user.isCrowdControlEnabled:
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('AddGameShuffleAutomatorChatCommand', f'Less than 2 arguments given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')

            self.__twitchChatMessenger.send(
                text = f'⚠ A number of seconds argument is necessary for the !addgameshuffleautomator command. Example using 5 minutes: !addgameshuffleautomator 300',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return

        reoccurSecondsStr: str | None = splits[1]

        try:
            reoccurSeconds = int(reoccurSecondsStr)
        except Exception as e:
            self.__timber.log('AddGameShuffleAutomatorChatCommand', f'Unable to convert reoccur seconds given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} into an int ({reoccurSecondsStr=})', e, traceback.format_exc())

            self.__twitchChatMessenger.send(
                text = f'⚠ The given number of seconds argument is malformed. Example using 5 minutes: !addgameshuffleautomator 300',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return

        if reoccurSeconds < 10 or reoccurSeconds > utils.getIntMaxSafeSize():
            self.__timber.log('AddGameShuffleAutomatorChatCommand', f'The reoccur seconds argument given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} is out of bounds ({reoccurSecondsStr=}) ({reoccurSeconds=})')

            self.__twitchChatMessenger.send(
                text = f'⚠ The given number of seconds argument is out of bounds. Example using 5 minutes: !addgameshuffleautomator 300',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return

        result = await self.__crowdControlAutomator.addGameShuffleAutomator(CrowdControlAutomatorData(
            reoccurSeconds = reoccurSeconds,
            twitchChannelId = await ctx.getTwitchChannelId(),
        ))

        reoccurSecondsStr = locale.format_string("%d", reoccurSeconds, grouping = True)

        match result:
            case CrowdControlAutomatorAddResult.OK:
                self.__twitchChatMessenger.send(
                    text = f'ⓘ Added {reoccurSecondsStr} second(s) game shuffle automator',
                    twitchChannelId = await ctx.getTwitchChannelId(),
                    replyMessageId = await ctx.getMessageId(),
                )

            case CrowdControlAutomatorAddResult.REPLACED:
                self.__twitchChatMessenger.send(
                    text = f'ⓘ Replaced existing game shuffle automator with a new {reoccurSecondsStr} second(s) game shuffle automator',
                    twitchChannelId = await ctx.getTwitchChannelId(),
                    replyMessageId = await ctx.getMessageId(),
                )

            case _:
                raise RuntimeError(f'Unknown CrowdControlAutomatorAddResult: \"{result}\"')

        self.__timber.log('AddGameShuffleAutomatorChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
