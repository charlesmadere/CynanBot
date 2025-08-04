from typing import Final

from .absChatAction import AbsChatAction
from ..aniv.helpers.whichAnivUserHelperInterface import WhichAnivUserHelperInterface
from ..aniv.repositories.mostRecentAnivMessageRepositoryInterface import MostRecentAnivMessageRepositoryInterface
from ..misc import utils as utils
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..twitch.configuration.twitchMessage import TwitchMessage
from ..users.userInterface import UserInterface


class SaveMostRecentAnivMessageChatAction(AbsChatAction):

    def __init__(
        self,
        mostRecentAnivMessageRepository: MostRecentAnivMessageRepositoryInterface,
        whichAnivUserHelper: WhichAnivUserHelperInterface,
    ):
        if not isinstance(mostRecentAnivMessageRepository, MostRecentAnivMessageRepositoryInterface):
            raise TypeError(f'mostRecentAnivMessageRepository argument is malformed: \"{mostRecentAnivMessageRepository}\"')
        elif not isinstance(whichAnivUserHelper, WhichAnivUserHelperInterface):
            raise TypeError(f'whichAnivUserHelper argument is malformed: \"{whichAnivUserHelper}\"')

        self.__mostRecentAnivMessageRepository: Final[MostRecentAnivMessageRepositoryInterface] = mostRecentAnivMessageRepository
        self.__whichAnivUserHelper: Final[WhichAnivUserHelperInterface] = whichAnivUserHelper

    async def handleChat(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface,
    ) -> bool:
        anivUser = await self.__whichAnivUserHelper.getAnivUser(
            twitchChannelId = await message.getTwitchChannelId(),
            whichAnivUser = user.whichAnivUser,
        )

        if anivUser is None or anivUser.userId != message.getAuthorId():
            return False

        cleanedMessage = utils.cleanStr(message.getContent())

        await self.__mostRecentAnivMessageRepository.set(
            message = cleanedMessage,
            twitchChannelId = await message.getTwitchChannelId(),
            whichAnivUser = anivUser.whichAnivUser,
        )

        return True
