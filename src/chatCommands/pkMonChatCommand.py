import re
import traceback
from typing import Collection, Final, Pattern

from .absChatCommand import AbsChatCommand
from .chatCommandResult import ChatCommandResult
from ..misc import utils as utils
from ..pkmn.pokepediaRepositoryInterface import PokepediaRepositoryInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class PkMonChatCommand(AbsChatCommand):

    def __init__(
        self,
        pokepediaRepository: PokepediaRepositoryInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(pokepediaRepository, PokepediaRepositoryInterface):
            raise TypeError(f'pokepediaRepository argument is malformed: \"{pokepediaRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__pokepediaRepository: Final[PokepediaRepositoryInterface] = pokepediaRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!pkmon\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'PkMonChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isPokepediaEnabled:
            return ChatCommandResult.IGNORED

        splits = utils.getCleanedSplits(chatMessage.text)
        if len(splits) < 2:
            self.__twitchChatMessenger.send(
                text = '⚠ A Pokémon name is necessary for the !pkmon command. Example: !pkmon charizard',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
            return ChatCommandResult.CONSUMED

        name = splits[1]

        try:
            mon = await self.__pokepediaRepository.searchPokemon(
                name = name,
            )

            for string in mon.toStrList():
                self.__twitchChatMessenger.send(
                    text = string,
                    twitchChannelId = chatMessage.twitchChannelId,
                    replyMessageId = chatMessage.twitchChatMessageId,
                )
        except Exception as e:
            self.__timber.log(self.commandName, f'Error searching for Pokemon ({name=})', e, traceback.format_exc())
            self.__twitchChatMessenger.send(
                text = f'⚠ Error searching Pokémon: \"{name}\"',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

        self.__timber.log(self.commandName, f'Handled ({name=}) ({chatMessage=})')
        return ChatCommandResult.CONSUMED
