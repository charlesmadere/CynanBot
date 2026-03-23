import re
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..misc.generalSettingsRepository import GeneralSettingsRepository
from ..timber.timberInterface import TimberInterface
from ..trivia.gameController.triviaGameGlobalControllersRepositoryInterface import \
    TriviaGameGlobalControllersRepositoryInterface
from ..trivia.triviaUtilsInterface import TriviaUtilsInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class GetGlobalTriviaControllersChatCommand(AbsChatCommand2):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        triviaGameGlobalControllersRepository: TriviaGameGlobalControllersRepositoryInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProviderInterface argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameGlobalControllersRepository, TriviaGameGlobalControllersRepositoryInterface):
            raise TypeError(f'triviaGameGlobalControllersRepository argument is malformed: \"{triviaGameGlobalControllersRepository}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__generalSettingsRepository: Final[GeneralSettingsRepository] = generalSettingsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__triviaGameGlobalControllersRepository: Final[TriviaGameGlobalControllersRepositoryInterface] = triviaGameGlobalControllersRepository
        self.__triviaUtils: Final[TriviaUtilsInterface] = triviaUtils
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!(?:get)?globaltriviacontrollers?\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'GetGlobalTriviaControllersChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        if not generalSettings.isTriviaGameEnabled() and not generalSettings.isSuperTriviaGameEnabled():
            return ChatCommandResult.IGNORED
        elif chatMessage.chatterUserId != await self.__administratorProvider.getAdministratorUserId():
            return ChatCommandResult.IGNORED

        controllers = await self.__triviaGameGlobalControllersRepository.getControllers()

        printOut = await self.__triviaUtils.getTriviaGameGlobalControllers(
            gameControllers = controllers,
        )

        self.__twitchChatMessenger.send(
            text = printOut,
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Handled ({printOut=}) ({controllers=})')
        return ChatCommandResult.HANDLED
