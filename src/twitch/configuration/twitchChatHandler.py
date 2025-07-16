import math
from typing import Final

from .twitchChannelProvider import TwitchChannelProvider
from ..absTwitchChatHandler import AbsTwitchChatHandler
from ..api.models.twitchChatMessage import TwitchChatMessage
from ..api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ...chatLogger.chatLoggerInterface import ChatLoggerInterface
from ...cheerActions.cheerActionHelperInterface import CheerActionHelperInterface
from ...misc import utils as utils
from ...soundPlayerManager.soundAlert import SoundAlert
from ...streamAlertsManager.streamAlert import StreamAlert
from ...streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ...timber.timberInterface import TimberInterface
from ...trivia.builder.triviaGameBuilderInterface import TriviaGameBuilderInterface
from ...trivia.triviaGameMachineInterface import TriviaGameMachineInterface
from ...tts.models.ttsCheerDonation import TtsCheerDonation
from ...tts.models.ttsEvent import TtsEvent
from ...tts.models.ttsProvider import TtsProvider
from ...tts.models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ...users.userInterface import UserInterface


class TwitchChatHandler(AbsTwitchChatHandler):

    def __init__(
        self,
        chatLogger: ChatLoggerInterface,
        cheerActionHelper: CheerActionHelperInterface | None,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        triviaGameBuilder: TriviaGameBuilderInterface | None,
        triviaGameMachine: TriviaGameMachineInterface | None,
    ):
        if not isinstance(chatLogger, ChatLoggerInterface):
            raise TypeError(f'chatLogger argument is malformed: \"{chatLogger}\"')
        elif cheerActionHelper is not None and not isinstance(cheerActionHelper, CheerActionHelperInterface):
            raise TypeError(f'cheerActionHelper argument is malformed: \"{cheerActionHelper}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif triviaGameBuilder is not None and not isinstance(triviaGameBuilder, TriviaGameBuilderInterface):
            raise TypeError(f'triviaGameBuilder argument is malformed: \"{triviaGameBuilder}\"')
        elif triviaGameMachine is not None and not isinstance(triviaGameMachine, TriviaGameMachineInterface):
            raise TypeError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')

        self.__chatLogger: Final[ChatLoggerInterface] = chatLogger
        self.__cheerActionHelper: Final[CheerActionHelperInterface | None] = cheerActionHelper
        self.__streamAlertsManager: Final[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: Final[TimberInterface] = timber
        self.__triviaGameBuilder: Final[TriviaGameBuilderInterface | None] = triviaGameBuilder
        self.__triviaGameMachine: Final[TriviaGameMachineInterface | None] = triviaGameMachine

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def __handleCheer(
        self,
        bits: int | None,
        chatterUserId: str,
        chatterUserLogin: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        chatMessage: TwitchChatMessage,
        user: UserInterface,
    ):
        if bits is None or bits < 1:
            return

        if user.isChatLoggingEnabled:
            self.__chatLogger.logCheer(
                bits = bits,
                twitchChannel = user.handle,
                twitchChannelId = twitchChannelId,
                userId = chatterUserId,
                userName = chatterUserLogin,
            )

        if user.areCheerActionsEnabled:
            if await self.__processCheerAction(
                bits = bits,
                chatterUserId = chatterUserId,
                chatterUserLogin = chatterUserLogin,
                twitchChannelId = twitchChannelId,
                twitchChatMessageId = twitchChatMessageId,
                chatMessage = chatMessage,
                user = user,
            ):
                return

        if user.isTtsEnabled:
            await self.__processTtsEvent(
                bits = bits,
                chatMessage = chatMessage,
                chatterUserId = chatterUserId,
                chatterUserLogin = chatterUserLogin,
                twitchChannelId = twitchChannelId,
                user = user,
            )

        if user.isSuperTriviaGameEnabled:
            await self.__processSuperTriviaEvent(
                bits = bits,
                twitchChannelId = twitchChannelId,
                user = user,
            )

    async def onNewChat(
        self,
        bits: int | None,
        chatMessage: str,
        chatterUserId: str,
        chatterUserLogin: str,
        chatterUserName: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        user: UserInterface,
    ):
        if bits is not None and not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits is not None and (bits < 0 or bits > utils.getIntMaxSafeSize()):
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif chatMessage is not None and not isinstance(chatMessage, str):
            raise TypeError(f'chatMessage argument is malformed: \"{chatMessage}\"')
        elif not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(chatterUserLogin):
            raise TypeError(f'chatterUserLogin argument is malformed: \"{chatterUserLogin}\"')
        elif not utils.isValidStr(chatterUserName):
            raise TypeError(f'chatterUserName argument is malformed: \"{chatterUserName}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif twitchChatMessageId is not None and not isinstance(twitchChatMessageId, str):
            raise TypeError(f'twitchChatMessageId argument is malformed: \"{twitchChatMessageId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        # TODO
        return

    async def onNewChatDataBundle(
        self,
        twitchChannelId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle,
    ):
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(dataBundle, TwitchWebsocketDataBundle):
            raise TypeError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        event = dataBundle.requirePayload().event

        if event is None:
            self.__timber.log('TwitchChatHandler', f'Received a data bundle that has no event: ({user=}) ({twitchChannelId=}) ({dataBundle=})')
            return

        ##################################################################################################
        ### INTENTIONALLY COMMENTED OUT WHILE I TEST MOVING THIS FUNCTIONALITY INTO TWITCHCHEERHANDLER ###
        ##################################################################################################
        #
        # chatterUserId = event.chatterUserId
        # chatterUserLogin = event.chatterUserLogin
        # chatterUserName = event.chatterUserName
        # chatMessage = event.chatMessage
        #
        # if not utils.isValidStr(chatterUserId) or not utils.isValidStr(chatterUserLogin) or not utils.isValidStr(chatterUserName) or chatMessage is None:
        #     self.__timber.log('TwitchChatHandler', f'Received a data bundle that is missing crucial data: ({user=}) ({userId=}) ({dataBundle=}) ({chatterUserId=}) ({chatterUserLogin=}) ({chatterUserName=}) ({chatMessage=}) ({event.cheer=})')
        #     return
        #
        # await self.__handleCheer(
        #     twitchChannelId = twitchChannelId,
        #     chatterUserId = chatterUserId,
        #     chatterUserLogin = chatterUserLogin,
        #     chatMessage = chatMessage,
        #     twitchChatMessageId = event.messageId,
        #     cheer = event.cheer,
        #     user = user
        # )

    async def __processCheerAction(
        self,
        bits: int,
        chatterUserId: str,
        chatterUserLogin: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        chatMessage: TwitchChatMessage,
        user: UserInterface,
    ) -> bool:
        if not user.areCheerActionsEnabled:
            return False
        elif self.__cheerActionHelper is None:
            return False
        else:
            return await self.__cheerActionHelper.handleCheerAction(
                bits = bits,
                broadcasterUserId = twitchChannelId,
                cheerUserId = chatterUserId,
                cheerUserName = chatterUserLogin,
                message = chatMessage.text,
                twitchChatMessageId = twitchChatMessageId,
                user = user,
            )

    async def __processSuperTriviaEvent(
        self,
        bits: int,
        twitchChannelId: str,
        user: UserInterface,
    ):
        if not user.isSuperTriviaGameEnabled:
            return
        elif self.__triviaGameBuilder is None or self.__triviaGameMachine is None:
            return

        superTriviaCheerTriggerAmount = user.superTriviaCheerTriggerAmount
        superTriviaCheerTriggerMaximum = user.superTriviaCheerTriggerMaximum

        if superTriviaCheerTriggerAmount is None or superTriviaCheerTriggerAmount < 1 or bits < superTriviaCheerTriggerAmount:
            return

        numberOfGames = int(math.floor(float(bits) / float(superTriviaCheerTriggerAmount)))

        if numberOfGames < 1:
            return
        elif superTriviaCheerTriggerMaximum is not None and numberOfGames > superTriviaCheerTriggerMaximum:
            numberOfGames = int(min(numberOfGames, superTriviaCheerTriggerMaximum))

        action = await self.__triviaGameBuilder.createNewSuperTriviaGame(
            twitchChannel = user.handle,
            twitchChannelId = twitchChannelId,
            numberOfGames = numberOfGames,
        )

        if action is not None:
            self.__triviaGameMachine.submitAction(action)

    async def __processTtsEvent(
        self,
        bits: int,
        chatterUserId: str,
        chatterUserLogin: str,
        twitchChannelId: str,
        chatMessage: TwitchChatMessage,
        user: UserInterface,
    ):
        if not user.isTtsEnabled:
            return

        provider: TtsProvider | None = None
        ttsBoosterPacks = user.ttsBoosterPacks

        if ttsBoosterPacks is None or len(ttsBoosterPacks) == 0:
            return

        for ttsBoosterPack in ttsBoosterPacks:
            if bits >= ttsBoosterPack.cheerAmount:
                provider = ttsBoosterPack.ttsProvider
                break

        if provider is None:
            return

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = SoundAlert.CHEER,
            twitchChannel = user.handle,
            twitchChannelId = twitchChannelId,
            ttsEvent = TtsEvent(
                message = chatMessage.text,
                twitchChannel = user.handle,
                twitchChannelId = twitchChannelId,
                userId = chatterUserId,
                userName = chatterUserLogin,
                donation = TtsCheerDonation(
                    bits = bits,
                ),
                provider = provider,
                providerOverridableStatus = TtsProviderOverridableStatus.THIS_EVENT_DISABLED,
                raidInfo = None,
            ),
        ))

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider
