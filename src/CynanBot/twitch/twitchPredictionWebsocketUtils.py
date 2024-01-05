from CynanBot.twitch.twitchPredictionWebsocketUtilsInterface import \
    TwitchPredictionWebsocketUtilsInterface
from CynanBot.twitch.websocket.websocketSubscriptionType import \
    WebsocketSubscriptionType


class TwitchPredictionWebsocketUtils(TwitchPredictionWebsocketUtilsInterface):

    async def websocketSubscriptionTypeToString(
        self,
        subscriptionType: WebsocketSubscriptionType
    ) -> str:
        if not isinstance(subscriptionType, WebsocketSubscriptionType):
            raise ValueError(f'subscriptionType argument is malformed: \"{subscriptionType}\"')

        if subscriptionType is WebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN:
            return 'prediction_begin'
        elif subscriptionType is WebsocketSubscriptionType.CHANNEL_PREDICTION_END:
            return 'prediction_end'
        elif subscriptionType is WebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK:
            return 'prediction_lock'
        elif subscriptionType is WebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS:
            return 'prediction_progress'
        else:
            raise ValueError(f'Can\'t convert the given WebsocketSubscriptionType (\"{subscriptionType}\") into a string!')
