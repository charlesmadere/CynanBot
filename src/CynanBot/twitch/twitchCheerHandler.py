import math
from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.cheerActions.cheerActionHelperInterface import \
    CheerActionHelperInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.triviaGameBuilderInterface import \
    TriviaGameBuilderInterface
from CynanBot.trivia.triviaGameMachineInterface import \
    TriviaGameMachineInterface
from CynanBot.tts.ttsCheerDonation import TtsCheerDonation
from CynanBot.tts.ttsDonation import TtsDonation
from CynanBot.tts.ttsEvent import TtsEvent
from CynanBot.tts.ttsManagerInterface import TtsManagerInterface
from CynanBot.twitch.absTwitchCheerHandler import AbsTwitchCheerHandler
from CynanBot.twitch.configuration.twitchChannelProvider import \
    TwitchChannelProvider
from CynanBot.twitch.websocket.websocketDataBundle import WebsocketDataBundle
from CynanBot.users.userInterface import UserInterface


class TwitchCheerHandler(AbsTwitchCheerHandler):

    def __init__(
        self,
        cheerActionHelper: Optional[CheerActionHelperInterface],
        timber: TimberInterface,
        triviaGameBuilder: Optional[TriviaGameBuilderInterface],
        triviaGameMachine: Optional[TriviaGameMachineInterface],
        ttsManager: Optional[TtsManagerInterface],
        twitchChannelProvider: TwitchChannelProvider
    ):
        if cheerActionHelper is not None and not isinstance(cheerActionHelper, CheerActionHelperInterface):
            raise ValueError(f'cheerActionHelper argument is malformed: \"{cheerActionHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif triviaGameBuilder is not None and not isinstance(triviaGameBuilder, TriviaGameBuilderInterface):
            raise ValueError(f'triviaGameBuilder argument is malformed: \"{triviaGameBuilder}\"')
        elif triviaGameMachine is not None and not isinstance(triviaGameMachine, TriviaGameMachineInterface):
            raise ValueError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')
        elif ttsManager is not None and not isinstance(ttsManager, TtsManagerInterface):
            raise ValueError(f'ttsManager argument is malformed: \"{ttsManager}\"')
        elif not isinstance(twitchChannelProvider, TwitchChannelProvider):
            raise ValueError(f'twitchChannelProvider argument is malformed: \"{twitchChannelProvider}\"')

        self.__cheerActionHelper: Optional[CheerActionHelperInterface] = cheerActionHelper
        self.__timber: TimberInterface = timber
        self.__triviaGameBuilder: Optional[TriviaGameBuilderInterface] = triviaGameBuilder
        self.__triviaGameMachine: Optional[TriviaGameMachineInterface] = triviaGameMachine
        self.__ttsManager: Optional[TtsManagerInterface] = ttsManager
        self.__twitchChannelProvider: TwitchChannelProvider = twitchChannelProvider

    async def onNewCheer(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: WebsocketDataBundle
    ):
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not isinstance(user, UserInterface):
            raise ValueError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(dataBundle, WebsocketDataBundle):
            raise ValueError(f'dataBundle argument is malformed: \"{dataBundle}\"')

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

        if user.isTtsEnabled():
            await self.__processTtsEvent(
                bits = bits,
                message = message,
                cheerUserId = cheerUserId,
                cheerUserLogin = cheerUserLogin,
                user = user
            )

        if user.areCheerActionsEnabled():
            await self.__processCheerAction(
                bits = bits,
                cheerUserId = cheerUserId,
                cheerUserLogin = cheerUserLogin,
                message = message,
                user = user
            )

    async def __processCheerAction(
        self,
        bits: int,
        cheerUserId: str,
        cheerUserLogin: str,
        message: Optional[str],
        user: UserInterface
    ):
        if not utils.isValidInt(bits):
            raise ValueError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif not utils.isValidStr(cheerUserId):
            raise ValueError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserLogin):
            raise ValueError(f'cheerUserLogin argument is malformed: \"{cheerUserLogin}\"')
        elif message is not None and not isinstance(message, str):
            raise ValueError(f'message argument is malformed: \"{message}\"')
        elif not isinstance(user, UserInterface):
            raise ValueError(f'user argument is malformed: \"{user}\"')

        if not utils.isValidStr(message) or self.__cheerActionHelper is None:
            return

        await self.__cheerActionHelper.handleCheerAction(
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
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif not isinstance(user, UserInterface):
            raise ValueError(f'user argument is malformed: \"{user}\"')

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
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif not utils.isValidStr(cheerUserId):
            raise ValueError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserLogin):
            raise ValueError(f'cheerUserLogin argument is malformed: \"{cheerUserLogin}\"')
        elif message is not None and not isinstance(message, str):
            raise ValueError(f'message argument is malformed: \"{message}\"')
        elif not isinstance(user, UserInterface):
            raise ValueError(f'user argument is malformed: \"{user}\"')

        if self.__ttsManager is None:
            return
        elif not user.isTtsEnabled():
            return
        elif not user.hasMinimumTtsCheerAmount() or bits < user.getMinimumTtsCheerAmount():
            return

        donation: TtsDonation = TtsCheerDonation(bits = bits)

        self.__ttsManager.submitTtsEvent(TtsEvent(
            message = message,
            twitchChannel = user.getHandle(),
            userId = cheerUserId,
            userName = cheerUserLogin,
            donation = donation,
            raidInfo = None
        ))
