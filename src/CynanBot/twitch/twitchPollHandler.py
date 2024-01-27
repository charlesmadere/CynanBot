from typing import List, Optional

import CynanBot.misc.utils as utils
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.tts.ttsEvent import TtsEvent
from CynanBot.tts.ttsManagerInterface import TtsManagerInterface
from CynanBot.twitch.absTwitchPollHandler import AbsTwitchPollHandler
from CynanBot.twitch.websocket.websocketDataBundle import WebsocketDataBundle
from CynanBot.twitch.websocket.websocketSubscriptionType import \
    WebsocketSubscriptionType
from CynanBot.users.userInterface import UserInterface


class TwitchPollHandler(AbsTwitchPollHandler):

    def __init__(
        self,
        timber: TimberInterface,
        ttsManager: Optional[TtsManagerInterface]
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif ttsManager is not None and not isinstance(ttsManager, TtsManagerInterface):
            raise TypeError(f'ttsManager argument is malformed: \"{ttsManager}\"')

        self.__timber: TimberInterface = timber
        self.__ttsManager: Optional[TtsManagerInterface] = ttsManager

    async def onNewPoll(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: WebsocketDataBundle
    ):
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(dataBundle, WebsocketDataBundle):
            raise TypeError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        payload = dataBundle.requirePayload()
        event = payload.getEvent()

        if event is None:
            self.__timber.log('TwitchPollHandler', f'Received a data bundle that has no event: (channel=\"{user.getHandle()}\") ({dataBundle=})')
            return

        title = event.getTitle()
        choices = event.getChoices()

        if not utils.isValidStr(title) or not isinstance(choices, List):
            self.__timber.log('TwitchPollHandler', f'Received a data bundle that is missing crucial data: (channel=\"{user.getHandle()}\") ({dataBundle=}) ({title=}) ({choices=})')
            return

        subscriptionType = payload.requireSubscription().getSubscriptionType()
        self.__timber.log('TwitchPollHandler', f'\"{user.getHandle()}\" received poll event ({title=}) ({choices=}) ({subscriptionType=})')

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

        if subscriptionType is not WebsocketSubscriptionType.CHANNEL_POLL_BEGIN:
            return
        elif self.__ttsManager is None:
            return
        elif not user.isTtsEnabled():
            return

        self.__ttsManager.submitTtsEvent(TtsEvent(
            message = f'A new poll has begun! \"{title}\"',
            twitchChannel = user.getHandle(),
            userId = userId,
            userName = user.getHandle(),
            donation = None,
            raidInfo = None
        ))
