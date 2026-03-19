import re
import traceback
import uuid
from dataclasses import dataclass
from typing import Collection, Final, Pattern

from frozenlist import FrozenList

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.absTwitchChatHandler import AbsTwitchChatHandler
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..twitch.localModels.twitchChatMessageFragment import TwitchChatMessageFragment
from ..twitch.localModels.twitchChatMessageFragmentType import TwitchChatMessageFragmentType
from ..twitch.localModels.twitchCheerMetadata import TwitchCheerMetadata


class TestCheerChatCommand(AbsChatCommand2):

    @dataclass(frozen = True, slots = True)
    class Arguments:
        bits: int
        text: str

        @property
        def fullText(self) -> str:
            return 'cheer' + str(self.bits) + ' ' + self.text

    def __init__(
        self,
        twitchChatHandler: AbsTwitchChatHandler,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(twitchChatHandler, AbsTwitchChatHandler):
            raise TypeError(f'twitchChatHandler argument is malformed: \"{twitchChatHandler}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__twitchChatHandler: Final[AbsTwitchChatHandler] = twitchChatHandler
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

    async def __generateEventId(self) -> str:
        eventId = str(uuid.uuid4())
        return self.__eventIdRegEx.sub('', eventId)

    async def __generateMessageFragments(self, arguments: Arguments) -> FrozenList[TwitchChatMessageFragment]:
        messageFragments: FrozenList[TwitchChatMessageFragment] = FrozenList()

        messageFragments.append(TwitchChatMessageFragment(
            text = 'cheer' + str(arguments.bits),
            cheermote = None,
            emote = None,
            mention = None,
            fragmentType = TwitchChatMessageFragmentType.CHEERMOTE,
        ))

        if utils.isValidStr(arguments.text):
            messageFragments.append(TwitchChatMessageFragment(
                text = arguments.text,
                cheermote = None,
                emote = None,
                mention = None,
                fragmentType = TwitchChatMessageFragmentType.TEXT,
            ))

        messageFragments.freeze()
        return messageFragments

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
            return ChatCommandResult.HANDLED

        newTwitchChatMessage = TwitchChatMessage(
            messageFragments = await self.__generateMessageFragments(arguments),
            chatterUserId = chatMessage.chatterUserId,
            chatterUserLogin = chatMessage.chatterUserLogin,
            chatterUserName = chatMessage.chatterUserName,
            eventId = await self.__generateEventId(),
            sourceMessageId = None,
            text = arguments.fullText,
            twitchChannelId = chatMessage.twitchChannelId,
            twitchChatMessageId = None,
            cheerMetadata = TwitchCheerMetadata(
                bits = arguments.bits,
            ),
            twitchUser = chatMessage.twitchUser,
        )

        exception: Exception | None = None

        try:
            await self.__twitchChatHandler.onNewChat(
                chatMessage = newTwitchChatMessage,
            )
        except Exception as e:
            exception = e
            self.__timber.log(self.commandName, f'Encountered exception when attempting to run onNewChat() ({arguments=}) ({newTwitchChatMessage=}) ({chatMessage=})', e, traceback.format_exc())

        self.__twitchChatMessenger.send(
            text = f'ⓘ Cheer test results ({arguments=}) ({exception=})',
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Handled ({arguments=}) ({newTwitchChatMessage=}) ({chatMessage=}) ({exception=})')
        return ChatCommandResult.HANDLED

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

        text = ' '.join(utils.getCleanedSplits(argumentsMatch.group(2)))

        return TestCheerChatCommand.Arguments(
            bits = bits,
            text = text,
        )
