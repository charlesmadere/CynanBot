from .twitchChannelProvider import TwitchChannelProvider
from ..absTwitchChatHandler import AbsTwitchChatHandler
from ..api.models.twitchChatMessage import TwitchChatMessage
from ..api.models.twitchCheerMetadata import TwitchCheerMetadata
from ..api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ...chatLogger.chatLoggerInterface import ChatLoggerInterface
from ...cheerActions.cheerActionHelperInterface import CheerActionHelperInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...users.userInterface import UserInterface


class TwitchChatHandler(AbsTwitchChatHandler):

    def __init__(
        self,
        chatLogger: ChatLoggerInterface,
        cheerActionHelper: CheerActionHelperInterface | None,
        timber: TimberInterface
    ):
        if not isinstance(chatLogger, ChatLoggerInterface):
            raise TypeError(f'chatLogger argument is malformed: \"{chatLogger}\"')
        elif cheerActionHelper is not None and not isinstance(cheerActionHelper, CheerActionHelperInterface):
            raise TypeError(f'cheerActionHelper argument is malformed: \"{cheerActionHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__chatLogger: ChatLoggerInterface = chatLogger
        self.__cheerActionHelper: CheerActionHelperInterface | None = cheerActionHelper
        self.__timber: TimberInterface = timber

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def __handleCheer(
        self,
        broadcasterUserId: str,
        chatterUserId: str,
        chatterUserName: str,
        twitchChatMessageId: str | None,
        chatMessage: TwitchChatMessage,
        cheer: TwitchCheerMetadata | None,
        user: UserInterface
    ):
        if not user.areCheerActionsEnabled:
            return
        elif cheer is None or cheer.bits < 1:
            return
        elif self.__cheerActionHelper is None:
            return

        await self.__cheerActionHelper.handleCheerAction(
            bits = cheer.bits,
            broadcasterUserId = broadcasterUserId,
            cheerUserId = chatterUserId,
            cheerUserName = chatterUserName,
            message = chatMessage.text,
            twitchChatMessageId = twitchChatMessageId,
            user = user
        )

    async def onNewChat(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle
    ):
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(dataBundle, TwitchWebsocketDataBundle):
            raise TypeError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        event = dataBundle.requirePayload().event

        if event is None:
            self.__timber.log('TwitchChatHandler', f'Received a data bundle that has no event: ({user=}) ({userId=}) ({dataBundle=})')
            return

        chatterUserId = event.chatterUserId
        chatterUserName = event.chatterUserName
        chatMessage = event.chatMessage

        if not utils.isValidStr(chatterUserId) or not utils.isValidStr(chatterUserName) or chatMessage is None:
            self.__timber.log('TwitchCheerHandler', f'Received a data bundle that is missing crucial data: ({user=}) ({dataBundle=}) ({chatterUserId=}) ({chatterUserName=}) ({chatMessage=})')
            return

        await self.__handleCheer(
            broadcasterUserId = userId,
            chatterUserId = chatterUserId,
            chatterUserName = chatterUserName,
            chatMessage = chatMessage,
            twitchChatMessageId = event.messageId,
            cheer = event.cheer,
            user = user
        )

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider
