from CynanBot.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBot.chatCommands.absChatCommand import AbsChatCommand
from CynanBot.language.languagesRepositoryInterface import \
    LanguagesRepositoryInterface
from CynanBot.recurringActions.recurringActionsRepositoryInterface import \
    RecurringActionsRepositoryInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.configuration.twitchContext import TwitchContext
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBot.users.usersRepositoryInterface import UsersRepositoryInterface


class AddRecurringActionCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        languagesRepository: LanguagesRepositoryInterface,
        recurringActionsRepository: RecurringActionsRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        assert isinstance(administratorProvider, AdministratorProviderInterface), f"malformed {administratorProvider=}"
        assert isinstance(languagesRepository, LanguagesRepositoryInterface), f"malformed {languagesRepository=}"
        assert isinstance(recurringActionsRepository, RecurringActionsRepositoryInterface), f"malformed {recurringActionsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(userIdsRepository, UserIdsRepositoryInterface), f"malformed {userIdsRepository=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__languagesRepository: LanguagesRepositoryInterface = languagesRepository
        self.__recurringActionsRepository: RecurringActionsRepositoryInterface = recurringActionsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        # TODO
        pass
