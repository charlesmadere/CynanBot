from CynanBotCommon.twitch.websocket.twitchWebsocketDataBundleListener import \
    TwitchWebsocketDataBundleListener
from CynanBotCommon.twitch.websocket.websocketDataBundle import \
    WebsocketDataBundle
from CynanBotCommon.twitch.websocket.websocketSubscriptionType import \
    WebsocketSubscriptionType
from twitch.twitchChannelPointRedemptionHandler import \
    TwitchChannelPointRedemptionHandler
from twitch.twitchSubscriptionHandler import TwitchSubscriptionHandler


class TwitchWebsocketDataBundleHandler(TwitchWebsocketDataBundleListener):

    def __init__(
        self,
        channelPointRedemptionHandler: TwitchChannelPointRedemptionHandler,
        subscriptionHandler: TwitchSubscriptionHandler
    ):
        if not isinstance(channelPointRedemptionHandler, TwitchChannelPointRedemptionHandler):
            raise ValueError(f'channelPointRedemptionHandler argument is malformed: \"{channelPointRedemptionHandler}\"')
        elif not isinstance(subscriptionHandler, TwitchSubscriptionHandler):
            raise ValueError(f'subscriptionHandler argument is malformed: \"{subscriptionHandler}\"')

        self.__channelPointRedemptionHandler: TwitchChannelPointRedemptionHandler = channelPointRedemptionHandler
        self.__subscriptionHandler: TwitchSubscriptionHandler = subscriptionHandler

    async def onNewWebsocketDataBundle(self, dataBundle: WebsocketDataBundle):
        subscriptionType = dataBundle.getMetadata().getSubscriptionType()

        if subscriptionType is WebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION:
            await self.__channelPointRedemptionHandler.onNewChannelPointRedemption(dataBundle)

        # TODO
        pass
