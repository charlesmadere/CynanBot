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
from CynanBot.chatActions.recurringActionsWizardChatAction import \
    RecurringActionsWizardChatAction
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
        recurringActionsWizardChatAction: Optional[RecurringActionsWizardChatAction],
        schubertWalkChatAction: Optional[SchubertWalkChatAction],
        supStreamerChatAction: Optional[SupStreamerChatAction],
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if anivCheckChatAction is not None and not isinstance(anivCheckChatAction, AnivCheckChatAction):
            raise TypeError(f'anivCheckChatAction argument is malformed: \"{anivCheckChatAction}\"')
        elif catJamChatAction is not None and not isinstance(catJamChatAction, CatJamChatAction):
            raise TypeError(f'catJamChatAction argument is malformed: \"{catJamChatAction}\"')
        elif chatLoggerChatAction is not None and not isinstance(chatLoggerChatAction, ChatLoggerChatAction):
            raise TypeError(f'chatLoggerChatAction argument is malformed: \"{chatLoggerChatAction}\"')
        elif deerForceChatAction is not None and not isinstance(deerForceChatAction, DeerForceChatAction):
            raise TypeError(f'deerForceChatAction argument is malformed: \"{deerForceChatAction}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(mostRecentChatsRepository, MostRecentChatsRepositoryInterface):
            raise TypeError(f'mostRecentChatsRepository argument is malformed: \"{mostRecentChatsRepository}\"')
        elif persistAllUsersChatAction is not None and not isinstance(persistAllUsersChatAction, PersistAllUsersChatAction):
            raise TypeError(f'persistAllUsersChatAction argument is malformed: \"{persistAllUsersChatAction}\"')
        elif recurringActionsWizardChatAction is not None and not isinstance(recurringActionsWizardChatAction, RecurringActionsWizardChatAction):
            raise TypeError(f'recurringActionsWizardChatAction argument is malformed: \"{recurringActionsWizardChatAction}\"')
        elif schubertWalkChatAction is not None and not isinstance(schubertWalkChatAction, SchubertWalkChatAction):
            raise TypeError(f'schubertWalkChatAction argument is malformed: \"{schubertWalkChatAction}\"')
        elif supStreamerChatAction is not None and not isinstance(supStreamerChatAction, SupStreamerChatAction):
            raise TypeError(f'supStreamerChatAction argument is malformed: \"{supStreamerChatAction}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__anivCheckChatAction: Optional[AbsChatAction] = anivCheckChatAction
        self.__catJamChatAction: Optional[AbsChatAction] = catJamChatAction
        self.__chatLoggerChatAction: Optional[AbsChatAction] = chatLoggerChatAction
        self.__deerForceChatAction: Optional[AbsChatAction] = deerForceChatAction
        self.__mostRecentChatsRepository: MostRecentChatsRepositoryInterface =  mostRecentChatsRepository
        self.__persistAllUsersChatAction: Optional[AbsChatAction] = persistAllUsersChatAction
        self.__recurringActionsWizardChatAction: Optional[AbsChatAction] = recurringActionsWizardChatAction
        self.__schubertWalkChatAction: Optional[AbsChatAction] = schubertWalkChatAction
        self.__supStreamerChatAction: Optional[AbsChatAction] = supStreamerChatAction
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleMessage(self, message: TwitchMessage):
        if not isinstance(message, TwitchMessage):
            raise TypeError(f'message argument is malformed: \"{message}\"')

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

        if self.__recurringActionsWizardChatAction is not None:
            await self.__recurringActionsWizardChatAction.handleChat(
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
        if mostRecentChat is not None and not isinstance(mostRecentChat, MostRecentChat):
            raise TypeError(f'mostRecentChat argument is malformed: \"{mostRecentChat}\"')
        elif not isinstance(message, TwitchMessage):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

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
