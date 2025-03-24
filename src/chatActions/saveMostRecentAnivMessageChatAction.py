from .absChatAction import AbsChatAction
from ..aniv.mostRecentAnivMessageRepositoryInterface import \
    MostRecentAnivMessageRepositoryInterface
from ..aniv.whichAnivUserHelperInterface import WhichAnivUserHelperInterface
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..twitch.configuration.twitchMessage import TwitchMessage
from ..twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface
from ..users.userInterface import UserInterface


class SaveMostRecentAnivMessageChatAction(AbsChatAction):

    def __init__(
        self,
        mostRecentAnivMessageRepository: MostRecentAnivMessageRepositoryInterface,
        whichAnivUserHelper: WhichAnivUserHelperInterface
    ):
        if not isinstance(mostRecentAnivMessageRepository, MostRecentAnivMessageRepositoryInterface):
            raise TypeError(f'mostRecentAnivMessageRepository argument is malformed: \"{mostRecentAnivMessageRepository}\"')
        elif not isinstance(whichAnivUserHelper, TwitchFriendsUserIdRepositoryInterface):
            raise TypeError(f'whichAnivUserHelper argument is malformed: \"{whichAnivUserHelper}\"')

        self.__mostRecentAnivMessageRepository: MostRecentAnivMessageRepositoryInterface = mostRecentAnivMessageRepository
        self.__whichAnivUserHelper: WhichAnivUserHelperInterface = whichAnivUserHelper

    async def handleChat(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface
    ) -> bool:
        anivUser = await self.__whichAnivUserHelper.getAnivUser(user.whichAnivUser)

        if anivUser is None or anivUser.userId != message.getAuthorId():
            return False

        await self.__mostRecentAnivMessageRepository.set(
            message = message.getContent(),
            twitchChannelId = await message.getTwitchChannelId()
        )

        return True
