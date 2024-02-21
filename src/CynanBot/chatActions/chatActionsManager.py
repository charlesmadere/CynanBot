from typing import Optional

from CynanBot.chatActions.absChatAction import AbsChatAction
from CynanBot.chatActions.anivCheckChatAction import AnivCheckChatAction
from CynanBot.chatActions.catJamChatAction import CatJamChatAction
from CynanBot.chatActions.chatActionsManagerInterface import \
    ChatActionsManagerInterface
from CynanBot.chatActions.chatLoggerChatAction import ChatLoggerChatAction
from CynanBot.chatActions.deerForceChatAction import DeerForceChatAction
from CynanBot.chatActions.persistAllUsersChatAction import \
    PersistAllUsersChatAction
from CynanBot.chatActions.schubertWalkChatAction import SchubertWalkChatAction
from CynanBot.chatActions.supStreamerChatAction import SupStreamerChatAction
from CynanBot.generalSettingsRepository import GeneralSettingsRepository
from CynanBot.mostRecentChat.mostRecentChat import MostRecentChat
from CynanBot.mostRecentChat.mostRecentChatsRepositoryInterface import \
    MostRecentChatsRepositoryInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.configuration.twitchMessage import TwitchMessage
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBot.users.userInterface import UserInterface
from CynanBot.users.usersRepositoryInterface import UsersRepositoryInterface


class ChatActionsManager(ChatActionsManagerInterface):

    def __init__(
        self,
        anivCheckChatAction: Optional[AnivCheckChatAction],
        catJamChatAction: Optional[CatJamChatAction],
        chatLoggerChatAction: Optional[ChatLoggerChatAction],
        deerForceChatAction: Optional[DeerForceChatAction],
        generalSettingsRepository: GeneralSettingsRepository,
        mostRecentChatsRepository: MostRecentChatsRepositoryInterface,
        persistAllUsersChatAction: Optional[PersistAllUsersChatAction],
        schubertWalkChatAction: Optional[SchubertWalkChatAction],
        supStreamerChatAction: Optional[SupStreamerChatAction],
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        assert anivCheckChatAction is None or isinstance(anivCheckChatAction, AnivCheckChatAction), f"malformed {anivCheckChatAction=}"
        assert catJamChatAction is None or isinstance(catJamChatAction, CatJamChatAction), f"malformed {catJamChatAction=}"
        assert chatLoggerChatAction is None or isinstance(chatLoggerChatAction, ChatLoggerChatAction), f"malformed {chatLoggerChatAction=}"
        assert deerForceChatAction is None or isinstance(deerForceChatAction, DeerForceChatAction), f"malformed {deerForceChatAction=}"
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(mostRecentChatsRepository, MostRecentChatsRepositoryInterface), f"malformed {mostRecentChatsRepository=}"
        assert persistAllUsersChatAction is None or isinstance(persistAllUsersChatAction, PersistAllUsersChatAction), f"malformed {persistAllUsersChatAction=}"
        assert schubertWalkChatAction is None or isinstance(schubertWalkChatAction, SchubertWalkChatAction), f"malformed {schubertWalkChatAction=}"
        assert supStreamerChatAction is None or isinstance(supStreamerChatAction, SupStreamerChatAction), f"malformed {supStreamerChatAction=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(userIdsRepository, UserIdsRepositoryInterface), f"malformed {userIdsRepository=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

        self.__anivCheckChatAction: Optional[AbsChatAction] = anivCheckChatAction
        self.__catJamChatAction: Optional[AbsChatAction] = catJamChatAction
        self.__chatLoggerChatAction: Optional[AbsChatAction] = chatLoggerChatAction
        self.__deerForceChatAction: Optional[AbsChatAction] = deerForceChatAction
        self.__mostRecentChatsRepository: MostRecentChatsRepositoryInterface =  mostRecentChatsRepository
        self.__persistAllUsersChatAction: Optional[AbsChatAction] = persistAllUsersChatAction
        self.__schubertWalkChatAction: Optional[AbsChatAction] = schubertWalkChatAction
        self.__supStreamerChatAction: Optional[AbsChatAction] = supStreamerChatAction
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleMessage(self, message: TwitchMessage):
        assert isinstance(message, TwitchMessage), f"malformed {message=}"

        mostRecentChat = await self.__mostRecentChatsRepository.get(
            chatterUserId = message.getAuthorId(),
            twitchChannelId = await message.getTwitchChannelId()
        )

        await self.__mostRecentChatsRepository.set(
            chatterUserId = message.getAuthorId(),
            twitchChannelId = await message.getTwitchChannelId()
        )

        user = await self.__usersRepository.getUserAsync(message.getTwitchChannelName())

        if self.__anivCheckChatAction is not None:
            await self.__anivCheckChatAction.handleChat(
                mostRecentChat = mostRecentChat,
                message = message,
                user = user
            )

        if self.__chatLoggerChatAction is not None:
            await self.__chatLoggerChatAction.handleChat(
                mostRecentChat = mostRecentChat,
                message = message,
                user = user
            )

        if self.__persistAllUsersChatAction is not None:
            await self.__persistAllUsersChatAction.handleChat(
                mostRecentChat = mostRecentChat,
                message = message,
                user = user
            )

        if self.__supStreamerChatAction is not None:
            await self.__supStreamerChatAction.handleChat(
                mostRecentChat = mostRecentChat,
                message = message,
                user = user
            )

        await self.__handleSimpleMessageChatActions(
            mostRecentChat = mostRecentChat,
            message = message,
            user = user
        )

        await self.__handleSimpleMessageChatActions(
            mostRecentChat = mostRecentChat,
            message = message,
            user = user
        )

    async def __handleSimpleMessageChatActions(
        self,
        mostRecentChat: Optional[MostRecentChat],
        message: TwitchMessage,
        user: UserInterface
    ):
        assert mostRecentChat is None or isinstance(mostRecentChat, MostRecentChat), f"malformed {mostRecentChat=}"
        assert isinstance(message, TwitchMessage), f"malformed {message=}"
        assert isinstance(user, UserInterface), f"malformed {user=}"

        if self.__catJamChatAction is not None and await self.__catJamChatAction.handleChat(
            mostRecentChat = mostRecentChat,
            message = message,
            user = user
        ):
            return

        if self.__deerForceChatAction is not None and not await self.__deerForceChatAction.handleChat(
            mostRecentChat = mostRecentChat,
            message = message,
            user = user
        ):
            return

        if self.__schubertWalkChatAction is not None and await self.__schubertWalkChatAction.handleChat(
            mostRecentChat = mostRecentChat,
            message = message,
            user = user
        ):
            return
