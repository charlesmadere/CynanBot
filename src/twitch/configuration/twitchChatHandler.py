import math
from typing import Final

from ..absTwitchChatHandler import AbsTwitchChatHandler
from ..api.models.twitchChatMessage import TwitchChatMessage
from ..api.models.twitchChatMessageFragmentType import TwitchChatMessageFragmentType
from ..api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ...chatLogger.chatLoggerInterface import ChatLoggerInterface
from ...cheerActions.cheerActionHelperInterface import CheerActionHelperInterface
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
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
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        chatLogger: ChatLoggerInterface,
        cheerActionHelper: CheerActionHelperInterface | None,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        triviaGameBuilder: TriviaGameBuilderInterface | None,
        triviaGameMachine: TriviaGameMachineInterface | None,
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(chatLogger, ChatLoggerInterface):
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

        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__chatLogger: Final[ChatLoggerInterface] = chatLogger
        self.__cheerActionHelper: Final[CheerActionHelperInterface | None] = cheerActionHelper
        self.__streamAlertsManager: Final[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: Final[TimberInterface] = timber
        self.__triviaGameBuilder: Final[TriviaGameBuilderInterface | None] = triviaGameBuilder
        self.__triviaGameMachine: Final[TriviaGameMachineInterface | None] = triviaGameMachine

    async def __logCheer(self, chatData: AbsTwitchChatHandler.ChatData):
        if chatData.cheer is None or chatData.cheer.bits < 1:
            return

        self.__chatLogger.logCheer(
            bits = chatData.cheer.bits,
            cheerUserId = chatData.chatterUserId,
            cheerUserLogin = chatData.chatterUserLogin,
            twitchChannel = chatData.user.handle,
            twitchChannelId = chatData.twitchChannelId,
        )

    async def onNewChat(self, chatData: AbsTwitchChatHandler.ChatData):
        if not isinstance(chatData, AbsTwitchChatHandler.ChatData):
            raise TypeError(f'chatData argument is malformed: \"{chatData}\"')

        if utils.isValidStr(chatData.sourceMessageId):
            # This is a chat message that originated from a shared chat/stream. As such, let's not
            # even bother to process it or work with it at all. In the future, we may have a reason
            # to change this. But for now, it's better to just ignore these messages completely.
            return

        if chatData.user.isChatLoggingEnabled:
            await self.__logCheer(chatData)

        if chatData.user.areCheerActionsEnabled and await self.__processCheerAction(chatData):
            return

        if chatData.user.isSuperTriviaGameEnabled:
            await self.__processSuperTriviaEvent(chatData)

        if chatData.user.isTtsEnabled:
            await self.__processTtsEvent(chatData)

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

        chatterUserId = event.chatterUserId
        chatterUserLogin = event.chatterUserLogin
        chatterUserName = event.chatterUserName
        chatMessage = event.chatMessage

        if not utils.isValidStr(chatterUserId) or not utils.isValidStr(chatterUserLogin) or not utils.isValidStr(chatterUserName) or chatMessage is None:
            self.__timber.log('TwitchChatHandler', f'Received a data bundle that is missing crucial data: ({user=}) ({twitchChannelId=}) ({dataBundle=}) ({chatterUserId=}) ({chatterUserLogin=}) ({chatterUserName=}) ({chatMessage=})')
            return

        chatData = AbsTwitchChatHandler.ChatData(
            chatterUserId = chatterUserId,
            chatterUserLogin = chatterUserLogin,
            chatterUserName = chatterUserName,
            sourceMessageId = event.sourceMessageId,
            twitchChannelId = twitchChannelId,
            twitchChatMessageId = event.messageId,
            message = chatMessage,
            cheer = event.cheer,
            user = user,
        )

        await self.onNewChat(
            chatData = chatData,
        )

    async def __processCheerAction(self, chatData: AbsTwitchChatHandler.ChatData) -> bool:
        user = chatData.user

        if not user.areCheerActionsEnabled:
            return False
        elif self.__cheerActionHelper is None:
            return False

        cheer = chatData.cheer
        if cheer is None or cheer.bits < 1:
            return False

        messageWithoutCheerText = await self.__purgeChatMessageOfCheers(chatData.message)
        self.__timber.log('TwitchChatHandler', f'Purged message of cheers: ({messageWithoutCheerText=}) ({chatData=})')

        return await self.__cheerActionHelper.handleCheerAction(
            bits = cheer.bits,
            cheerUserId = chatData.chatterUserId,
            cheerUserName = chatData.chatterUserLogin,
            message = chatData.message.text,
            twitchChannelId = chatData.twitchChannelId,
            twitchChatMessageId = chatData.twitchChatMessageId,
            user = user,
        )

    async def __processSuperTriviaEvent(self, chatData: AbsTwitchChatHandler.ChatData):
        user = chatData.user

        if not user.isSuperTriviaGameEnabled:
            return
        elif self.__triviaGameBuilder is None or self.__triviaGameMachine is None:
            return

        cheer = chatData.cheer
        if cheer is None or cheer.bits < 1:
            return

        superTriviaCheerTriggerAmount = user.superTriviaCheerTriggerAmount
        superTriviaCheerTriggerMaximum = user.superTriviaCheerTriggerMaximum

        if superTriviaCheerTriggerAmount is None or superTriviaCheerTriggerAmount < 1 or cheer.bits < superTriviaCheerTriggerAmount:
            return

        numberOfGames = int(math.floor(float(cheer.bits) / float(superTriviaCheerTriggerAmount)))

        if numberOfGames < 1:
            return
        elif superTriviaCheerTriggerMaximum is not None and numberOfGames > superTriviaCheerTriggerMaximum:
            numberOfGames = int(min(numberOfGames, superTriviaCheerTriggerMaximum))

        action = await self.__triviaGameBuilder.createNewSuperTriviaGame(
            twitchChannel = user.handle,
            twitchChannelId = chatData.twitchChannelId,
            numberOfGames = numberOfGames,
        )

        if action is not None:
            self.__triviaGameMachine.submitAction(action)

    async def __processTtsEvent(self, chatData: AbsTwitchChatHandler.ChatData):
        user = chatData.user

        if not user.isTtsEnabled:
            return

        cheer = chatData.cheer
        if cheer is None or cheer.bits < 1:
            return

        provider: TtsProvider | None = None
        ttsBoosterPacks = user.ttsBoosterPacks

        if ttsBoosterPacks is None or len(ttsBoosterPacks) == 0:
            return

        for ttsBoosterPack in ttsBoosterPacks:
            if ttsBoosterPack.isEnabled and cheer.bits >= ttsBoosterPack.cheerAmount:
                provider = ttsBoosterPack.ttsProvider
                break

        if provider is None:
            return

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = SoundAlert.CHEER,
            twitchChannel = user.handle,
            twitchChannelId = chatData.twitchChannelId,
            ttsEvent = TtsEvent(
                message = chatData.message.text,
                twitchChannel = user.handle,
                twitchChannelId = chatData.twitchChannelId,
                userId = chatData.chatterUserId,
                userName = chatData.chatterUserLogin,
                donation = TtsCheerDonation(
                    bits = cheer.bits,
                ),
                provider = provider,
                providerOverridableStatus = TtsProviderOverridableStatus.THIS_EVENT_DISABLED,
                raidInfo = None,
            ),
        ))

    async def __purgeChatMessageOfCheers(self, message: TwitchChatMessage) -> str:
        purgedMessage = ''

        for fragment in message.fragments:
            if fragment.fragmentType is not TwitchChatMessageFragmentType.CHEERMOTE:
                purgedMessage = f'{purgedMessage} {fragment.text}'

        return utils.cleanStr(purgedMessage)
