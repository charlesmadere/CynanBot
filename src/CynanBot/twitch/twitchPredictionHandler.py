from typing import List, Optional

import CynanBotCommon.utils as utils
from CynanBotCommon.timber.timberInterface import TimberInterface
from CynanBotCommon.tts.ttsEvent import TtsEvent
from CynanBotCommon.tts.ttsManagerInterface import TtsManagerInterface
from CynanBotCommon.twitch.websocket.websocketDataBundle import \
    WebsocketDataBundle
from CynanBotCommon.twitch.websocket.websocketSubscriptionType import \
    WebsocketSubscriptionType
from CynanBotCommon.users.userInterface import UserInterface
from twitch.absTwitchPredictionHandler import AbsTwitchPredictionHandler


class TwitchPredictionHandler(AbsTwitchPredictionHandler):

    def __init__(
        self,
        timber: TimberInterface,
        ttsManager: Optional[TtsManagerInterface]
    ):
        if not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif ttsManager is not None and not isinstance(ttsManager, TtsManagerInterface):
            raise ValueError(f'ttsManager argument is malformed: \"{ttsManager}\"')

        self.__timber: TimberInterface = timber
        self.__ttsManager: Optional[TtsManagerInterface] = ttsManager

    async def onNewPrediction(
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

        payload = dataBundle.getPayload()
        event = payload.getEvent()

        if event is None:
            self.__timber.log('TwitchPredictionHandler', f'Received a data bundle that has no event: (channel=\"{user.getHandle()}\") ({dataBundle=})')
            return

        title = event.getTitle()
        outcomes = event.getOutcomes()
        subscriptionType = payload.getSubscription().getSubscriptionType()

        if not utils.isValidStr(title) or not isinstance(outcomes, List):
            self.__timber.log('TwitchPredictionHandler', f'Received a data bundle that is missing crucial data: (channel=\"{user.getHandle()}\") ({dataBundle=}) ({title=})')
            return

        self.__timber.log('TwitchPredictionHandler', f'\"{user.getHandle()}\" received prediction event ({title=}) ({outcomes=})')

        await self.__processTtsEvent(
            title = title,
            userId = userId,
            user = user,
            subscriptionType = subscriptionType
        )

    async def __processTtsEvent(
        self,
        title: str,
        userId: str,
        user: UserInterface,
        subscriptionType: WebsocketSubscriptionType
    ):
        if not utils.isValidStr(title):
            raise ValueError(f'title argument is malformed: \"{title}\"')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not isinstance(user, UserInterface):
            raise ValueError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(subscriptionType, WebsocketSubscriptionType):
            raise ValueError(f'subscriptionType argument is malformed: \"{subscriptionType}\"')

        if subscriptionType is not WebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN:
            return
        elif self.__ttsManager is None:
            return
        elif not user.isTtsEnabled():
            return

        self.__ttsManager.submitTtsEvent(TtsEvent(
            message = f'A new prediction has begun! \"{title}\"',
            twitchChannel = user.getHandle(),
            userId = userId,
            userName = user.getHandle(),
            donation = None,
            raidInfo = None
        ))
