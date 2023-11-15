import math
from typing import Optional

import CynanBotCommon.utils as utils
from CynanBotCommon.timber.timberInterface import TimberInterface
from CynanBotCommon.trivia.triviaGameBuilderInterface import \
    TriviaGameBuilderInterface
from CynanBotCommon.trivia.triviaGameMachineInterface import \
    TriviaGameMachineInterface
from CynanBotCommon.tts.ttsCheerDonation import TtsCheerDonation
from CynanBotCommon.tts.ttsDonation import TtsDonation
from CynanBotCommon.tts.ttsEvent import TtsEvent
from CynanBotCommon.tts.ttsManagerInterface import TtsManagerInterface
from CynanBotCommon.twitch.websocket.websocketDataBundle import \
    WebsocketDataBundle
from CynanBotCommon.users.userInterface import UserInterface
from twitch.absTwitchCheerHandler import AbsTwitchCheerHandler
from twitch.twitchChannelProvider import TwitchChannelProvider


class TwitchCheerHandler(AbsTwitchCheerHandler):

    def __init__(
        self,
        timber: TimberInterface,
        triviaGameBuilder: Optional[TriviaGameBuilderInterface],
        triviaGameMachine: Optional[TriviaGameMachineInterface],
        ttsManager: Optional[TtsManagerInterface],
        twitchChannelProvider: TwitchChannelProvider
    ):
        if not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif triviaGameBuilder is not None and not isinstance(triviaGameBuilder, TriviaGameBuilderInterface):
            raise ValueError(f'triviaGameBuilder argument is malformed: \"{triviaGameBuilder}\"')
        elif triviaGameMachine is not None and not isinstance(triviaGameMachine, TriviaGameMachineInterface):
            raise ValueError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')
        elif ttsManager is not None and not isinstance(ttsManager, TtsManagerInterface):
            raise ValueError(f'ttsManager argument is malformed: \"{ttsManager}\"')
        elif not isinstance(twitchChannelProvider, TwitchChannelProvider):
            raise ValueError(f'twitchChannelProvider argument is malformed: \"{twitchChannelProvider}\"')

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

        event = dataBundle.getPayload().getEvent()

        if event is None:
            self.__timber.log('TwitchCheerHandler', f'Received a data bundle that has no event: (channel=\"{user.getHandle()}\") ({dataBundle=})')
            return

        bits = event.getBits()
        message = event.getMessage()
        redemptionUserId = event.getUserId()
        redemptionUserLogin = event.getUserLogin()
        redemptionUserName = event.getUserName()

        if not utils.isValidInt(bits) or bits < 1 or not utils.isValidStr(redemptionUserId) or not utils.isValidStr(redemptionUserLogin) or not utils.isValidStr(redemptionUserName):
            self.__timber.log('TwitchCheerHandler', f'Received a data bundle that is missing crucial data: (channel=\"{user.getHandle()}\") ({dataBundle=}) ({bits=}) ({message=}) ({redemptionUserId=}) ({redemptionUserLogin=}) ({redemptionUserName=})')
            return

        self.__timber.log('TwitchCheerHandler', f'Received a cheer event: (channel=\"{user.getHandle()}\") ({dataBundle=}) ({bits=}) ({message=}) ({redemptionUserId=}) ({redemptionUserLogin=}) ({redemptionUserName=})')

        if user.isSuperTriviaGameEnabled():
            await self.__processSuperTriviaEvent(
                bits = bits,
                user = user
            )

        if user.isTtsEnabled():
            await self.__processTtsEvent(
                bits = bits,
                message = message,
                redemptionUserId = redemptionUserId,
                redemptionUserLogin = redemptionUserLogin,
                user = user
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
        elif not user.hasSuperTriviaCheerTriggerAmount() or bits < user.getSuperTriviaCheerTriggerAmount():
            return

        numberOfGames = math.floor(bits / user.getSuperTriviaCheerTriggerAmount())

        if numberOfGames < 1:
            return

        action = await self.__triviaGameBuilder.createNewSuperTriviaGame(
            twitchChannel = user.getHandle(),
            numberOfGames = numberOfGames
        )

        if action is not None:
            self.__triviaGameMachine.submitAction(action)

    async def __processTtsEvent(
        self,
        bits: int,
        message: Optional[str],
        redemptionUserId: str,
        redemptionUserLogin: str,
        user: UserInterface
    ):
        if not utils.isValidInt(bits):
            raise ValueError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif message is not None and not isinstance(message, str):
            raise ValueError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(redemptionUserId):
            raise ValueError(f'redemptionUserId argument is malformed: \"{redemptionUserId}\"')
        elif not utils.isValidStr(redemptionUserLogin):
            raise ValueError(f'redemptionUserLogin argument is malformed: \"{redemptionUserLogin}\"')
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
            userId = redemptionUserId,
            userName = redemptionUserLogin,
            donation = donation,
            raidInfo = None
        ))
