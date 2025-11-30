from typing import Final

from .absChatAction import AbsChatAction
from ..aniv.repositories.anivUserIdsRepositoryInterface import AnivUserIdsRepositoryInterface
from ..aniv.repositories.mostRecentAnivMessageRepositoryInterface import MostRecentAnivMessageRepositoryInterface
from ..misc import utils as utils
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchMessage import TwitchMessage
from ..users.userInterface import UserInterface


class SaveMostRecentAnivMessageChatAction(AbsChatAction):

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

    async def handleChat(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface,
    ) -> bool:
        whichAnivUser = await self.__anivUserIdsRepository.determineAnivUser(
            chatterUserId = message.getAuthorId(),
        )

        if whichAnivUser is None:
            return False

        cleanedMessage = utils.cleanStr(message.getContent())
        twitchChannelId = await message.getTwitchChannelId()

        await self.__mostRecentAnivMessageRepository.set(
            message = cleanedMessage,
            twitchChannelId = twitchChannelId,
            whichAnivUser = whichAnivUser,
        )

        self.__timber.log('SaveMostRecentAnivMessageChatAction', f'Updated most recent aniv message ({user=}) ({twitchChannelId=}) ({whichAnivUser=})')
        return True
