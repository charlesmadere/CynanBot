import math
from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.cheerActions.cheerActionHelperInterface import \
    CheerActionHelperInterface
from CynanBot.soundPlayerManager.soundAlert import SoundAlert
from CynanBot.streamAlertsManager.streamAlert import StreamAlert
from CynanBot.streamAlertsManager.streamAlertsManagerInterface import \
    StreamAlertsManagerInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.builder.triviaGameBuilderInterface import \
    TriviaGameBuilderInterface
from CynanBot.trivia.triviaGameMachineInterface import \
    TriviaGameMachineInterface
from CynanBot.tts.ttsCheerDonation import TtsCheerDonation
from CynanBot.tts.ttsDonation import TtsDonation
from CynanBot.tts.ttsEvent import TtsEvent
from CynanBot.tts.ttsProvider import TtsProvider
from CynanBot.twitch.absTwitchCheerHandler import AbsTwitchCheerHandler
from CynanBot.twitch.api.websocket.twitchWebsocketDataBundle import \
    TwitchWebsocketDataBundle
from CynanBot.twitch.configuration.twitchChannelProvider import \
    TwitchChannelProvider
from CynanBot.users.userInterface import UserInterface


class TwitchCheerHandler(AbsTwitchCheerHandler):

    def __init__(
        self,
        cheerActionHelper: Optional[CheerActionHelperInterface],
        streamAlertsManager: Optional[StreamAlertsManagerInterface],
        timber: TimberInterface,
        triviaGameBuilder: Optional[TriviaGameBuilderInterface],
        triviaGameMachine: Optional[TriviaGameMachineInterface],
        twitchChannelProvider: TwitchChannelProvider
    ):
        assert cheerActionHelper is None or isinstance(cheerActionHelper, CheerActionHelperInterface), f"malformed {cheerActionHelper=}"
        assert streamAlertsManager is None or isinstance(streamAlertsManager, StreamAlertsManagerInterface), f"malformed {streamAlertsManager=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert triviaGameBuilder is None or isinstance(triviaGameBuilder, TriviaGameBuilderInterface), f"malformed {triviaGameBuilder=}"
        assert triviaGameMachine is None or isinstance(triviaGameMachine, TriviaGameMachineInterface), f"malformed {triviaGameMachine=}"
        assert isinstance(twitchChannelProvider, TwitchChannelProvider), f"malformed {twitchChannelProvider=}"

        self.__cheerActionHelper: Optional[CheerActionHelperInterface] = cheerActionHelper
        self.__streamAlertsManager: Optional[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: TimberInterface = timber
        self.__triviaGameBuilder: Optional[TriviaGameBuilderInterface] = triviaGameBuilder
        self.__triviaGameMachine: Optional[TriviaGameMachineInterface] = triviaGameMachine
        self.__twitchChannelProvider: TwitchChannelProvider = twitchChannelProvider

    async def onNewCheer(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle
    ):
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        assert isinstance(user, UserInterface), f"malformed {user=}"
        assert isinstance(dataBundle, TwitchWebsocketDataBundle), f"malformed {dataBundle=}"

        event = dataBundle.requirePayload().getEvent()

        if event is None:
            self.__timber.log('TwitchCheerHandler', f'Received a data bundle that has no event: (channel=\"{user.getHandle()}\") ({dataBundle=})')
            return

        bits = event.getBits()
        message = event.getMessage()
        cheerUserId = event.getUserId()
        cheerUserLogin = event.getUserLogin()
        cheerUserName = event.getUserName()

        if not utils.isValidInt(bits) or bits < 1 or not utils.isValidStr(cheerUserId) or not utils.isValidStr(cheerUserLogin) or not utils.isValidStr(cheerUserName):
            self.__timber.log('TwitchCheerHandler', f'Received a data bundle that is missing crucial data: (channel=\"{user.getHandle()}\") ({dataBundle=}) ({bits=}) ({message=}) ({cheerUserId=}) ({cheerUserLogin=}) ({cheerUserName=})')
            return

        self.__timber.log('TwitchCheerHandler', f'Received a cheer event: (channel=\"{user.getHandle()}\") ({dataBundle=}) ({bits=}) ({message=}) ({cheerUserId=}) ({cheerUserLogin=}) ({cheerUserName=})')

        if user.isSuperTriviaGameEnabled():
            await self.__processSuperTriviaEvent(
                bits = bits,
                user = user
            )

        if not user.areCheerActionsEnabled() or not await self.__processCheerAction(
            bits = bits,
            cheerUserId = cheerUserId,
            cheerUserLogin = cheerUserLogin,
            message = message,
            user = user
        ):
            if user.isTtsEnabled():
                await self.__processTtsEvent(
                   bits = bits,
                    message = message,
                    cheerUserId = cheerUserId,
                    cheerUserLogin = cheerUserLogin,
                    user = user
                )

    async def __processCheerAction(
        self,
        bits: int,
        cheerUserId: str,
        cheerUserLogin: str,
        message: Optional[str],
        user: UserInterface
    ) -> bool:
        if not utils.isValidInt(bits):
            raise ValueError(f'bits argument is malformed: \"{bits}\"')
        if bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        if not utils.isValidStr(cheerUserId):
            raise ValueError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        if not utils.isValidStr(cheerUserLogin):
            raise ValueError(f'cheerUserLogin argument is malformed: \"{cheerUserLogin}\"')
        assert message is None or isinstance(message, str), f"malformed {message=}"
        assert isinstance(user, UserInterface), f"malformed {user=}"

        if self.__cheerActionHelper is None:
            return False
        if not utils.isValidStr(message):
            return False

        return await self.__cheerActionHelper.handleCheerAction(
            bits = bits,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserLogin,
            message = message,
            user =  user
        )

    async def __processSuperTriviaEvent(
        self,
        bits: int,
        user: UserInterface
    ):
        if not utils.isValidInt(bits):
            raise ValueError(f'bits argument is malformed: \"{bits}\"')
        if bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        assert isinstance(user, UserInterface), f"malformed {user=}"

        if self.__triviaGameBuilder is None or self.__triviaGameMachine is None:
            return
        elif not user.isSuperTriviaGameEnabled():
            return

        superTriviaCheerTriggerAmount = user.getSuperTriviaCheerTriggerAmount()
        superTriviaCheerTriggerMaximum = user.getSuperTriviaCheerTriggerMaximum()

        if not utils.isValidNum(superTriviaCheerTriggerAmount) or bits < superTriviaCheerTriggerAmount:
            return

        numberOfGames = math.floor(bits / superTriviaCheerTriggerAmount)

        if numberOfGames < 1:
            return
        elif utils.isValidInt(superTriviaCheerTriggerMaximum) and numberOfGames > superTriviaCheerTriggerMaximum:
            numberOfGames = superTriviaCheerTriggerMaximum

        action = await self.__triviaGameBuilder.createNewSuperTriviaGame(
            twitchChannel = user.getHandle(),
            numberOfGames = numberOfGames
        )

        if action is not None:
            self.__triviaGameMachine.submitAction(action)

    async def __processTtsEvent(
        self,
        bits: int,
        cheerUserId: str,
        cheerUserLogin: str,
        message: Optional[str],
        user: UserInterface
    ):
        if not utils.isValidInt(bits):
            raise ValueError(f'bits argument is malformed: \"{bits}\"')
        if bits <= 0 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        if not utils.isValidStr(cheerUserId):
            raise ValueError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        if not utils.isValidStr(cheerUserLogin):
            raise ValueError(f'cheerUserLogin argument is malformed: \"{cheerUserLogin}\"')
        assert message is None or isinstance(message, str), f"malformed {message=}"
        assert isinstance(user, UserInterface), f"malformed {user=}"

        if self.__streamAlertsManager is None:
            return
        elif not user.isTtsEnabled():
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

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = SoundAlert.CHEER,
            twitchChannel = user.getHandle(),
            ttsEvent = TtsEvent(
                message = message,
                twitchChannel = user.getHandle(),
                userId = cheerUserId,
                userName = cheerUserLogin,
                donation = donation,
                provider = TtsProvider.DEC_TALK,
                raidInfo = None
            )
        ))
