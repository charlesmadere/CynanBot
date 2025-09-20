from abc import ABC, abstractmethod

from .misc.administratorProviderInterface import AdministratorProviderInterface
from .timber.timberInterface import TimberInterface
from .twitch.configuration.twitchContext import TwitchContext
from .twitch.twitchUtilsInterface import TwitchUtilsInterface
from .users.addOrRemoveUserActionType import AddOrRemoveUserActionType
from .users.addOrRemoveUserDataHelperInterface import AddOrRemoveUserDataHelperInterface
from .users.usersRepositoryInterface import UsersRepositoryInterface


class AbsCommand(ABC):

    @abstractmethod
    async def handleCommand(self, ctx: TwitchContext):
        pass


class ConfirmCommand(AbsCommand):

    def __init__(
        self,
        addOrRemoveUserDataHelper: AddOrRemoveUserDataHelperInterface,
        administratorProvider: AdministratorProviderInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(addOrRemoveUserDataHelper, AddOrRemoveUserDataHelperInterface):
            raise ValueError(f'addOrRemoveUserDataHelper argument is malformed: \"{addOrRemoveUserDataHelper}\"')
        elif not isinstance(administratorProvider, AdministratorProviderInterface):
            raise ValueError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__addOrRemoveUserDataHelper: AddOrRemoveUserDataHelperInterface = addOrRemoveUserDataHelper
        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if ctx.getAuthorId() != administrator:
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


class StubCommand(AbsCommand):

    def __init__(self):
        pass

    async def handleCommand(self, ctx: TwitchContext):
        pass
