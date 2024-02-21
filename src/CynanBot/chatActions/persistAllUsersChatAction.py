from typing import Optional

from CynanBot.chatActions.absChatAction import AbsChatAction
from CynanBot.generalSettingsRepository import GeneralSettingsRepository
from CynanBot.mostRecentChat.mostRecentChat import MostRecentChat
from CynanBot.twitch.configuration.twitchMessage import TwitchMessage
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBot.users.userInterface import UserInterface


class PersistAllUsersChatAction(AbsChatAction):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(userIdsRepository, UserIdsRepositoryInterface), f"malformed {userIdsRepository=}"

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

    async def handleChat(
        self,
        mostRecentChat: Optional[MostRecentChat],
        message: TwitchMessage,
        user: UserInterface
    ) -> bool:
        settings = await self.__generalSettingsRepository.getAllAsync()

        if not settings.isPersistAllUsersEnabled():
            return False

        await self.__userIdsRepository.setUser(
            userId = message.getAuthorId(),
            userName = message.getAuthorName()
        )

        return True
