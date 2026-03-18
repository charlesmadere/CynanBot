from typing import Final

from .absChatAction2 import AbsChatAction2
from .chatActionResult import ChatActionResult
from ..aniv.repositories.anivUserIdsRepositoryInterface import AnivUserIdsRepositoryInterface
from ..aniv.repositories.mostRecentAnivMessageRepositoryInterface import MostRecentAnivMessageRepositoryInterface
from ..misc import utils as utils
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..timber.timberInterface import TimberInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class SaveMostRecentAnivMessageChatAction(AbsChatAction2):

    def __init__(
        self,
        anivUserIdsRepository: AnivUserIdsRepositoryInterface,
        mostRecentAnivMessageRepository: MostRecentAnivMessageRepositoryInterface,
        timber: TimberInterface,
    ):
        if not isinstance(anivUserIdsRepository, AnivUserIdsRepositoryInterface):
            raise TypeError(f'anivUserIdsRepository argument is malformed: \"{anivUserIdsRepository}\"')
        elif not isinstance(mostRecentAnivMessageRepository, MostRecentAnivMessageRepositoryInterface):
            raise TypeError(f'mostRecentAnivMessageRepository argument is malformed: \"{mostRecentAnivMessageRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__anivUserIdsRepository: Final[AnivUserIdsRepositoryInterface] = anivUserIdsRepository
        self.__mostRecentAnivMessageRepository: Final[MostRecentAnivMessageRepositoryInterface] = mostRecentAnivMessageRepository
        self.__timber: Final[TimberInterface] = timber

    @property
    def actionName(self) -> str:
        return 'SaveMostRecentAnivMessageChatAction'

    async def handleChatAction(
        self,
        mostRecentChat: MostRecentChat | None,
        chatMessage: TwitchChatMessage,
    ) -> ChatActionResult:
        whichAnivUser = await self.__anivUserIdsRepository.determineAnivUser(
            chatterUserId = chatMessage.chatterUserId,
        )

        if whichAnivUser is None:
            return ChatActionResult.IGNORED

        cleanedMessage = utils.cleanStr(chatMessage.text)

        await self.__mostRecentAnivMessageRepository.set(
            message = cleanedMessage,
            twitchChannelId = chatMessage.twitchChannelId,
            whichAnivUser = whichAnivUser,
        )

        self.__timber.log(self.actionName, f'Updated most recent aniv message ({chatMessage=}) ({whichAnivUser=})')
        return ChatActionResult.HANDLED
