from typing import Final

from .absChatCommand import AbsChatCommand
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..users.addOrRemoveUserActionType import AddOrRemoveUserActionType
from ..users.addOrRemoveUserDataHelperInterface import AddOrRemoveUserDataHelperInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class ConfirmChatCommand(AbsChatCommand):

    def __init__(
        self,
        addOrRemoveUserDataHelper: AddOrRemoveUserDataHelperInterface,
        administratorProvider: AdministratorProviderInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        usersRepository: UsersRepositoryInterface,
    ):
        if not isinstance(addOrRemoveUserDataHelper, AddOrRemoveUserDataHelperInterface):
            raise TypeError(f'addOrRemoveUserDataHelper argument is malformed: \"{addOrRemoveUserDataHelper}\"')
        elif not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__addOrRemoveUserDataHelper: Final[AddOrRemoveUserDataHelperInterface] = addOrRemoveUserDataHelper
        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if ctx.getAuthorId() != await self.__administratorProvider.getAdministratorUserId():
            self.__timber.log('ConfirmCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} tried using this command!')
            return

        data = await self.__addOrRemoveUserDataHelper.getData()

        if data is None:
            self.__timber.log('ConfirmCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} tried confirming the modification of a user, but there is no persisted user data')
            return

        match data.actionType:
            case AddOrRemoveUserActionType.ADD:
                await self.__usersRepository.addUser(data.userName)

            case AddOrRemoveUserActionType.REMOVE:
                await self.__usersRepository.removeUser(data.userName)

            case _:
                raise RuntimeError(f'unknown AddOrRemoveUserActionType: \"{data.actionType}\"')

        await self.__addOrRemoveUserDataHelper.notifyAddOrRemoveUserEventListenerAndClearData()
        self.__timber.log('CommandsCommand', f'Handled !confirm command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
