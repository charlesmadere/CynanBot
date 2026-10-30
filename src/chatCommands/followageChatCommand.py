import re
import traceback
from dataclasses import dataclass
from typing import Collection, Final, Pattern

from .absChatCommand import AbsChatCommand
from .chatCommandResult import ChatCommandResult
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.followingStatus.twitchFollowingStatusHelperInterface import TwitchFollowingStatusHelperInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ..twitch.userIds.twitchUserIdsHelperInterface import TwitchUserIdsHelperInterface


class FollowageChatCommand(AbsChatCommand):

    @dataclass(frozen = True, slots = True)
    class Arguments:
        chatterUserId: str
        chatterUserLogin: str
        chatterUserName: str

    def __init__(
        self,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchFollowingStatusHelper: TwitchFollowingStatusHelperInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        twitchUserIdsHelper: TwitchUserIdsHelperInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(twitchFollowingStatusHelper, TwitchFollowingStatusHelperInterface):
            raise TypeError(f'twitchFollowingStatusHelper argument is malformed: \"{twitchFollowingStatusHelper}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(twitchUserIdsHelper, TwitchUserIdsHelperInterface):
            raise TypeError(f'twitchUserIdsHelper argument is malformed: \"{twitchUserIdsHelper}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchFollowingStatusHelper: Final[TwitchFollowingStatusHelperInterface] = twitchFollowingStatusHelper
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__twitchUserIdsHelper: Final[TwitchUserIdsHelperInterface] = twitchUserIdsHelper

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!followage\b', re.IGNORECASE),
        })

        self.__argumentsPattern: Final[Pattern] = re.compile(r'^\s*!\w+\s+@?(\w+)', re.IGNORECASE)

    @property
    def commandName(self) -> str:
        return 'FollowageChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isFollowageCommandEnabled:
            return ChatCommandResult.IGNORED

        arguments = await self.__parseArguments(
            chatMessage = chatMessage,
        )

        if arguments is None:
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to find followage for the given user',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Unable to find target user ID ({arguments=}) ({chatMessage=})')
            return ChatCommandResult.CONSUMED

        result = await self.__twitchFollowingStatusHelper.fetch(
            twitchChannelId = chatMessage.twitchChannelId,
            userId = arguments.chatterUserId,
        )

        printOut: str

        if result is None:
            printOut = f'ⓘ @{arguments.chatterUserName} is not following'
        elif chatMessage.chatterUserId == arguments.chatterUserId:
            printOut = f'🗓️ you\'ve been following for {result.durationMessage}'
        else:
            printOut = f'🗓️ @{result.getUserName()} has been following for {result.durationMessage}'

        self.__twitchChatMessenger.send(
            text = printOut,
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Consumed ({result=}) ({arguments=}) ({chatMessage=})')
        return ChatCommandResult.CONSUMED

    async def __parseArguments(self, chatMessage: TwitchChatMessage) -> Arguments | None:
        argumentsMatch = self.__argumentsPattern.match(chatMessage.text)
        if argumentsMatch is None:
            return FollowageChatCommand.Arguments(
                chatterUserId = chatMessage.chatterUserId,
                chatterUserLogin = chatMessage.chatterUserLogin,
                chatterUserName = chatMessage.chatterUserName,
            )

        chatterUserName = argumentsMatch.group(1)

        try:
            chatterUserData = await self.__twitchUserIdsHelper.requireByLoginOrName(
                userLoginOrName = chatterUserName,
                twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
                    twitchChannelId = chatMessage.twitchChannelId,
                ),
            )
        except Exception as e:
            self.__timber.log(self.commandName, f'Failed to fetch user ID for the given chatter username ({chatterUserName=}) ({argumentsMatch=}) ({chatMessage=})', e, traceback.format_exc())
            return None

        return FollowageChatCommand.Arguments(
            chatterUserId = chatterUserData.userId,
            chatterUserLogin = chatterUserData.userLogin,
            chatterUserName = chatterUserData.userName,
        )
