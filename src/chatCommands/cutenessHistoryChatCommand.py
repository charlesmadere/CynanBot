import re
from typing import Any, Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..cuteness.cutenessRepositoryInterface import CutenessRepositoryInterface
from ..cuteness.cutenessUtilsInterface import CutenessUtilsInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class CutenessHistoryChatCommand(AbsChatCommand2):

    def __init__(
        self,
        cutenessRepository: CutenessRepositoryInterface,
        cutenessUtils: CutenessUtilsInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        entryDelimiter: str = ', ',
        leaderboardDelimiter: str = ' — ',
    ):
        if not isinstance(cutenessRepository, CutenessRepositoryInterface):
            raise TypeError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif not isinstance(cutenessUtils, CutenessUtilsInterface):
            raise TypeError(f'cutenessUtils argument is malformed: \"{cutenessUtils}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(entryDelimiter, str):
            raise TypeError(f'entryDelimiter argument is malformed: \"{entryDelimiter}\"')
        elif not isinstance(leaderboardDelimiter, str):
            raise TypeError(f'leaderboardDelimiter argument is malformed: \"{leaderboardDelimiter}\"')

        self.__cutenessRepository: Final[CutenessRepositoryInterface] = cutenessRepository
        self.__cutenessUtils: Final[CutenessUtilsInterface] = cutenessUtils
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__entryDelimiter: Final[str] = entryDelimiter
        self.__leaderboardDelimiter: Final[str] = leaderboardDelimiter

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!cutenesshistory\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'CutenessHistoryChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isCutenessEnabled:
            return ChatCommandResult.IGNORED

        targetUserName = chatMessage.chatterUserName
        splits = utils.getCleanedSplits(chatMessage.text)

        if len(splits) >= 2 and utils.strContainsAlphanumericCharacters(splits[1]):
            targetUserName = utils.removePreceedingAt(splits[1])

        result: Any

        # this means that a user is querying for another user's cuteness history
        if targetUserName.casefold() != chatMessage.chatterUserName.casefold():
            targetUserId = await self.__userIdsRepository.fetchUserId(userName = targetUserName)

            if not utils.isValidStr(targetUserId):
                self.__timber.log(self.commandName, f'Unable to find target user ID ({targetUserName=}) ({splits=}) ({chatMessage=})')

                self.__twitchChatMessenger.send(
                    text = f'⚠ Unable to find cuteness info for \"{targetUserName}\"',
                    twitchChannelId = chatMessage.twitchChannelId,
                    replyMessageId = chatMessage.twitchChatMessageId,
                )
                return ChatCommandResult.HANDLED

            result = await self.__cutenessRepository.fetchCutenessHistory(
                twitchChannel = chatMessage.twitchChannel,
                twitchChannelId = chatMessage.twitchChannelId,
                userId = targetUserId,
                userName = targetUserName,
            )

            message = self.__cutenessUtils.getCutenessHistory(
                result = result,
                delimiter = self.__entryDelimiter,
            )

            self.__twitchChatMessenger.send(
                text = message,
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
        else:
            result = await self.__cutenessRepository.fetchCutenessLeaderboardHistory(
                twitchChannel = chatMessage.twitchChannel,
                twitchChannelId = chatMessage.twitchChannelId,
            )

            message = self.__cutenessUtils.getCutenessLeaderboardHistory(
                result = result,
                entryDelimiter = self.__entryDelimiter,
                leaderboardDelimiter = self.__leaderboardDelimiter,
            )

            self.__twitchChatMessenger.send(
                text = message,
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

        self.__timber.log(self.commandName, f'Handled ({result=})')
        return ChatCommandResult.HANDLED
