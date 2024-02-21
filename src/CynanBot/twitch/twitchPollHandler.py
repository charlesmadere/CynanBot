from typing import List, Optional

import CynanBot.misc.utils as utils
from CynanBot.streamAlertsManager.streamAlert import StreamAlert
from CynanBot.streamAlertsManager.streamAlertsManagerInterface import \
    StreamAlertsManagerInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.tts.ttsEvent import TtsEvent
from CynanBot.tts.ttsProvider import TtsProvider
from CynanBot.twitch.absTwitchPollHandler import AbsTwitchPollHandler
from CynanBot.twitch.api.websocket.twitchWebsocketDataBundle import \
    TwitchWebsocketDataBundle
from CynanBot.twitch.api.websocket.twitchWebsocketSubscriptionType import \
    TwitchWebsocketSubscriptionType
from CynanBot.users.userInterface import UserInterface


class TwitchPollHandler(AbsTwitchPollHandler):

    def __init__(
        self,
        streamAlertsManager: Optional[StreamAlertsManagerInterface],
        timber: TimberInterface
    ):
        assert streamAlertsManager is None or isinstance(streamAlertsManager, StreamAlertsManagerInterface), f"malformed {streamAlertsManager=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"

        self.__streamAlertsManager: Optional[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: TimberInterface = timber

    async def onNewPoll(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle
    ):
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        assert isinstance(user, UserInterface), f"malformed {user=}"
        assert isinstance(dataBundle, TwitchWebsocketDataBundle), f"malformed {dataBundle=}"

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
        subscriptionType: TwitchWebsocketSubscriptionType
    ):
        if not utils.isValidStr(title):
            raise ValueError(f'title argument is malformed: \"{title}\"')
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        assert isinstance(user, UserInterface), f"malformed {user=}"
        assert isinstance(subscriptionType, TwitchWebsocketSubscriptionType), f"malformed {subscriptionType=}"

        if subscriptionType is not TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN:
            return
        elif self.__streamAlertsManager is None:
            return
        elif not user.isTtsEnabled():
            return

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = None,
            twitchChannel = user.getHandle(),
            ttsEvent = TtsEvent(
                message = f'A new poll has begun! \"{title}\"',
                twitchChannel = user.getHandle(),
                userId = userId,
                userName = user.getHandle(),
                donation = None,
                provider = TtsProvider.DEC_TALK,
                raidInfo = None
            )
        ))
