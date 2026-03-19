import re
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..misc import utils as utils
from ..misc.generalSettingsRepository import GeneralSettingsRepository
from ..timber.timberInterface import TimberInterface
from ..trivia.score.triviaScoreRepositoryInterface import TriviaScoreRepositoryInterface
from ..trivia.specialStatus.shinyTriviaOccurencesRepositoryInterface import ShinyTriviaOccurencesRepositoryInterface
from ..trivia.specialStatus.toxicTriviaOccurencesRepositoryInterface import ToxicTriviaOccurencesRepositoryInterface
from ..trivia.triviaUtilsInterface import TriviaUtilsInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class TriviaScoreChatCommand(AbsChatCommand2):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        shinyTriviaOccurencesRepository: ShinyTriviaOccurencesRepositoryInterface,
        timber: TimberInterface,
        toxicTriviaOccurencesRepository: ToxicTriviaOccurencesRepositoryInterface,
        triviaScoreRepository: TriviaScoreRepositoryInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        userIdsRepository: UserIdsRepositoryInterface,
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(shinyTriviaOccurencesRepository, ShinyTriviaOccurencesRepositoryInterface):
            raise TypeError(f'shinyTriviaOccurencesRepository argument is malformed: \"{shinyTriviaOccurencesRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(toxicTriviaOccurencesRepository, ToxicTriviaOccurencesRepositoryInterface):
            raise TypeError(f'toxicTriviaOccurencesRepository argument is malformed: \"{toxicTriviaOccurencesRepository}\"')
        elif not isinstance(triviaScoreRepository, TriviaScoreRepositoryInterface):
            raise TypeError(f'triviaScoreRepository argument is malformed: \"{triviaScoreRepository}\"')
        elif not isinstance(triviaUtils, TriviaUtilsInterface):
            raise TypeError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__generalSettingsRepository: Final[GeneralSettingsRepository] = generalSettingsRepository
        self.__shinyTriviaOccurencesRepository: Final[ShinyTriviaOccurencesRepositoryInterface] = shinyTriviaOccurencesRepository
        self.__timber: Final[TimberInterface] = timber
        self.__toxicTriviaOccurencesRepository: Final[ToxicTriviaOccurencesRepositoryInterface] = toxicTriviaOccurencesRepository
        self.__triviaScoreRepository: Final[TriviaScoreRepositoryInterface] = triviaScoreRepository
        self.__triviaUtils: Final[TriviaUtilsInterface] = triviaUtils
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!triviascore\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'TriviaScoreChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isTriviaGameEnabled and not chatMessage.twitchUser.isSuperTriviaGameEnabled:
            return ChatCommandResult.IGNORED

        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        if not generalSettings.isTriviaGameEnabled() and not generalSettings.isSuperTriviaGameEnabled():
            return ChatCommandResult.IGNORED

        targetUserId = chatMessage.chatterUserId
        targetUserName = chatMessage.chatterUserName
        splits = utils.getCleanedSplits(chatMessage.text)

        if len(splits) >= 2 and utils.strContainsAlphanumericCharacters(splits[1]):
            targetUserName = utils.removePreceedingAt(splits[1])

        # this means that a user is querying for another user's trivia score
        if targetUserName.casefold() != chatMessage.chatterUserName:
            targetUserId = await self.__userIdsRepository.fetchUserId(userName = targetUserName)

            if not utils.isValidStr(targetUserId):
                self.__timber.log(self.commandName, f'Unable to find target user ID ({targetUserName=}) ({splits=}) ({chatMessage=})')

                self.__twitchChatMessenger.send(
                    text = f'⚠ Unable to find trivia score info for \"{targetUserName}\"',
                    twitchChannelId = chatMessage.twitchChannelId,
                    replyMessageId = chatMessage.twitchChatMessageId,
                )
                return ChatCommandResult.HANDLED

        shinyResult = await self.__shinyTriviaOccurencesRepository.fetchDetails(
            twitchChannel = chatMessage.twitchChannel,
            twitchChannelId = chatMessage.twitchChannelId,
            userId = targetUserId,
        )

        toxicResult = await self.__toxicTriviaOccurencesRepository.fetchDetails(
            twitchChannel = chatMessage.twitchChannel,
            twitchChannelId = chatMessage.twitchChannelId,
            userId = targetUserId,
        )

        triviaResult = await self.__triviaScoreRepository.fetchTriviaScore(
            twitchChannel = chatMessage.twitchChannel,
            twitchChannelId = chatMessage.twitchChannelId,
            userId = targetUserId,
        )

        message = await self.__triviaUtils.getTriviaScoreMessage(
            shinyResult = shinyResult,
            userName = targetUserName,
            toxicResult = toxicResult,
            triviaResult = triviaResult,
        )

        self.__twitchChatMessenger.send(
            text = message,
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Handled ({shinyResult=}) ({toxicResult=}) ({triviaResult=})')
        return ChatCommandResult.HANDLED
