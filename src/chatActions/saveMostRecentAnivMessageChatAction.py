from .absChatAction import AbsChatAction
from ..aniv.anivUserIdProviderInterface import AnivUserIdProviderInterface
from ..aniv.mostRecentAnivMessageRepositoryInterface import \
    MostRecentAnivMessageRepositoryInterface
from ..misc import utils as utils
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..twitch.configuration.twitchMessage import TwitchMessage
from ..users.userInterface import UserInterface


class SaveMostRecentAnivMessageChatAction(AbsChatAction):

    def __init__(
        self,
        anivUserIdProvider: AnivUserIdProviderInterface,
        mostRecentAnivMessageRepository: MostRecentAnivMessageRepositoryInterface
    ):
        if not isinstance(anivUserIdProvider, AnivUserIdProviderInterface):
            raise TypeError(f'anivUserIdProvider argument is malformed: \"{anivUserIdProvider}\"')
        elif not isinstance(mostRecentAnivMessageRepository, MostRecentAnivMessageRepositoryInterface):
            raise TypeError(f'mostRecentAnivMessageRepository argument is malformed: \"{mostRecentAnivMessageRepository}\"')

        self.__anivUserIdProvider: AnivUserIdProviderInterface = anivUserIdProvider
        self.__mostRecentAnivMessageRepository: MostRecentAnivMessageRepositoryInterface = mostRecentAnivMessageRepository

    async def handleChat(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface
    ) -> bool:
        anivUserId = await self.__anivUserIdProvider.getAnivUserId()

        if not utils.isValidStr(anivUserId) or anivUserId != message.getAuthorId():
            return False

        await self.__mostRecentAnivMessageRepository.set(
            message = message.getContent(),
            twitchChannelId = await message.getTwitchChannelId()
        )

        return True
