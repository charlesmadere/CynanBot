from datetime import datetime
from typing import Final

from .absChatCommand import AbsChatCommand
from ..crowdControl.actions.buttonPressCrowdControlAction import ButtonPressCrowdControlAction
from ..crowdControl.actions.crowdControlAction import CrowdControlAction
from ..crowdControl.actions.gameShuffleCrowdControlAction import GameShuffleCrowdControlAction
from ..crowdControl.crowdControlMachineInterface import CrowdControlMachineInterface
from ..crowdControl.idGenerator.crowdControlIdGeneratorInterface import CrowdControlIdGeneratorInterface
from ..crowdControl.utils.crowdControlUserInputUtilsInterface import CrowdControlUserInputUtilsInterface
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class CrowdControlChatCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        crowdControlIdGenerator: CrowdControlIdGeneratorInterface,
        crowdControlMachine: CrowdControlMachineInterface,
        crowdControlUserInputUtils: CrowdControlUserInputUtilsInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        usersRepository: UsersRepositoryInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(crowdControlIdGenerator, CrowdControlIdGeneratorInterface):
            raise TypeError(f'crowdControlIdGenerator argument is malformed: \"{crowdControlIdGenerator}\"')
        elif not isinstance(crowdControlMachine, CrowdControlMachineInterface):
            raise TypeError(f'crowdControlMachine argument is malformed: \"{crowdControlMachine}\"')
        elif not isinstance(crowdControlUserInputUtils, CrowdControlUserInputUtilsInterface):
            raise TypeError(f'crowdControlUserInputUtils  argument is malformed: \"{crowdControlUserInputUtils}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__crowdControlIdGenerator: Final[CrowdControlIdGeneratorInterface] = crowdControlIdGenerator
        self.__crowdControlMachine: Final[CrowdControlMachineInterface] = crowdControlMachine
        self.__crowdControlUserInputUtils: Final[CrowdControlUserInputUtilsInterface] = crowdControlUserInputUtils
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isCrowdControlEnabled:
            return

        twitchChannelId = await ctx.getTwitchChannelId()
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if twitchChannelId != ctx.getAuthorId() and administrator != ctx.getAuthorId():
            self.__timber.log('CrowdControlChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} tried using this command!')
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())

        message: str | None = None
        if len(splits) >= 2:
            message = splits[1].strip()

        button = await self.__crowdControlUserInputUtils.parseButtonFromUserInput(message)
        now = datetime.now(self.__timeZoneRepository.getDefault())
        actionId = await self.__crowdControlIdGenerator.generateActionId()
        crowdControlAction: CrowdControlAction

        if button is None:
            crowdControlAction = GameShuffleCrowdControlAction(
                dateTime = now,
                entryWithinGigaShuffle = False,
                startOfGigaShuffleSize = None,
                actionId = actionId,
                chatterUserId = ctx.getAuthorId(),
                chatterUserName = ctx.getAuthorName(),
                twitchChannel = user.handle,
                twitchChannelId = twitchChannelId,
                twitchChatMessageId = await ctx.getMessageId(),
            )
        else:
            crowdControlAction = ButtonPressCrowdControlAction(
                button = button,
                dateTime = now,
                actionId = actionId,
                chatterUserId = ctx.getAuthorId(),
                chatterUserName = ctx.getAuthorName(),
                twitchChannel = user.handle,
                twitchChannelId = twitchChannelId,
                twitchChatMessageId = await ctx.getMessageId(),
            )

        self.__crowdControlMachine.submitAction(crowdControlAction)

        self.__twitchChatMessenger.send(
            text = f'ⓘ Handled crowd control action ({button=}) ({crowdControlAction.actionType=})',
            twitchChannelId = twitchChannelId,
            replyMessageId = await ctx.getMessageId(),
        )

        self.__timber.log('CrowdControlChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} ({button=})')
