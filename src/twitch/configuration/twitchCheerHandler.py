import math

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
from ...tts.ttsCheerDonation import TtsCheerDonation
from ...tts.ttsEvent import TtsEvent
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
            self.__timber.log('TwitchCheerHandler', f'Received a data bundle that has no event: ({user=}) ({userId=}) ({dataBundle=})')
            return

        bits = event.bits
        message = event.message
        broadcasterUserId = event.broadcasterUserId
        cheerUserId = event.userId
        cheerUserLogin = event.userLogin
        cheerUserName = event.userName

        if bits is None or bits < 1 or not utils.isValidStr(broadcasterUserId) or not utils.isValidStr(cheerUserId) or not utils.isValidStr(cheerUserLogin) or not utils.isValidStr(cheerUserName):
            self.__timber.log('TwitchCheerHandler', f'Received a data bundle that is missing crucial data: ({user=}) ({dataBundle=}) ({bits=}) ({message=}) ({broadcasterUserId=}) ({cheerUserId=}) ({cheerUserLogin=}) ({cheerUserName=})')
            return

        self.__timber.log('TwitchCheerHandler', f'Received a cheer event: ({user=}) ({dataBundle=}) ({bits=}) ({message=}) ({broadcasterUserId=}) ({cheerUserId=}) ({cheerUserLogin=}) ({cheerUserName=})')

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
                message = message,
                messageId = event.messageId,
                user = user
            ):
                return

        if user.isTtsEnabled:
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
        if not user.areCheerActionsEnabled:
            return False
        elif self.__cheerActionHelper is None:
            return False
        elif not utils.isValidStr(message):
            return False

        return await self.__cheerActionHelper.handleCheerAction(
            bits = bits,
            broadcasterUserId = broadcasterUserId,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserLogin,
            message = message,
            twitchChatMessageId = messageId,
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

        numberOfGames = int(math.floor(float(bits) / superTriviaCheerTriggerAmount))

        if numberOfGames < 1:
            return
        elif superTriviaCheerTriggerMaximum is not None and numberOfGames > superTriviaCheerTriggerMaximum:
            numberOfGames = min(numberOfGames, superTriviaCheerTriggerMaximum)

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
        cheerUserId: str,
        cheerUserLogin: str,
        message: str | None,
        user: UserInterface
    ):
        if not user.isTtsEnabled:
            return

        maximumTtsCheerAmount = user.maximumTtsCheerAmount
        minimumTtsCheerAmount = user.minimumTtsCheerAmount

        if utils.isValidInt(maximumTtsCheerAmount) and utils.isValidInt(minimumTtsCheerAmount) and (bits < minimumTtsCheerAmount or bits > maximumTtsCheerAmount):
            return
        elif utils.isValidInt(maximumTtsCheerAmount) and bits > maximumTtsCheerAmount:
            return
        elif utils.isValidInt(minimumTtsCheerAmount) and bits < minimumTtsCheerAmount:
            return

        provider = user.defaultTtsProvider
        ttsBoosterPacks = user.ttsBoosterPacks

        if ttsBoosterPacks is not None and len(ttsBoosterPacks) >= 1:
            for ttsBoosterPack in ttsBoosterPacks:
                if bits >= ttsBoosterPack.cheerAmount:
                    provider = ttsBoosterPack.ttsProvider
                    break

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = SoundAlert.CHEER,
            twitchChannel = user.handle,
            twitchChannelId = broadcasterUserId,
            ttsEvent = TtsEvent(
                allowChatterPreferredTts = False,
                message = message,
                twitchChannel = user.handle,
                twitchChannelId = broadcasterUserId,
                userId = cheerUserId,
                userName = cheerUserLogin,
                donation = TtsCheerDonation(
                    bits = bits
                ),
                provider = provider,
                raidInfo = None
            )
        ))
