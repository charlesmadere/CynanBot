from enum import Enum, auto

from ....misc import utils as utils


class TwitchWebsocketSubscriptionType(Enum):

    CHANNEL_POINTS_REDEMPTION = auto()
    CHANNEL_POLL_BEGIN = auto()
    CHANNEL_POLL_END = auto()
    CHANNEL_POLL_PROGRESS = auto()
    CHANNEL_PREDICTION_BEGIN = auto()
    CHANNEL_PREDICTION_END = auto()
    CHANNEL_PREDICTION_LOCK = auto()
    CHANNEL_PREDICTION_PROGRESS = auto()
    CHANNEL_UPDATE = auto()
    CHAT_MESSAGE = auto()
    CHEER = auto()
    FOLLOW = auto()
    RAID = auto()
    SUBSCRIBE = auto()
    SUBSCRIPTION_GIFT = auto()
    SUBSCRIPTION_MESSAGE = auto()

    @classmethod
    def fromStr(cls, text: str | None):
        if not utils.isValidStr(text):
            return None

        text = text.lower()

        match text:
            case 'channel.channel_points_custom_reward_redemption.add':
                return TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION
            case 'channel.poll.begin':
                return TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN
            case 'channel.poll.end':
                return TwitchWebsocketSubscriptionType.CHANNEL_POLL_END
            case 'channel.poll.progress':
                return TwitchWebsocketSubscriptionType.CHANNEL_POLL_PROGRESS
            case 'channel.prediction.begin':
                return TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN
            case 'channel.prediction.end':
                return TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END
            case 'channel.prediction.lock':
                return TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK
            case 'channel.prediction.progress':
                return TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS
            case 'channel.update':
                return TwitchWebsocketSubscriptionType.CHANNEL_UPDATE
            case 'channel.chat.message':
                return TwitchWebsocketSubscriptionType.CHAT_MESSAGE
            case 'channel.cheer':
                return TwitchWebsocketSubscriptionType.CHEER
            case 'channel.follow':
                return TwitchWebsocketSubscriptionType.FOLLOW
            case 'channel.raid':
                return TwitchWebsocketSubscriptionType.RAID
            case 'channel.subscribe':
                return TwitchWebsocketSubscriptionType.SUBSCRIBE
            case 'channel.subscription.gift':
                return TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT
            case 'channel.subscription.message':
                return TwitchWebsocketSubscriptionType.SUBSCRIPTION_MESSAGE
            case _:
                return None

    def getVersion(self) -> str:
        match self:
            case TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION: return '1'
            case TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN: return '1'
            case TwitchWebsocketSubscriptionType.CHANNEL_POLL_END: return '1'
            case TwitchWebsocketSubscriptionType.CHANNEL_POLL_PROGRESS: return '1'
            case TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN: return '1'
            case TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END: return '1'
            case TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK: return '1'
            case TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS: return '1'
            case TwitchWebsocketSubscriptionType.CHANNEL_UPDATE: return '2'
            case TwitchWebsocketSubscriptionType.CHAT_MESSAGE: return '1'
            case TwitchWebsocketSubscriptionType.CHEER: return '1'
            case TwitchWebsocketSubscriptionType.FOLLOW: return '2'
            case TwitchWebsocketSubscriptionType.RAID: return '1'
            case TwitchWebsocketSubscriptionType.SUBSCRIBE: return '1'
            case TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT: return '1'
            case TwitchWebsocketSubscriptionType.SUBSCRIPTION_MESSAGE: return '1'
            case _: raise RuntimeError(f'unknown TwitchWebsocketSubscriptionType: \"{self}\"')

    def toStr(self) -> str:
        match self:
            case TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION:
                return 'channel.channel_points_custom_reward_redemption.add'
            case TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN:
                return 'channel.poll.begin'
            case TwitchWebsocketSubscriptionType.CHANNEL_POLL_END:
                return 'channel.poll.end'
            case TwitchWebsocketSubscriptionType.CHANNEL_POLL_PROGRESS:
                return 'channel.poll.progress'
            case TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN:
                return 'channel.prediction.begin'
            case TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END:
                return 'channel.prediction.end'
            case TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK:
                return 'channel.prediction.lock'
            case TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS:
                return 'channel.prediction.progress'
            case TwitchWebsocketSubscriptionType.CHANNEL_UPDATE:
                return 'channel.update'
            case TwitchWebsocketSubscriptionType.CHAT_MESSAGE:
                return 'channel.chat.message'
            case TwitchWebsocketSubscriptionType.CHEER:
                return 'channel.cheer'
            case TwitchWebsocketSubscriptionType.FOLLOW:
                return 'channel.follow'
            case TwitchWebsocketSubscriptionType.RAID:
                return 'channel.raid'
            case TwitchWebsocketSubscriptionType.SUBSCRIBE:
                return 'channel.subscribe'
            case TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT:
                return 'channel.subscription.gift'
            case TwitchWebsocketSubscriptionType.SUBSCRIPTION_MESSAGE:
                return 'channel.subscription.message'
            case _:
                raise RuntimeError(f'unknown TwitchWebsocketSubscriptionType: \"{self}\"')
