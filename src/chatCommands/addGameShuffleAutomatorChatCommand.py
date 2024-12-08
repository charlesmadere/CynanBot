from .absChatCommand import AbsChatCommand
from ..crowdControl.automator.crowdControlAutomatorInterface import CrowdControlAutomatorInterface
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class AddGameShuffleAutomatorChatCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        crowdControlAutomator: CrowdControlAutomatorInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        if not isinstance(crowdControlAutomator, CrowdControlAutomatorInterface):
            raise TypeError(f'crowdControlAutomator argument is malformed: \"{crowdControlAutomator}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__crowdControlAutomator: CrowdControlAutomatorInterface = crowdControlAutomator
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

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

        # TODO
        # (1) Check user input for a seconds argument
        # (2) If there is no seconds argument, notify the user
        # (3) Make sure it is sane
        # (4) If it is not sane, notify the user
        # (5) If everything is OK:
        #     (a) add the automator
        #     (b) notify the user of the add result

        self.__timber.log('AddGameShuffleAutomatorChatCommand', f'Handled !addgameshuffleautomator command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
