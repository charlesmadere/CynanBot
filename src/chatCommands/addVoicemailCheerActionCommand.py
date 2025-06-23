from typing import Final

from .absChatCommand import AbsChatCommand
from ..cheerActions.cheerActionType import CheerActionType
from ..cheerActions.cheerActionsWizardInterface import CheerActionsWizardInterface
from ..cheerActions.wizards.voicemail.voicemailStep import VoicemailStep
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class AddVoicemailCheerActionCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        cheerActionsWizard: CheerActionsWizardInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(cheerActionsWizard, CheerActionsWizardInterface):
            raise TypeError(f'cheerActionsWizard argument is malformed: \"{cheerActionsWizard}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__cheerActionsWizard: Final[CheerActionsWizardInterface] = cheerActionsWizard
        self.__timber: Final[TimberInterface] = timber
        self.__twitchUtils: Final[TwitchUtilsInterface] = twitchUtils
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        if not user.areCheerActionsEnabled:
            return

        userId = await ctx.getTwitchChannelId()
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if userId != ctx.getAuthorId() and administrator != ctx.getAuthorId():
            self.__timber.log('VoicemailCheerActionCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} tried using this command!')
            return

        wizard = await self.__cheerActionsWizard.start(
            cheerActionType = CheerActionType.VOICEMAIL,
            twitchChannel = user.handle,
            twitchChannelId = userId
        )

        step = wizard.currentStep

        if step is not VoicemailStep.BITS:
            raise RuntimeError(f'unknown VoicemailStep: \"{step}\"')

        await self.__twitchUtils.safeSend(
            messageable = ctx,
            message = f'ⓘ Please specify the number of bits for this Voicemail cheer action',
            replyMessageId = await ctx.getMessageId()
        )

        self.__timber.log('VoicemailCheerActionCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
