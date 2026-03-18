from typing import Any, Collection, Final

from .chatActionsManagerInterface import ChatActionsManagerInterface
from ..absChatAction import AbsChatAction
from ..absChatAction2 import AbsChatAction2
from ..chatBackMessagesChatAction import ChatBackMessagesChatAction
from ..cheerActionsWizardChatAction import CheerActionsWizardChatAction
from ..recurringActionsWizardChatAction import RecurringActionsWizardChatAction
from ..voicemailChatAction import VoicemailChatAction
from ...misc.generalSettingsRepository import GeneralSettingsRepository
from ...mostRecentChat.mostRecentChatsRepositoryInterface import MostRecentChatsRepositoryInterface
from ...timber.timberInterface import TimberInterface
from ...twitch.activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from ...twitch.configuration.twitchMessage import TwitchMessage
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ...users.usersRepositoryInterface import UsersRepositoryInterface


class ChatActionsManager(ChatActionsManagerInterface):

    def __init__(
        self,
        activeChattersRepository: ActiveChattersRepositoryInterface,
        chatBackMessagesChatAction: ChatBackMessagesChatAction | None,
        cheerActionsWizardChatAction: CheerActionsWizardChatAction | None,
        chatActions: Collection[AbsChatAction2 | Any | None] | None,
        generalSettingsRepository: GeneralSettingsRepository,
        mostRecentChatsRepository: MostRecentChatsRepositoryInterface,
        recurringActionsWizardChatAction: RecurringActionsWizardChatAction | None,
        timber: TimberInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
        voicemailChatAction: VoicemailChatAction | None,
    ):
        if not isinstance(activeChattersRepository, ActiveChattersRepositoryInterface):
            raise TypeError(f'activeChattersRepository argument is malformed: \"{activeChattersRepository}\"')
        elif chatBackMessagesChatAction is not None and not isinstance(chatBackMessagesChatAction, ChatBackMessagesChatAction):
            raise TypeError(f'chatBackMessagesChatAction argument is malformed: \"{chatBackMessagesChatAction}\"')
        elif cheerActionsWizardChatAction is not None and not isinstance(cheerActionsWizardChatAction, CheerActionsWizardChatAction):
            raise TypeError(f'cheerActionsWizardChatAction argument is malformed: \"{cheerActionsWizardChatAction}\"')
        elif chatActions is not None and not isinstance(chatActions, Collection):
            raise TypeError(f'chatActions argument is malformed: \"{chatActions}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(mostRecentChatsRepository, MostRecentChatsRepositoryInterface):
            raise TypeError(f'mostRecentChatsRepository argument is malformed: \"{mostRecentChatsRepository}\"')
        elif recurringActionsWizardChatAction is not None and not isinstance(recurringActionsWizardChatAction, RecurringActionsWizardChatAction):
            raise TypeError(f'recurringActionsWizardChatAction argument is malformed: \"{recurringActionsWizardChatAction}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif voicemailChatAction is not None and not isinstance(voicemailChatAction, VoicemailChatAction):
            raise TypeError(f'voicemailChatAction argument is malformed: \"{voicemailChatAction}\"')

        self.__activeChattersRepository: Final[ActiveChattersRepositoryInterface] = activeChattersRepository
        self.__chatBackMessagesChatAction: Final[AbsChatAction | None] = chatBackMessagesChatAction
        self.__cheerActionsWizardChatAction: Final[CheerActionsWizardChatAction | None] = cheerActionsWizardChatAction
        self.__mostRecentChatsRepository: Final[MostRecentChatsRepositoryInterface] = mostRecentChatsRepository
        self.__recurringActionsWizardChatAction: Final[AbsChatAction | None] = recurringActionsWizardChatAction
        self.__timber: Final[TimberInterface] = timber
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository
        self.__voicemailChatAction: Final[VoicemailChatAction | None] = voicemailChatAction

    async def handleMessage(self, message: TwitchMessage):
        if not isinstance(message, TwitchMessage):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        await self.__activeChattersRepository.add(
            chatterUserId = message.getAuthorId(),
            chatterUserName = message.getAuthorName(),
            twitchChannelId = await message.getTwitchChannelId(),
        )

        mostRecentChat = await self.__mostRecentChatsRepository.get(
            chatterUserId = message.getAuthorId(),
            twitchChannelId = await message.getTwitchChannelId(),
        )

        user = await self.__usersRepository.getUserAsync(message.getTwitchChannelName())

        if self.__chatBackMessagesChatAction is not None:
            await self.__chatBackMessagesChatAction.handleChat(
                mostRecentChat = mostRecentChat,
                message = message,
                user = user,
            )

        if self.__cheerActionsWizardChatAction is not None:
            await self.__cheerActionsWizardChatAction.handleChat(
                mostRecentChat = mostRecentChat,
                message = message,
                user = user,
            )

        if self.__recurringActionsWizardChatAction is not None:
            await self.__recurringActionsWizardChatAction.handleChat(
                mostRecentChat = mostRecentChat,
                message = message,
                user = user,
            )

        if self.__voicemailChatAction is not None:
            await self.__voicemailChatAction.handleChat(
                mostRecentChat = mostRecentChat,
                message = message,
                user = user,
            )
