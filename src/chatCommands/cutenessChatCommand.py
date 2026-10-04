import re
import traceback
from dataclasses import dataclass
from typing import Collection, Final, Pattern

from .absChatCommand import AbsChatCommand
from .chatCommandResult import ChatCommandResult
from ..cuteness.cutenessPresenterInterface import CutenessPresenterInterface
from ..cuteness.helpers.cutenessHelperInterface import CutenessHelperInterface
from ..cuteness.settings.cutenessSettingsInterface import CutenessSettingsInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ..twitch.userIds.twitchUserIdsHelperInterface import TwitchUserIdsHelperInterface


class CutenessChatCommand(AbsChatCommand):

    @dataclass(frozen = True, slots = True)
    class Arguments:
        chatterUserId: str
        chatterUserLogin: str
        chatterUserName: str

    def __init__(
        self,
        cutenessHelper: CutenessHelperInterface,
        cutenessPresenter: CutenessPresenterInterface,
        cutenessSettings: CutenessSettingsInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        twitchUserIdsHelper: TwitchUserIdsHelperInterface,
    ):
        if not isinstance(cutenessHelper, CutenessHelperInterface):
            raise TypeError(f'cutenessHelper argument is malformed: \"{cutenessHelper}\"')
        elif not isinstance(cutenessPresenter, CutenessPresenterInterface):
            raise TypeError(f'cutenessPresenter argument is malformed: \"{cutenessPresenter}\"')
        elif not isinstance(cutenessSettings, CutenessSettingsInterface):
            raise TypeError(f'cutenessSettings argument is malformed: \"{cutenessSettings}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(twitchUserIdsHelper, TwitchUserIdsHelperInterface):
            raise TypeError(f'twitchUserIdsHelper argument is malformed: \"{twitchUserIdsHelper}\"')

        self.__cutenessHelper: Final[CutenessHelperInterface] = cutenessHelper
        self.__cutenessPresenter: Final[CutenessPresenterInterface] = cutenessPresenter
        self.__cutenessSettings: Final[CutenessSettingsInterface] = cutenessSettings
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__twitchUserIdsHelper: Final[TwitchUserIdsHelperInterface] = twitchUserIdsHelper

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!cuteness\b', re.IGNORECASE),
        })

        self.__argumentsPattern: Final[Pattern] = re.compile(r'^\s*!\w+\s+@?(\w+)', re.IGNORECASE)

    @property
    def commandName(self) -> str:
        return 'CutenessChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isCutenessEnabled:
            return ChatCommandResult.IGNORED
        elif not await self.__cutenessSettings.isEnabled():
            return ChatCommandResult.IGNORED

        arguments = await self.__parseArguments(
            chatMessage = chatMessage,
        )

        if arguments is None:
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to find cuteness info for the given user',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Unable to find target user ID ({arguments=}) ({chatMessage=})')
            return ChatCommandResult.CONSUMED

        if chatMessage.chatterUserId == arguments.chatterUserId:
            result = await self.__cutenessHelper.fetchCutenessLeaderboard(
                twitchChannelId = chatMessage.twitchChannelId,
                specificLookupUserId = arguments.chatterUserId,
            )

            printOut = await self.__cutenessPresenter.printLeaderboard(
                result = result,
            )

            self.__twitchChatMessenger.send(
                text = printOut,
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
        else:
            result = await self.__cutenessHelper.fetchCuteness(
                chatterUserId = chatMessage.chatterUserId,
                twitchChannelId = chatMessage.twitchChannelId,
            )

            printOut = await self.__cutenessPresenter.printCuteness(
                result = result,
            )

            self.__twitchChatMessenger.send(
                text = printOut,
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

        self.__timber.log('CutenessChatCommand', f'Consumed ({result=}) ({arguments=}) ({chatMessage=})')
        return ChatCommandResult.CONSUMED

    async def __parseArguments(self, chatMessage: TwitchChatMessage) -> Arguments | None:
        argumentsMatch = self.__argumentsPattern.match(chatMessage.text)
        if argumentsMatch is None:
            return CutenessChatCommand.Arguments(
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

        return CutenessChatCommand.Arguments(
            chatterUserId = chatterUserData.userId,
            chatterUserLogin = chatterUserData.userLogin,
            chatterUserName = chatterUserData.userName,
        )
