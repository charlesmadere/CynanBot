import math
from typing import Final

from .twitchChannelProvider import TwitchChannelProvider
from ..absTwitchCheerHandler import AbsTwitchCheerHandler
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


class TwitchCheerHandler(AbsTwitchCheerHandler):

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
        if cheerActionHelper is not None and not isinstance(cheerActionHelper, CheerActionHelperInterface):
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

    async def __logCheer(self, cheerData: AbsTwitchCheerHandler.CheerData):
        self.__chatLogger.logCheer(
            bits = cheerData.bits,
            cheerUserId = cheerData.cheerUserId,
            cheerUserLogin = cheerData.cheerUserLogin,
            twitchChannel = cheerData.user.handle,
            twitchChannelId = cheerData.twitchChannelId,
        )

    async def onNewCheer(self, cheerData: AbsTwitchCheerHandler.CheerData):
        if not isinstance(cheerData, AbsTwitchCheerHandler.CheerData):
            raise TypeError(f'cheerData argument is malformed: \"{cheerData}\"')

        if cheerData.user.isChatLoggingEnabled:
            await self.__logCheer(cheerData)

        if cheerData.user.areCheerActionsEnabled and await self.__processCheerAction(cheerData):
            return

        if cheerData.user.isSuperTriviaGameEnabled:
            await self.__processSuperTriviaEvent(cheerData)

        if cheerData.user.isTtsEnabled:
            await self.__processTtsEvent(cheerData)

    async def onNewCheerDataBundle(
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
            self.__timber.log('TwitchCheerHandler', f'Received a data bundle that has no event: ({user=}) ({twitchChannelId=}) ({dataBundle=})')
            return

        bits = event.bits
        chatMessage = event.message
        cheerUserId = event.userId
        cheerUserLogin = event.userLogin
        cheerUserName = event.userName

        if not utils.isValidInt(bits) or bits < 1 or not utils.isValidStr(chatMessage) or not utils.isValidStr(cheerUserId) or not utils.isValidStr(cheerUserLogin) or not utils.isValidStr(cheerUserName):
            self.__timber.log('TwitchCheerHandler', f'Received a data bundle that is missing crucial data: ({user=}) ({twitchChannelId=}) ({dataBundle=}) ({bits=}) ({chatMessage=}) ({cheerUserId=}) ({cheerUserLogin=}) ({cheerUserName=})')
            return

        cheerData = AbsTwitchCheerHandler.CheerData(
            bits = bits,
            chatMessage = chatMessage,
            cheerUserId = cheerUserId,
            cheerUserLogin = cheerUserLogin,
            cheerUserName = cheerUserName,
            twitchChannelId = twitchChannelId,
            twitchChatMessageId = event.messageId,
            user = user,
        )

        await self.onNewCheer(
            cheerData = cheerData,
        )

    async def __processCheerAction(self, cheerData: AbsTwitchCheerHandler.CheerData) -> bool:
        user = cheerData.user

        if not user.areCheerActionsEnabled:
            return False
        elif self.__cheerActionHelper is None:
            return False
        else:
            return await self.__cheerActionHelper.handleCheerAction(
                bits = cheerData.bits,
                cheerUserId = cheerData.cheerUserId,
                cheerUserName = cheerData.cheerUserLogin,
                message = cheerData.chatMessage,
                twitchChannelId = cheerData.twitchChannelId,
                twitchChatMessageId = cheerData.twitchChatMessageId,
                user = user,
            )

    async def __processSuperTriviaEvent(self, cheerData: AbsTwitchCheerHandler.CheerData):
        user = cheerData.user

        if not user.isSuperTriviaGameEnabled:
            return
        elif self.__triviaGameBuilder is None or self.__triviaGameMachine is None:
            return

        superTriviaCheerTriggerAmount = user.superTriviaCheerTriggerAmount
        superTriviaCheerTriggerMaximum = user.superTriviaCheerTriggerMaximum

        if superTriviaCheerTriggerAmount is None or superTriviaCheerTriggerAmount < 1 or cheerData.bits < superTriviaCheerTriggerAmount:
            return

        numberOfGames = int(math.floor(float(cheerData.bits) / float(superTriviaCheerTriggerAmount)))

        if numberOfGames < 1:
            return
        elif superTriviaCheerTriggerMaximum is not None and numberOfGames > superTriviaCheerTriggerMaximum:
            numberOfGames = int(min(numberOfGames, superTriviaCheerTriggerMaximum))

        action = await self.__triviaGameBuilder.createNewSuperTriviaGame(
            twitchChannel = user.handle,
            twitchChannelId = cheerData.twitchChannelId,
            numberOfGames = numberOfGames,
        )

        if action is not None:
            self.__triviaGameMachine.submitAction(action)

    async def __processTtsEvent(self, cheerData: AbsTwitchCheerHandler.CheerData):
        user = cheerData.user

        if not user.isTtsEnabled:
            return

        provider: TtsProvider | None = None
        ttsBoosterPacks = user.ttsBoosterPacks

        if ttsBoosterPacks is None or len(ttsBoosterPacks) == 0:
            return

        for ttsBoosterPack in ttsBoosterPacks:
            if cheerData.bits >= ttsBoosterPack.cheerAmount:
                provider = ttsBoosterPack.ttsProvider
                break

        if provider is None:
            return

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = SoundAlert.CHEER,
            twitchChannel = user.handle,
            twitchChannelId = cheerData.twitchChannelId,
            ttsEvent = TtsEvent(
                message = cheerData.chatMessage,
                twitchChannel = user.handle,
                twitchChannelId = cheerData.twitchChannelId,
                userId = cheerData.cheerUserId,
                userName = cheerData.cheerUserLogin,
                donation = TtsCheerDonation(
                    bits = cheerData.bits,
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
