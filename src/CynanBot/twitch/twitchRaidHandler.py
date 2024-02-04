from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.soundPlayerManager.soundAlert import SoundAlert
from CynanBot.streamAlertsManager.streamAlert import StreamAlert
from CynanBot.streamAlertsManager.streamAlertsManagerInterface import \
    StreamAlertsManagerInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.tts.ttsEvent import TtsEvent
from CynanBot.tts.ttsProvider import TtsProvider
from CynanBot.tts.ttsRaidInfo import TtsRaidInfo
from CynanBot.twitch.absTwitchRaidHandler import AbsTwitchRaidHandler
from CynanBot.twitch.websocket.websocketDataBundle import WebsocketDataBundle
from CynanBot.users.userInterface import UserInterface


class TwitchRaidHandler(AbsTwitchRaidHandler):

    def __init__(
        self,
        streamAlertsManager: Optional[StreamAlertsManagerInterface],
        timber: TimberInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif streamAlertsManager is not None and not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')

        self.__timber: TimberInterface = timber
        self.__streamAlertsManager: Optional[StreamAlertsManagerInterface] = streamAlertsManager

    async def onNewRaid(
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

        event = dataBundle.requirePayload().getEvent()

        if event is None:
            self.__timber.log('TwitchRaidHandler', f'Received a data bundle that has no event: (channel=\"{user.getHandle()}\") ({dataBundle=})')
            return

        fromUserId = event.getFromBroadcasterUserId()
        fromUserLogin = event.getFromBroadcasterUserLogin()
        fromUserName = event.getFromBroadcasterUserName()
        toUserId = event.getToBroadcasterUserId()
        toUserLogin = event.getToBroadcasterUserLogin()
        toUserName = event.getToBroadcasterUserName()
        viewers = event.getViewers()

        if not utils.isValidStr(fromUserId) or not utils.isValidStr(fromUserLogin) or not utils.isValidStr(fromUserName) or not utils.isValidStr(toUserId) or not utils.isValidStr(toUserLogin) or not utils.isValidStr(toUserName) or not utils.isValidInt(viewers):
            self.__timber.log('TwitchRaidHandler', f'Received a data bundle that is missing crucial data: (channel=\"{user.getHandle()}\") ({dataBundle=}) ({fromUserId=}) ({fromUserLogin=}) ({fromUserName=}) ({toUserId=}) ({toUserLogin=}) ({toUserName=}) ({viewers=})')
            return

        self.__timber.log('TwitchRaidHandler', f'\"{user.getHandle()}\" received raid of {viewers} from \"{fromUserLogin}\"')

        await self.__processTtsEvent(
            viewers = viewers,
            userId = fromUserId,
            fromUserName = fromUserName,
            user = user
        )

    async def __processTtsEvent(
        self,
        viewers: int,
        userId: str,
        fromUserName: str,
        user: UserInterface
    ):
        if not utils.isValidInt(viewers):
            raise TypeError(f'viewers argument is malformed: \"{viewers}\"')
        elif viewers < 0 or viewers > utils.getIntMaxSafeSize():
            raise ValueError(f'viewers argument is out of bounds: {viewers}')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(fromUserName):
            raise TypeError(f'fromUserName argument is malformed: \"{fromUserName}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        if self.__streamAlertsManager is None:
            return
        elif not user.isTtsEnabled():
            return
        elif viewers < 1:
            return

        raidInfo = TtsRaidInfo(viewers = viewers)

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = SoundAlert.RAID,
            twitchChannel = user.getHandle(),
            ttsEvent = TtsEvent(
                message = f'Hello everyone from {fromUserName}\'s stream, welcome in. Thanks for the raid of {viewers}!',
                twitchChannel = user.getHandle(),
                userId = userId,
                userName = fromUserName,
                donation = None,
                provider = TtsProvider.DEC_TALK,
                raidInfo = raidInfo
            )
        ))
