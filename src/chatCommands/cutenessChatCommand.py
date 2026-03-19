import re
from typing import Any, Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..cuteness.cutenessPresenterInterface import CutenessPresenterInterface
from ..cuteness.cutenessRepositoryInterface import CutenessRepositoryInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class CutenessChatCommand(AbsChatCommand2):

    def __init__(
        self,
        cutenessPresenter: CutenessPresenterInterface,
        cutenessRepository: CutenessRepositoryInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        delimiter: str = ', ',
    ):
        if not isinstance(cutenessPresenter, CutenessPresenterInterface):
            raise TypeError(f'cutenessPresenter argument is malformed: \"{cutenessPresenter}\"')
        elif not isinstance(cutenessRepository, CutenessRepositoryInterface):
            raise TypeError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        self.__cutenessPresenter: Final[CutenessPresenterInterface] = cutenessPresenter
        self.__cutenessRepository: Final[CutenessRepositoryInterface] = cutenessRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__delimiter: Final[str] = delimiter

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!cuteness\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'CutenessChatCommand'

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

        targetUserId: str | None
        result: Any

        # this means that a user is querying for another user's cuteness
        if targetUserName.casefold() != chatMessage.chatterUserName.casefold():
            targetUserId = await self.__userIdsRepository.fetchUserId(userName = targetUserName)

            if not utils.isValidStr(targetUserId):
                self.__twitchChatMessenger.send(
                    text = f'⚠ Unable to find cuteness info for \"{targetUserName}\"',
                    twitchChannelId = chatMessage.twitchChannelId,
                    replyMessageId = chatMessage.twitchChatMessageId,
                )
                return ChatCommandResult.HANDLED

            result = await self.__cutenessRepository.fetchCuteness(
                twitchChannel = chatMessage.twitchChannel,
                twitchChannelId = chatMessage.twitchChannelId,
                userId = targetUserId,
                userName = targetUserName,
            )

            printOut = await self.__cutenessPresenter.printCuteness(
                result = result,
            )

            self.__twitchChatMessenger.send(
                text = printOut,
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
        else:
            targetUserId = chatMessage.chatterUserId

            result = await self.__cutenessRepository.fetchCutenessLeaderboard(
                twitchChannel = chatMessage.twitchChannel,
                twitchChannelId = chatMessage.twitchChannelId,
                specificLookupUserId = targetUserId,
                specificLookupUserName = targetUserName,
            )

            printOut = await self.__cutenessPresenter.printLeaderboard(
                result = result,
                delimiter = self.__delimiter,
            )

            self.__twitchChatMessenger.send(
                text = printOut,
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

        self.__timber.log('CutenessChatCommand', f'Handled ({result=})')
        return ChatCommandResult.HANDLED
