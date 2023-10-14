from CynanBotCommon.timber.timberInterface import TimberInterface
from CynanBotCommon.twitch.websocket.websocketDataBundle import \
    WebsocketDataBundle
from CynanBotCommon.twitch.websocket.websocketSubscriptionType import \
    WebsocketSubscriptionType


class TwitchChannelPointRedemptionHandler():

    def __init__(
        self,
        timber: TimberInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

    async def onNewChannelPointRedemption(self, dataBundle: WebsocketDataBundle):
        if not isinstance(dataBundle, WebsocketDataBundle):
            raise ValueError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        # TODO
        pass
