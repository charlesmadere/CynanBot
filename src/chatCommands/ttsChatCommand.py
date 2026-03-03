import random
import re
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..streamAlertsManager.streamAlert import StreamAlert
from ..streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ..timber.timberInterface import TimberInterface
from ..tts.jsonMapper.ttsJsonMapperInterface import TtsJsonMapperInterface
from ..tts.models.ttsEvent import TtsEvent
from ..tts.models.ttsProvider import TtsProvider
from ..tts.models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..users.userInterface import UserInterface


class TtsChatCommand(AbsChatCommand2):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        ttsJsonMapper: TtsJsonMapperInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsJsonMapper, TtsJsonMapperInterface):
            raise TypeError(f'ttsJsonMapper argument is malformed: \"{ttsJsonMapper}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__streamAlertsManager: Final[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: Final[TimberInterface] = timber
        self.__ttsJsonMapper: Final[TtsJsonMapperInterface] = ttsJsonMapper
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!tts', re.IGNORECASE),
        })

        self.__ttsProviderRegEx: Final[Pattern] = re.compile(r'^--(\w+)$', re.IGNORECASE)

    @property
    def commandName(self) -> str:
        return 'TtsChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def __displayTtsCheerAmounts(self, chatMessage: TwitchChatMessage):
        cheerAmountStrings = await self.__getTtsCheerAmountStrings(chatMessage.twitchUser)

        if len(cheerAmountStrings) == 0:
            self.__twitchChatMessenger.send(
                text = f'ⓘ TTS cheers have not been set up for this channel',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
        else:
            cheerAmountString = ', '.join(cheerAmountStrings)

            self.__twitchChatMessenger.send(
                text = f'ⓘ TTS cheer information — {cheerAmountString}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

    async def __getTtsCheerAmountStrings(self, user: UserInterface) -> list[str]:
        ttsBoosterPacks = user.ttsBoosterPacks
        strings: list[str] = list()

        if ttsBoosterPacks is None or len(ttsBoosterPacks) == 0:
            return strings

        for ttsBoosterPack in ttsBoosterPacks:
            if not ttsBoosterPack.isEnabled:
                continue

            bitsString: str

            if ttsBoosterPack.cheerAmount == 1:
                bitsString = 'bit'
            else:
                bitsString = 'bits'

            string = f'{ttsBoosterPack.cheerAmountStr} {bitsString} or more for {ttsBoosterPack.ttsProvider.humanName}'
            strings.append(string)

        return strings

    async def __getTtsProviderStrings(self) -> list[str]:
        strings: list[str] = list()

        for ttsProvider in TtsProvider:
            strings.append(await self.__ttsJsonMapper.asyncSerializeProvider(ttsProvider))

        strings.sort(key = lambda ttsProvider: ttsProvider.casefold())
        return strings

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isTtsEnabled:
            return ChatCommandResult.IGNORED

        administrator = await self.__administratorProvider.getAdministratorUserId()
        if chatMessage.twitchChannelId != chatMessage.chatterUserId and administrator != chatMessage.chatterUserId:
            await self.__displayTtsCheerAmounts(chatMessage)
            return ChatCommandResult.HANDLED

        splits = utils.getCleanedSplits(chatMessage.text)
        if len(splits) < 2:
            await self.__displayTtsCheerAmounts(chatMessage)
            return ChatCommandResult.HANDLED

        message = ' '.join(splits[1:])
        if not utils.isValidStr(message):
            await self.__displayTtsCheerAmounts(chatMessage)
            return ChatCommandResult.HANDLED

        ttsProvider = chatMessage.twitchUser.defaultTtsProvider
        ttsProviderMatch = self.__ttsProviderRegEx.fullmatch(message.split()[0])

        if ttsProviderMatch is not None and utils.isValidStr(ttsProviderMatch.group(1)) and len(splits) >= 3:
            try:
                ttsProvider = await self.__ttsJsonMapper.asyncRequireProvider(ttsProviderMatch.group(1))
                message = ' '.join(splits[2:])
            except ValueError:
                ttsProviderStrings = await self.__getTtsProviderStrings()
                ttsProviderString = ', '.join(ttsProviderStrings)

                self.__twitchChatMessenger.send(
                    text = f'⚠ TTS provider argument is malformed! Available TTS provider(s): {ttsProviderString}. Example: !tts --{random.choice(ttsProviderStrings)} Hello, World!',
                    twitchChannelId = chatMessage.twitchChannelId,
                    replyMessageId = chatMessage.twitchChatMessageId,
                )

                return ChatCommandResult.HANDLED

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = None,
            twitchChannel = chatMessage.twitchChannel,
            twitchChannelId = chatMessage.twitchChannelId,
            ttsEvent = TtsEvent(
                message = message,
                twitchChannel = chatMessage.twitchChannel,
                twitchChannelId = chatMessage.twitchChannelId,
                userId = chatMessage.chatterUserId,
                userName = chatMessage.chatterUserName,
                donation = None,
                provider = ttsProvider,
                providerOverridableStatus = TtsProviderOverridableStatus.THIS_EVENT_DISABLED,
                raidInfo = None,
            ),
        ))

        self.__twitchChatMessenger.send(
            text = f'ⓘ Submitted TTS message using {ttsProvider.humanName}…',
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Handled ({chatMessage=})')
        return ChatCommandResult.HANDLED
