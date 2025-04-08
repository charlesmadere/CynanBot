from .chatActionsManagerInterface import ChatActionsManagerInterface
from ..absChatAction import AbsChatAction
from ..anivCheckChatAction import AnivCheckChatAction
from ..chatBackMessagesChatAction import ChatBackMessagesChatAction
from ..chatLoggerChatAction import ChatLoggerChatAction
from ..cheerActionsWizardChatAction import CheerActionsWizardChatAction
from ..persistAllUsersChatAction import PersistAllUsersChatAction
from ..recurringActionsWizardChatAction import RecurringActionsWizardChatAction
from ..saveMostRecentAnivMessageChatAction import SaveMostRecentAnivMessageChatAction
from ..soundAlertChatAction import SoundAlertChatAction
from ..supStreamerChatAction import SupStreamerChatAction
from ..ttsChatterChatAction import TtsChatterChatAction
from ...aniv.helpers.mostRecentAnivMessageTimeoutHelperInterface import MostRecentAnivMessageTimeoutHelperInterface
from ...misc.generalSettingsRepository import GeneralSettingsRepository
from ...mostRecentChat.mostRecentChat import MostRecentChat
from ...mostRecentChat.mostRecentChatsRepositoryInterface import MostRecentChatsRepositoryInterface
from ...twitch.activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from ...twitch.configuration.twitchMessage import TwitchMessage
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ...users.userInterface import UserInterface
from ...users.usersRepositoryInterface import UsersRepositoryInterface


class ChatActionsManager(ChatActionsManagerInterface):

    def __init__(
        self,
        activeChattersRepository: ActiveChattersRepositoryInterface,
        anivCheckChatAction: AnivCheckChatAction | None,
        chatBackMessagesChatAction: ChatBackMessagesChatAction | None,
        chatLoggerChatAction: ChatLoggerChatAction | None,
        cheerActionsWizardChatAction: CheerActionsWizardChatAction | None,
        generalSettingsRepository: GeneralSettingsRepository,
        mostRecentAnivMessageTimeoutHelper: MostRecentAnivMessageTimeoutHelperInterface | None,
        mostRecentChatsRepository: MostRecentChatsRepositoryInterface,
        persistAllUsersChatAction: PersistAllUsersChatAction | None,
        recurringActionsWizardChatAction: RecurringActionsWizardChatAction | None,
        saveMostRecentAnivMessageChatAction: SaveMostRecentAnivMessageChatAction | None,
        soundAlertChatAction: SoundAlertChatAction | None,
        supStreamerChatAction: SupStreamerChatAction | None,
        ttsChatterChatAction: TtsChatterChatAction | None,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(activeChattersRepository, ActiveChattersRepositoryInterface):
            raise TypeError(f'activeChattersRepository argument is malformed: \"{activeChattersRepository}\"')
        elif anivCheckChatAction is not None and not isinstance(anivCheckChatAction, AnivCheckChatAction):
            raise TypeError(f'anivCheckChatAction argument is malformed: \"{anivCheckChatAction}\"')
        elif chatBackMessagesChatAction is not None and not isinstance(chatBackMessagesChatAction, ChatBackMessagesChatAction):
            raise TypeError(f'chatBackMessagesChatAction argument is malformed: \"{chatBackMessagesChatAction}\"')
        elif chatLoggerChatAction is not None and not isinstance(chatLoggerChatAction, ChatLoggerChatAction):
            raise TypeError(f'chatLoggerChatAction argument is malformed: \"{chatLoggerChatAction}\"')
        elif cheerActionsWizardChatAction is not None and not isinstance(cheerActionsWizardChatAction, CheerActionsWizardChatAction):
            raise TypeError(f'cheerActionsWizardChatAction argument is malformed: \"{cheerActionsWizardChatAction}\"')
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
        elif soundAlertChatAction is not None and not isinstance(soundAlertChatAction, SoundAlertChatAction):
            raise TypeError(f'soundAlertChatAction argument is malformed: \"{soundAlertChatAction}\"')
        elif supStreamerChatAction is not None and not isinstance(supStreamerChatAction, SupStreamerChatAction):
            raise TypeError(f'supStreamerChatAction argument is malformed: \"{supStreamerChatAction}\"')
        elif ttsChatterChatAction is not None and not isinstance(ttsChatterChatAction, TtsChatterChatAction):
            raise TypeError(f'ttsChatterChatAction argument is malformed: \"{ttsChatterChatAction}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__activeChattersRepository: ActiveChattersRepositoryInterface = activeChattersRepository
        self.__anivCheckChatAction: AbsChatAction | None = anivCheckChatAction
        self.__chatBackMessagesChatAction: AbsChatAction | None = chatBackMessagesChatAction
        self.__chatLoggerChatAction: AbsChatAction | None = chatLoggerChatAction
        self.__cheerActionsWizardChatAction: CheerActionsWizardChatAction | None = cheerActionsWizardChatAction
        self.__mostRecentAnivMessageTimeoutHelper: MostRecentAnivMessageTimeoutHelperInterface | None = mostRecentAnivMessageTimeoutHelper
        self.__mostRecentChatsRepository: MostRecentChatsRepositoryInterface =  mostRecentChatsRepository
        self.__persistAllUsersChatAction: AbsChatAction | None = persistAllUsersChatAction
        self.__recurringActionsWizardChatAction: AbsChatAction | None = recurringActionsWizardChatAction
        self.__saveMostRecentAnivMessageChatAction: AbsChatAction | None = saveMostRecentAnivMessageChatAction
        self.__soundAlertChatAction: AbsChatAction | None = soundAlertChatAction
        self.__supStreamerChatAction: AbsChatAction | None = supStreamerChatAction
        self.__ttsChatterChatAction: AbsChatAction | None = ttsChatterChatAction
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__soundAlertChatActionPlayed: bool = False

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

        await self.__activeChattersRepository.add(
            chatterUserId = message.getAuthorId(),
            chatterUserName = message.getAuthorName(),
            twitchChannelId = await message.getTwitchChannelId()
        )

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

        if self.__chatBackMessagesChatAction is not None:
            await self.__chatBackMessagesChatAction.handleChat(
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

        if self.__cheerActionsWizardChatAction is not None:
            await self.__cheerActionsWizardChatAction.handleChat(
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

        if self.__soundAlertChatAction is not None:
            self.__soundAlertChatActionPlayed = await self.__soundAlertChatAction.handleChat(
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

        if self.__ttsChatterChatAction is not None:
            if not self.__soundAlertChatActionPlayed:
                await self.__ttsChatterChatAction.handleChat(
                    mostRecentChat = mostRecentChat,
                    message = message,
                    user = user
                )
