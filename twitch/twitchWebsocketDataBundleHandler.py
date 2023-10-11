from CynanBotCommon.twitch.websocket.twitchWebsocketDataBundleListener import \
    TwitchWebsocketDataBundleListener
from CynanBotCommon.twitch.websocket.websocketDataBundle import \
    WebsocketDataBundle
from CynanBotCommon.twitch.websocket.websocketSubscriptionType import \
    WebsocketSubscriptionType
from twitch.twitchChannelPointRedemptionHandler import \
    TwitchChannelPointRedemptionHandler


class TwitchWebsocketDataBundleHandler(TwitchWebsocketDataBundleListener):

    def __init__(
        self,
        channelPointRedemptionHandler: TwitchChannelPointRedemptionHandler
    ):
        if not isinstance(channelPointRedemptionHandler, TwitchChannelPointRedemptionHandler):
            raise ValueError(f'channelPointRedemptionHandler argument is malformed: \"{channelPointRedemptionHandler}\"')

        self.__channelPointRedemptionHandler: TwitchChannelPointRedemptionHandler = channelPointRedemptionHandler

    async def onNewWebsocketDataBundle(self, dataBundle: WebsocketDataBundle):
        subscriptionType = dataBundle.getMetadata().getSubscriptionType()

        if subscriptionType is WebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION:
            await self.__channelPointRedemptionHandler.onNewChannelPointRedemption(dataBundle)

        # TODO
        pass
