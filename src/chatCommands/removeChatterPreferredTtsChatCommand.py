import re
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..chatterPreferredTts.chatterPreferredTtsPresenter import ChatterPreferredTtsPresenter
from ..chatterPreferredTts.repository.chatterPreferredTtsRepositoryInterface import \
    ChatterPreferredTtsRepositoryInterface
from ..chatterPreferredTts.settings.chatterPreferredTtsSettingsRepositoryInterface import \
    ChatterPreferredTtsSettingsRepositoryInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class RemoveChatterPreferredTtsChatCommand(AbsChatCommand2):

    def __init__(
        self,
        chatterPreferredTtsPresenter: ChatterPreferredTtsPresenter,
        chatterPreferredTtsRepository: ChatterPreferredTtsRepositoryInterface,
        chatterPreferredTtsSettingsRepository: ChatterPreferredTtsSettingsRepositoryInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(chatterPreferredTtsPresenter, ChatterPreferredTtsPresenter):
            raise TypeError(f'chatterPreferredTtsPresenter argument is malformed: \"{chatterPreferredTtsPresenter}\"')
        elif not isinstance(chatterPreferredTtsRepository, ChatterPreferredTtsRepositoryInterface):
            raise TypeError(f'chatterPreferredTtsRepository argument is malformed: \"{chatterPreferredTtsRepository}\"')
        elif not isinstance(chatterPreferredTtsSettingsRepository, ChatterPreferredTtsSettingsRepositoryInterface):
            raise TypeError(f'chatterPreferredTtsSettingsRepository argument is malformed: \"{chatterPreferredTtsSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__chatterPreferredTtsPresenter: Final[ChatterPreferredTtsPresenter] = chatterPreferredTtsPresenter
        self.__chatterPreferredTtsRepository: Final[ChatterPreferredTtsRepositoryInterface] = chatterPreferredTtsRepository
        self.__chatterPreferredTtsSettingsRepository: Final[ChatterPreferredTtsSettingsRepositoryInterface] = chatterPreferredTtsSettingsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!del(?:lete)?(?:my)?(?:chatter)?preferredtts\b', re.IGNORECASE),
            re.compile(r'^\s*remove(?:my)?(?:chatter)?preferredtts\b', re.IGNORECASE),
            re.compile(r'^\s*rm(?:my)?(?:chatter)?preferredtts\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'RemoveChatterPreferredTtsChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isChatterPreferredTtsEnabled:
            return ChatCommandResult.IGNORED
        elif not await self.__chatterPreferredTtsSettingsRepository.isEnabled():
            return ChatCommandResult.IGNORED

        preferredTts = await self.__chatterPreferredTtsRepository.remove(
            chatterUserId = chatMessage.chatterUserId,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        if preferredTts is None:
            self.__twitchChatMessenger.send(
                text = f'ⓘ You don\'t currently have a preferred TTS to delete',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
        else:
            printOut = await self.__chatterPreferredTtsPresenter.printOut(
                preferredTts = preferredTts,
            )

            self.__twitchChatMessenger.send(
                text = f'ⓘ Your preferred TTS was deleted, it previously was: {printOut}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

        self.__timber.log(self.commandName, f'Handled ({preferredTts=}) ({chatMessage=})')
        return ChatCommandResult.HANDLED
