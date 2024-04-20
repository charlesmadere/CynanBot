from CynanBot.aniv.mostRecentAnivMessageTimeoutHelperInterface import \
    MostRecentAnivMessageTimeoutHelperInterface
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
from CynanBot.chatActions.saveMostRecentAnivMessageChatAction import \
    SaveMostRecentAnivMessageChatAction
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
        anivCheckChatAction: AnivCheckChatAction | None,
        catJamChatAction: CatJamChatAction | None,
        chatLoggerChatAction: ChatLoggerChatAction | None,
        deerForceChatAction: DeerForceChatAction | None,
        generalSettingsRepository: GeneralSettingsRepository,
        mostRecentAnivMessageTimeoutHelper: MostRecentAnivMessageTimeoutHelperInterface | None,
        mostRecentChatsRepository: MostRecentChatsRepositoryInterface,
        persistAllUsersChatAction: PersistAllUsersChatAction | None,
        recurringActionsWizardChatAction: RecurringActionsWizardChatAction | None,
        saveMostRecentAnivMessageChatAction: SaveMostRecentAnivMessageChatAction | None,
        schubertWalkChatAction: SchubertWalkChatAction | None,
        supStreamerChatAction: SupStreamerChatAction | None,
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
        elif mostRecentAnivMessageTimeoutHelper is not None and not isinstance(mostRecentAnivMessageTimeoutHelper, MostRecentAnivMessageTimeoutHelperInterface):
            raise TypeError(f'mostRecentAnivMessageTimeoutHelper argument is malformed: \"{mostRecentAnivMessageTimeoutHelper}\"')
        elif not isinstance(mostRecentChatsRepository, MostRecentChatsRepositoryInterface):
            raise TypeError(f'mostRecentChatsRepository argument is malformed: \"{mostRecentChatsRepository}\"')
        elif persistAllUsersChatAction is not None and not isinstance(persistAllUsersChatAction, PersistAllUsersChatAction):
            raise TypeError(f'persistAllUsersChatAction argument is malformed: \"{persistAllUsersChatAction}\"')
        elif recurringActionsWizardChatAction is not None and not isinstance(recurringActionsWizardChatAction, RecurringActionsWizardChatAction):
            raise TypeError(f'recurringActionsWizardChatAction argument is malformed: \"{recurringActionsWizardChatAction}\"')
        elif saveMostRecentAnivMessageChatAction is not None and not isinstance(saveMostRecentAnivMessageChatAction, SaveMostRecentAnivMessageChatAction):
            raise TypeError(f'saveMostRecentAnivMessageChatAction argument is malformed: \"{saveMostRecentAnivMessageChatAction}\"')
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

        self.__anivCheckChatAction: AbsChatAction | None = anivCheckChatAction
        self.__catJamChatAction: AbsChatAction | None = catJamChatAction
        self.__chatLoggerChatAction: AbsChatAction | None = chatLoggerChatAction
        self.__deerForceChatAction: AbsChatAction | None = deerForceChatAction
        self.__mostRecentAnivMessageTimeoutHelper: MostRecentAnivMessageTimeoutHelperInterface | None = mostRecentAnivMessageTimeoutHelper
        self.__mostRecentChatsRepository: MostRecentChatsRepositoryInterface =  mostRecentChatsRepository
        self.__persistAllUsersChatAction: AbsChatAction | None = persistAllUsersChatAction
        self.__recurringActionsWizardChatAction: AbsChatAction | None = recurringActionsWizardChatAction
        self.__saveMostRecentAnivMessageChatAction: AbsChatAction | None = saveMostRecentAnivMessageChatAction
        self.__schubertWalkChatAction: AbsChatAction | None = schubertWalkChatAction
        self.__supStreamerChatAction: AbsChatAction | None = supStreamerChatAction
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def __handleAnivChatActions(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface
    ):
        if mostRecentChat is not None and not isinstance(mostRecentChat, MostRecentChat):
            raise TypeError(f'mostRecentChat argument is malformed: \"{mostRecentChat}\"')
        elif not isinstance(message, TwitchMessage):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        if self.__saveMostRecentAnivMessageChatAction is not None:
            await self.__saveMostRecentAnivMessageChatAction.handleChat(
                mostRecentChat = mostRecentChat,
                message = message,
                user = user
            )

            if self.__mostRecentAnivMessageTimeoutHelper is not None:
                await self.__mostRecentAnivMessageTimeoutHelper.checkMessageAndMaybeTimeout(
                    chatterMessage = message.getContent(),
                    chatterUserId = message.getAuthorId(),
                    chatterUserName = message.getAuthorName(),
                    twitchChannelId = await message.getTwitchChannelId(),
                    user = user
                )

        if self.__anivCheckChatAction is not None:
            await self.__anivCheckChatAction.handleChat(
                mostRecentChat = mostRecentChat,
                message = message,
                user = user
            )

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

        await self.__handleAnivChatActions(
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
        mostRecentChat: MostRecentChat | None,
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
