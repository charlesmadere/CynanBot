from datetime import datetime, timedelta, timezone
from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.chatActions.absChatAction import AbsChatAction
from CynanBot.chatActions.chatActionsManagerInterface import \
    ChatActionsManagerInterface
from CynanBot.chatActions.supStreamerChatAction import SupStreamerChatAction
from CynanBot.chatLogger.chatLoggerInterface import ChatLoggerInterface
from CynanBot.generalSettingsRepository import GeneralSettingsRepository
from CynanBot.mostRecentChat.mostRecentChat import MostRecentChat
from CynanBot.mostRecentChat.mostRecentChatsRepositoryInterface import \
    MostRecentChatsRepositoryInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.tts.ttsEvent import TtsEvent
from CynanBot.tts.ttsManagerInterface import TtsManagerInterface
from CynanBot.twitch.configuration.twitchMessage import TwitchMessage
from CynanBot.twitch.twitchUtils import TwitchUtils
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBot.users.userInterface import UserInterface
from CynanBot.users.usersRepositoryInterface import UsersRepositoryInterface


class ChatActionsManager(ChatActionsManagerInterface):

    def __init__(
        self,
        chatLogger: Optional[ChatLoggerInterface], 
        generalSettingsRepository: GeneralSettingsRepository,
        mostRecentChatsRepository: Optional[MostRecentChatsRepositoryInterface],
        supStreamerChatAction: Optional[SupStreamerChatAction],
        timber: TimberInterface,
        ttsManager: Optional[TtsManagerInterface],
        twitchUtils: TwitchUtils,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
        supStreamerCooldown: timedelta = timedelta(hours = 16),
        timeZone: timezone = timezone.utc
    ):
        if chatLogger is not None and not isinstance(chatLogger, ChatLoggerInterface):
            raise ValueError(f'chatLogger argument is malformed: \"{chatLogger}\"')
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif mostRecentChatsRepository is not None and not isinstance(mostRecentChatsRepository, MostRecentChatsRepositoryInterface):
            raise ValueError(f'mostRecentChatsRepository argument is malformed: \"{mostRecentChatsRepository}\"')
        elif supStreamerChatAction is not None and not isinstance(supStreamerChatAction, SupStreamerChatAction):
            raise ValueError(f'supStreamerChatAction argument is malformed: \"{supStreamerChatAction}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif ttsManager is not None and not isinstance(ttsManager, TtsManagerInterface):
            raise ValueError(f'ttsManager argument is malformed: \"{ttsManager}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(supStreamerCooldown, timedelta):
            raise ValueError(f'supStreamerCooldown argument is malformed: \"{supStreamerCooldown}\"')
        elif not isinstance(timeZone, timezone):
            raise ValueError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__chatLogger: Optional[ChatLoggerInterface] = chatLogger
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__mostRecentChatsRepository: Optional[MostRecentChatsRepositoryInterface] =  mostRecentChatsRepository
        self.__supStreamerChatAction: Optional[AbsChatAction] = supStreamerChatAction
        self.__timber: TimberInterface = timber
        self.__ttsManager: Optional[TtsManagerInterface] = ttsManager
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__supStreamerCooldown: timedelta = supStreamerCooldown
        self.__timeZone: timezone = timeZone

    async def handleMessage(self, message: TwitchMessage):
        if not isinstance(message, TwitchMessage):
            raise ValueError(f'message argument is malformed: \"{message}\"')

        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if generalSettings.isPersistAllUsersEnabled():
            await self.__userIdsRepository.setUser(
                userId = message.getAuthorId(),
                userName = message.getAuthorName()
            )

        user = await self.__usersRepository.getUserAsync(message.getTwitchChannelName())
        mostRecentChat = await self.__handleMostRecentChat(message)

        await self.__handleSupMessage(
            mostRecentChat = mostRecentChat,
            message = message,
            user = user,
        )

    async def __handleMostRecentChat(self, message: TwitchMessage):
        if not isinstance(message, TwitchMessage):
            raise ValueError(f'message argument is malformed: \"{message}\"')

        if self.__mostRecentChatsRepository is None:
            return None

        mostRecentChat = await self.__mostRecentChatsRepository.get(
            chatterUserId = message.getAuthorId(),
            twitchChannelId = await message.getTwitchChannelId()
        )

        await self.__mostRecentChatsRepository.set(
            chatterUserId = message.getAuthorId(),
            twitchChannelId = await message.getTwitchChannelId()
        )

        return mostRecentChat

    async def __handleSupMessage(
        self,
        mostRecentChat: Optional[MostRecentChat],
        message: TwitchMessage,
        user: UserInterface
    ):
        if mostRecentChat is not None and not isinstance(mostRecentChat, MostRecentChat):
            raise ValueError(f'mostRecentChat argument is malformed: \"{mostRecentChat}\"')
        elif not isinstance(message, TwitchMessage):
            raise ValueError(f'message argument is malformed: \"{message}\"')
        elif not isinstance(user, UserInterface):
            raise ValueError(f'user argument is malformed: \"{user}\"')

        if self.__ttsManager is None:
            return
        elif not user.isSupStreamerEnabled() and not user.isTtsEnabled():
            return

        now = datetime.now(self.__timeZone)

        if mostRecentChat is not None and (mostRecentChat.getMostRecentChat() + self.__supStreamerCooldown) > now:
            return

        supStreamerMessage = user.getSupStreamerMessage()

        if not utils.isValidStr(supStreamerMessage) or message.getContent() != supStreamerMessage:
            return

        self.__ttsManager.submitTtsEvent(TtsEvent(
            message = f'{message.getAuthorName()} sup',
            twitchChannel = user.getHandle(),
            userId = message.getAuthorId(),
            userName = message.getAuthorName(),
            donation = None,
            raidInfo = None
        ))
