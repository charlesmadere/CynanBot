import math

from .twitchChannelProvider import TwitchChannelProvider
from ..absTwitchCheerHandler import AbsTwitchCheerHandler
from ..api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
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
        cheerActionHelper: CheerActionHelperInterface | None,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        triviaGameBuilder: TriviaGameBuilderInterface | None,
        triviaGameMachine: TriviaGameMachineInterface | None
    ):
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

        self.__cheerActionHelper: CheerActionHelperInterface | None = cheerActionHelper
        self.__streamAlertsManager: StreamAlertsManagerInterface = streamAlertsManager
        self.__timber: TimberInterface = timber
        self.__triviaGameBuilder: TriviaGameBuilderInterface | None = triviaGameBuilder
        self.__triviaGameMachine: TriviaGameMachineInterface | None = triviaGameMachine

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def __handleCheer(
        self,
        bits: int,
        broadcasterUserId: str,
        chatMessage: str,
        cheerUserId: str,
        cheerUserLogin: str,
        cheerUserName: str,
        twitchChatMessageId: str | None,
        user: UserInterface
    ):
        if user.isSuperTriviaGameEnabled:
            await self.__processSuperTriviaEvent(
                bits = bits,
                broadcasterUserId = broadcasterUserId,
                user = user
            )

        if user.areCheerActionsEnabled:
            if await self.__processCheerAction(
                bits = bits,
                broadcasterUserId = broadcasterUserId,
                cheerUserId = cheerUserId,
                cheerUserLogin = cheerUserLogin,
                twitchChatMessageId = twitchChatMessageId,
                chatMessage = chatMessage,
                user = user
            ):
                return

        if user.isTtsEnabled:
            await self.__processTtsEvent(
                bits = bits,
                broadcasterUserId = broadcasterUserId,
                chatMessage = chatMessage,
                cheerUserId = cheerUserId,
                cheerUserLogin = cheerUserLogin,
                user = user
            )

    async def onNewCheer(
        self,
        bits: int | None,
        broadcasterUserId: str,
        chatMessage: str | None,
        cheerUserId: str | None,
        cheerUserLogin: str | None,
        cheerUserName: str | None,
        twitchChatMessageId: str | None,
        user: UserInterface
    ):
        if not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        if bits is None or bits < 1 or not utils.isValidStr(chatMessage) or not utils.isValidStr(cheerUserId) or not utils.isValidStr(cheerUserLogin) or not utils.isValidStr(cheerUserName):
            self.__timber.log('TwitchCheerHandler', f'Received a data bundle that is missing crucial data: ({user=}) ({broadcasterUserId=}) ({bits=}) ({chatMessage=}) ({cheerUserId=}) ({cheerUserLogin=}) ({cheerUserName=}) ({twitchChatMessageId=})')
            return

        await self.__handleCheer(
            bits = bits,
            broadcasterUserId = broadcasterUserId,
            chatMessage = chatMessage,
            cheerUserId = cheerUserId,
            cheerUserLogin = cheerUserLogin,
            cheerUserName = cheerUserName,
            twitchChatMessageId = twitchChatMessageId,
            user = user
        )

    async def onNewCheerDataBundle(
        self,
        broadcasterUserId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle
    ):
        if not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(dataBundle, TwitchWebsocketDataBundle):
            raise TypeError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        event = dataBundle.requirePayload().event

        if event is None:
            self.__timber.log('TwitchCheerHandler', f'Received a data bundle that has no event: ({user=}) ({broadcasterUserId=}) ({dataBundle=})')
            return

        await self.onNewCheer(
            bits = event.bits,
            broadcasterUserId = broadcasterUserId,
            chatMessage = event.message,
            cheerUserId = event.userId,
            cheerUserLogin = event.userLogin,
            cheerUserName = event.userName,
            twitchChatMessageId = event.messageId,
            user = user
        )

    async def __processCheerAction(
        self,
        bits: int,
        chatMessage: str,
        broadcasterUserId: str,
        cheerUserId: str,
        cheerUserLogin: str,
        twitchChatMessageId: str | None,
        user: UserInterface
    ) -> bool:
        if not user.areCheerActionsEnabled:
            return False
        elif self.__cheerActionHelper is None:
            return False
        else:
            return await self.__cheerActionHelper.handleCheerAction(
                bits = bits,
                broadcasterUserId = broadcasterUserId,
                cheerUserId = cheerUserId,
                cheerUserName = cheerUserLogin,
                message = chatMessage,
                twitchChatMessageId = twitchChatMessageId,
                user = user
            )

    async def __processSuperTriviaEvent(
        self,
        bits: int,
        broadcasterUserId: str,
        user: UserInterface
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
            twitchChannelId = broadcasterUserId,
            numberOfGames = numberOfGames
        )

        if action is not None:
            self.__triviaGameMachine.submitAction(action)

    async def __processTtsEvent(
        self,
        bits: int,
        broadcasterUserId: str,
        chatMessage: str,
        cheerUserId: str,
        cheerUserLogin: str,
        user: UserInterface
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
            twitchChannelId = broadcasterUserId,
            ttsEvent = TtsEvent(
                message = chatMessage,
                twitchChannel = user.handle,
                twitchChannelId = broadcasterUserId,
                userId = cheerUserId,
                userName = cheerUserLogin,
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
