import re
import traceback
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..cuteness.cutenessRepositoryInterface import CutenessRepositoryInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..trivia.triviaUtilsInterface import TriviaUtilsInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.handleProvider.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class GiveCutenessChatCommand(AbsChatCommand2):

    def __init__(
        self,
        cutenessRepository: CutenessRepositoryInterface,
        timber: TimberInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        userIdsRepository: UserIdsRepositoryInterface,
    ):
        if not isinstance(cutenessRepository, CutenessRepositoryInterface):
            raise TypeError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaUtils, TriviaUtilsInterface):
            raise TypeError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__cutenessRepository: Final[CutenessRepositoryInterface] = cutenessRepository
        self.__timber: Final[TimberInterface] = timber
        self.__triviaUtils: Final[TriviaUtilsInterface] = triviaUtils
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!givecuteness\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'GiveCutenessChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isCutenessEnabled or not chatMessage.twitchUser.isGiveCutenessEnabled:
            return ChatCommandResult.IGNORED
        elif not await self.__triviaUtils.isPrivilegedTriviaUser(
            twitchChannelId = chatMessage.twitchChannelId,
            userId = chatMessage.chatterUserId,
        ):
            return ChatCommandResult.IGNORED

        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()

        splits = utils.getCleanedSplits(chatMessage.text)
        if len(splits) < 3:
            self.__timber.log(self.commandName, f'Less than 2 arguments given ({chatMessage=}) ({splits=})')
            self.__twitchChatMessenger.send(
                text = f'⚠ Username and amount is necessary for this command. Example: !givecuteness @{twitchHandle} 5',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
            return ChatCommandResult.HANDLED

        targetUserName: str | None = splits[1]
        if not utils.isValidStr(targetUserName) or not utils.strContainsAlphanumericCharacters(targetUserName):
            self.__timber.log(self.commandName, f'Given target username is malformed ({chatMessage=}) ({splits=}) ({targetUserName=})')
            self.__twitchChatMessenger.send(
                text = f'⚠ Username argument is malformed. Example: !givecuteness @{twitchHandle} 5',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
            return ChatCommandResult.HANDLED

        targetUserName = utils.removePreceedingAt(targetUserName)
        incrementAmountStr: str | None = splits[2]

        try:
            incrementAmount = int(incrementAmountStr)
        except Exception as e:
            self.__timber.log(self.commandName, f'Unable to convert increment amount into an int ({chatMessage=}) ({splits=}) ({targetUserName=}) ({incrementAmountStr=})', e, traceback.format_exc())
            self.__twitchChatMessenger.send(
                text = f'⚠ Increment amount argument is malformed. Example: !givecuteness @{targetUserName} 5',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
            return ChatCommandResult.HANDLED

        targetUserId = await self.__userIdsRepository.fetchUserId(userName = targetUserName)

        if not utils.isValidStr(targetUserId):
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to fetch user ID for \"{targetUserName}\"',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
            return ChatCommandResult.HANDLED

        try:
            result = await self.__cutenessRepository.fetchCutenessIncrementedBy(
                incrementAmount = incrementAmount,
                twitchChannel = chatMessage.twitchChannel,
                twitchChannelId = chatMessage.twitchChannelId,
                userId = targetUserId,
                userName = targetUserName,
            )

            self.__twitchChatMessenger.send(
                text = f'ⓘ Cuteness for @{targetUserName} is now {result.newCutenessStr} (was previously {result.previousCutenessStr})',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
        except (OverflowError, ValueError) as e:
            self.__timber.log(self.commandName, f'Error giving cuteness ({chatMessage=}) ({incrementAmount=}) ({targetUserId=}) ({targetUserName=})', e, traceback.format_exc())
            self.__twitchChatMessenger.send(
                text = f'⚠ Error giving cuteness to \"{targetUserName}\"',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

        self.__timber.log(self.commandName, f'Handled ({chatMessage=}) ({incrementAmount=}) ({targetUserId=}) ({targetUserName=})')
        return ChatCommandResult.HANDLED
