import re
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..chatterPreferredName.repositories.chatterPreferredNameRepositoryInterface import \
    ChatterPreferredNameRepositoryInterface
from ..chatterPreferredName.settings.chatterPreferredNameSettingsInterface import ChatterPreferredNameSettingsInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class RemoveChatterPreferredNameChatCommand(AbsChatCommand2):

    def __init__(
        self,
        chatterPreferredNameRepository: ChatterPreferredNameRepositoryInterface,
        chatterPreferredNameSettings: ChatterPreferredNameSettingsInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(chatterPreferredNameRepository, ChatterPreferredNameRepositoryInterface):
            raise TypeError(f'chatterPreferredNameRepository argument is malformed: \"{chatterPreferredNameRepository}\"')
        elif not isinstance(chatterPreferredNameSettings, ChatterPreferredNameSettingsInterface):
            raise TypeError(f'chatterPreferredNameSettings argument is malformed: \"{chatterPreferredNameSettings}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__chatterPreferredNameRepository: Final[ChatterPreferredNameRepositoryInterface] = chatterPreferredNameRepository
        self.__chatterPreferredNameSettings: Final[ChatterPreferredNameSettingsInterface] = chatterPreferredNameSettings
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!del(?:lete)?(?:my)?(?:chatter)?preferredname\b', re.IGNORECASE),
            re.compile(r'^\s*!remove(?:my)?(?:chatter)?preferredname\b', re.IGNORECASE),
            re.compile(r'^\s*!rm(?:my)?(?:chatter)?preferredname\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'RemoveChatterPreferredNameChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isChatterPreferredNameEnabled:
            return ChatCommandResult.IGNORED
        elif not await self.__chatterPreferredNameSettings.isEnabled():
            return ChatCommandResult.IGNORED

        preferredNameData = await self.__chatterPreferredNameRepository.remove(
            chatterUserId = chatMessage.chatterUserId,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        if preferredNameData is None:
            self.__twitchChatMessenger.send(
                text = f'ⓘ You don\'t currently have a preferred name to delete',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
        else:
            self.__twitchChatMessenger.send(
                text = f'ⓘ Your preferred name was deleted, it previously was: {preferredNameData.preferredName}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

        self.__timber.log(self.commandName, f'Handled ({preferredNameData=}) ({chatMessage})')
        return ChatCommandResult.HANDLED
