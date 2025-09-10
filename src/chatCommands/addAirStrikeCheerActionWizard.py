from typing import Final

from .absChatCommand import AbsChatCommand
from ..cheerActions.cheerActionType import CheerActionType
from ..cheerActions.cheerActionsWizardInterface import CheerActionsWizardInterface
from ..cheerActions.wizards.airStrike.airStrikeStep import AirStrikeStep
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class AddAirStrikeCheerActionCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        cheerActionsWizard: CheerActionsWizardInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        usersRepository: UsersRepositoryInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(cheerActionsWizard, CheerActionsWizardInterface):
            raise TypeError(f'cheerActionsWizard argument is malformed: \"{cheerActionsWizard}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__cheerActionsWizard: Final[CheerActionsWizardInterface] = cheerActionsWizard
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.areCheerActionsEnabled:
            return

        twitchChannelId = await ctx.getTwitchChannelId()
        administratorId = await self.__administratorProvider.getAdministratorUserId()

        if ctx.getAuthorId() != twitchChannelId and ctx.getAuthorId() != administratorId:
            self.__timber.log('AddAirStrikeCheerActionCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} tried using this command!')
            return

        wizard = await self.__cheerActionsWizard.start(
            cheerActionType = CheerActionType.AIR_STRIKE,
            twitchChannel = user.handle,
            twitchChannelId = twitchChannelId,
        )

        step = wizard.currentStep

        if step is not AirStrikeStep.BITS:
            raise RuntimeError(f'unknown AirStrikeStep: \"{step}\"')

        self.__twitchChatMessenger.send(
            text = f'ⓘ Please specify the number of bits for this Air Strike cheer action',
            twitchChannelId = twitchChannelId,
            replyMessageId = await ctx.getMessageId(),
        )

        self.__timber.log('AddAirStrikeCheerActionCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
