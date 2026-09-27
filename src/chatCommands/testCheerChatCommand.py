import re
import traceback
from dataclasses import dataclass
from typing import Collection, Final, Pattern

from .absChatCommand import AbsChatCommand
from .chatCommandResult import ChatCommandResult
from ..cheerActions.cheerActionHelperInterface import CheerActionHelperInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class TestCheerChatCommand(AbsChatCommand):

    @dataclass(frozen = True, slots = True)
    class Arguments:
        bits: int
        text: str

    def __init__(
        self,
        cheerActionHelper: CheerActionHelperInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(cheerActionHelper, CheerActionHelperInterface):
            raise TypeError(f'cheerActionHelper argument is malformed: \"{cheerActionHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__cheerActionHelper: Final[CheerActionHelperInterface] = cheerActionHelper
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!testcheer\b', re.IGNORECASE),
        })

        self.__argumentFormat: Final[Pattern] = re.compile(r'^\s*!\w+\s+(\d+)(?:\s+(.*))?$')
        self.__eventIdRegEx: Final[Pattern] = re.compile(r'[^a-z0-9]', re.IGNORECASE)

    @property
    def commandName(self) -> str:
        return 'TestCheerChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if chatMessage.twitchChannelId != chatMessage.chatterUserId:
            return ChatCommandResult.IGNORED

        arguments = await self.__parseArguments(chatMessage)
        if arguments is None:
            self.__twitchChatMessenger.send(
                text = f'⚠ Invalid arguments given. Example: !testcheer 100 Hello, World!',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Invalid arguments given ({arguments=}) ({chatMessage=})')
            return ChatCommandResult.CONSUMED

        handled: bool | None = None
        exception: Exception | None = None

        try:
            handled = await self.__cheerActionHelper.handleCheer(
                cheerInfo = CheerActionHelperInterface.CheerInfo(
                    bits = arguments.bits,
                    cheerUserId = chatMessage.chatterUserId,
                    cheerUserLogin = chatMessage.chatterUserLogin,
                    cheerUserName = chatMessage.chatterUserName,
                    message = arguments.text,
                    twitchChannelId = chatMessage.twitchChannelId,
                    twitchChatMessageId = chatMessage.twitchChatMessageId,
                    twitchUser = chatMessage.twitchUser,
                ),
            )
        except Exception as e:
            exception = e
            self.__timber.log(self.commandName, f'Encountered exception when attempting to run handleCheer() ({handled=}) ({exception=}) ({arguments=}) ({chatMessage=})', e, traceback.format_exc())

        self.__twitchChatMessenger.send(
            text = f'ⓘ Cheer test results ({handled=}) ({exception=}) ({arguments=})',
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Consumed ({handled=}) ({exception=}) ({arguments=}) ({chatMessage=})')
        return ChatCommandResult.CONSUMED

    async def __parseArguments(self, chatMessage: TwitchChatMessage) -> Arguments | None:
        argumentsMatch = self.__argumentFormat.fullmatch(chatMessage.text)
        if argumentsMatch is None:
            return None

        bits: int | None = None

        try:
            bits = int(argumentsMatch.group(1))
        except:
            pass

        if not utils.isValidInt(bits) or bits < 1 or bits > utils.getIntMaxSafeSize():
            return None

        text = utils.cleanStr(argumentsMatch.group(2))

        return TestCheerChatCommand.Arguments(
            bits = bits,
            text = text,
        )
