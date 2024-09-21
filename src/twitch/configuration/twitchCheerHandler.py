import math

from .twitchChannelProvider import TwitchChannelProvider
from ..absTwitchCheerHandler import AbsTwitchCheerHandler
from ..api.websocket.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ...cheerActions.cheerActionHelperInterface import CheerActionHelperInterface
from ...misc import utils as utils
from ...soundPlayerManager.soundAlert import SoundAlert
from ...streamAlertsManager.streamAlert import StreamAlert
from ...streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ...timber.timberInterface import TimberInterface
from ...trivia.builder.triviaGameBuilderInterface import TriviaGameBuilderInterface
from ...trivia.triviaGameMachineInterface import TriviaGameMachineInterface
from ...tts.ttsCheerDonation import TtsCheerDonation
from ...tts.ttsDonation import TtsDonation
from ...tts.ttsEvent import TtsEvent
from ...tts.ttsProvider import TtsProvider
from ...users.userInterface import UserInterface


class TwitchCheerHandler(AbsTwitchCheerHandler):

    def __init__(
        self,
        cheerActionHelper: CheerActionHelperInterface | None,
        streamAlertsManager: StreamAlertsManagerInterface | None,
        timber: TimberInterface,
        triviaGameBuilder: TriviaGameBuilderInterface | None,
        triviaGameMachine: TriviaGameMachineInterface | None
    ):
        if cheerActionHelper is not None and not isinstance(cheerActionHelper, CheerActionHelperInterface):
            raise TypeError(f'cheerActionHelper argument is malformed: \"{cheerActionHelper}\"')
        elif streamAlertsManager is not None and not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif triviaGameBuilder is not None and not isinstance(triviaGameBuilder, TriviaGameBuilderInterface):
            raise TypeError(f'triviaGameBuilder argument is malformed: \"{triviaGameBuilder}\"')
        elif triviaGameMachine is not None and not isinstance(triviaGameMachine, TriviaGameMachineInterface):
            raise TypeError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')

        self.__cheerActionHelper: CheerActionHelperInterface | None = cheerActionHelper
        self.__streamAlertsManager: StreamAlertsManagerInterface | None = streamAlertsManager
        self.__timber: TimberInterface = timber
        self.__triviaGameBuilder: TriviaGameBuilderInterface | None = triviaGameBuilder
        self.__triviaGameMachine: TriviaGameMachineInterface | None = triviaGameMachine

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def onNewCheer(
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
            self.__timber.log('TwitchCheerHandler', f'Received a data bundle that has no event (channel=\"{user.getHandle()}\") ({dataBundle=})')
            return

        bits = event.bits
        message = event.message
        broadcasterUserId = event.broadcasterUserId
        cheerUserId = event.userId
        cheerUserLogin = event.userLogin
        cheerUserName = event.userName

        if not utils.isValidInt(bits) or bits < 1 or not utils.isValidStr(broadcasterUserId) or not utils.isValidStr(cheerUserId) or not utils.isValidStr(cheerUserLogin) or not utils.isValidStr(cheerUserName):
            self.__timber.log('TwitchCheerHandler', f'Received a data bundle that is missing crucial data: (channel=\"{user.getHandle()}\") ({dataBundle=}) ({bits=}) ({message=}) ({broadcasterUserId=}) ({cheerUserId=}) ({cheerUserLogin=}) ({cheerUserName=})')
            return

        self.__timber.log('TwitchCheerHandler', f'Received a cheer event: (channel=\"{user.getHandle()}\") ({dataBundle=}) ({bits=}) ({message=}) ({broadcasterUserId=}) ({cheerUserId=}) ({cheerUserLogin=}) ({cheerUserName=})')

        if user.isSuperTriviaGameEnabled():
            await self.__processSuperTriviaEvent(
                bits = bits,
                broadcasterUserId = broadcasterUserId,
                user = user
            )

        if user.areCheerActionsEnabled and await self.__processCheerAction(
            bits = bits,
            broadcasterUserId = broadcasterUserId,
            cheerUserId = cheerUserId,
            cheerUserLogin = cheerUserLogin,
            message = message,
            messageId = event.messageId,
            user = user
        ):
            return

        if user.isTtsEnabled():
            await self.__processTtsEvent(
                bits = bits,
                broadcasterUserId = broadcasterUserId,
                message = message,
                cheerUserId = cheerUserId,
                cheerUserLogin = cheerUserLogin,
                user = user
            )

    async def __processCheerAction(
        self,
        bits: int,
        broadcasterUserId: str,
        cheerUserId: str,
        cheerUserLogin: str,
        message: str | None,
        messageId: str | None,
        user: UserInterface
    ) -> bool:
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not utils.isValidStr(cheerUserId):
            raise TypeError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserLogin):
            raise TypeError(f'cheerUserLogin argument is malformed: \"{cheerUserLogin}\"')
        elif message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif messageId is not None and not isinstance(messageId, str):
            raise TypeError(f'messageId argument is malformed: \"{messageId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        cheerActionHelper = self.__cheerActionHelper

        if cheerActionHelper is None or not utils.isValidStr(message):
            return False

        return await cheerActionHelper.handleCheerAction(
            bits = bits,
            broadcasterUserId = broadcasterUserId,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserLogin,
            message = message,
            twitchChatMessageId = messageId,
            user =  user
        )

    async def __processSuperTriviaEvent(
        self,
        bits: int,
        broadcasterUserId: str,
        user: UserInterface
    ):
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        triviaGameBuilder = self.__triviaGameBuilder
        triviaGameMachine = self.__triviaGameMachine

        if triviaGameBuilder is None or triviaGameMachine is None:
            return
        elif not user.isSuperTriviaGameEnabled():
            return

        superTriviaCheerTriggerAmount = user.getSuperTriviaCheerTriggerAmount()
        superTriviaCheerTriggerMaximum = user.getSuperTriviaCheerTriggerMaximum()

        if not utils.isValidNum(superTriviaCheerTriggerAmount) or bits < superTriviaCheerTriggerAmount:
            return

        numberOfGames = int(math.floor(bits / superTriviaCheerTriggerAmount))

        if numberOfGames < 1:
            return
        elif utils.isValidInt(superTriviaCheerTriggerMaximum) and numberOfGames > superTriviaCheerTriggerMaximum:
            numberOfGames = superTriviaCheerTriggerMaximum

        action = await triviaGameBuilder.createNewSuperTriviaGame(
            twitchChannel = user.getHandle(),
            twitchChannelId = broadcasterUserId,
            numberOfGames = numberOfGames
        )

        if action is not None:
            triviaGameMachine.submitAction(action)

    async def __processTtsEvent(
        self,
        bits: int,
        broadcasterUserId: str,
        cheerUserId: str,
        cheerUserLogin: str,
        message: str | None,
        user: UserInterface
    ):
        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not utils.isValidStr(cheerUserId):
            raise TypeError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserLogin):
            raise TypeError(f'cheerUserLogin argument is malformed: \"{cheerUserLogin}\"')
        elif message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        streamAlertsManager = self.__streamAlertsManager

        if streamAlertsManager is None or not user.isTtsEnabled():
            return

        maximumTtsCheerAmount = user.getMaximumTtsCheerAmount()
        minimumTtsCheerAmount = user.getMinimumTtsCheerAmount()

        if utils.isValidInt(maximumTtsCheerAmount) and utils.isValidInt(minimumTtsCheerAmount) and (bits < minimumTtsCheerAmount or bits > maximumTtsCheerAmount):
            return
        elif utils.isValidInt(maximumTtsCheerAmount) and bits > maximumTtsCheerAmount:
            return
        elif utils.isValidInt(minimumTtsCheerAmount) and bits < minimumTtsCheerAmount:
            return

        donation: TtsDonation = TtsCheerDonation(bits = bits)
        provider: TtsProvider

        if bits >= 150:
            provider = TtsProvider.TTS_MONSTER
        elif bits >= 100:
            provider = TtsProvider.STREAM_ELEMENTS
        else:
            provider = TtsProvider.DEC_TALK

        streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = SoundAlert.CHEER,
            twitchChannel = user.getHandle(),
            twitchChannelId = broadcasterUserId,
            ttsEvent = TtsEvent(
                message = message,
                twitchChannel = user.getHandle(),
                twitchChannelId = broadcasterUserId,
                userId = cheerUserId,
                userName = cheerUserLogin,
                donation = donation,
                provider = provider,
                raidInfo = None
            )
        ))

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider
