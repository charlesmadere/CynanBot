from enum import Enum, auto


class TwitchWebsocketSubscriptionType(Enum):

    CHANNEL_CHAT_MESSAGE = auto()
    CHANNEL_CHEER = auto()
    CHANNEL_HYPE_TRAIN_BEGIN = auto()
    CHANNEL_HYPE_TRAIN_END = auto()
    CHANNEL_HYPE_TRAIN_PROGRESS = auto()
    CHANNEL_POINTS_REDEMPTION = auto()
    CHANNEL_POLL_BEGIN = auto()
    CHANNEL_POLL_END = auto()
    CHANNEL_POLL_PROGRESS = auto()
    CHANNEL_PREDICTION_BEGIN = auto()
    CHANNEL_PREDICTION_END = auto()
    CHANNEL_PREDICTION_LOCK = auto()
    CHANNEL_PREDICTION_PROGRESS = auto()
    CHANNEL_UPDATE = auto()
    FOLLOW = auto()
    RAID = auto()
    STREAM_OFFLINE = auto()
    STREAM_ONLINE = auto()
    SUBSCRIBE = auto()
    SUBSCRIPTION_GIFT = auto()
    SUBSCRIPTION_MESSAGE = auto()
    USER_UPDATE = auto()

    @property
    def version(self) -> str:
        match self:
            case TwitchWebsocketSubscriptionType.CHANNEL_CHAT_MESSAGE: return '1'
            case TwitchWebsocketSubscriptionType.CHANNEL_CHEER: return '1'
            case TwitchWebsocketSubscriptionType.CHANNEL_HYPE_TRAIN_BEGIN: return '2'
            case TwitchWebsocketSubscriptionType.CHANNEL_HYPE_TRAIN_END: return '2'
            case TwitchWebsocketSubscriptionType.CHANNEL_HYPE_TRAIN_PROGRESS: return '2'
            case TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION: return '1'
            case TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN: return '1'
            case TwitchWebsocketSubscriptionType.CHANNEL_POLL_END: return '1'
            case TwitchWebsocketSubscriptionType.CHANNEL_POLL_PROGRESS: return '1'
            case TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN: return '1'
            case TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END: return '1'
            case TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK: return '1'
            case TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS: return '1'
            case TwitchWebsocketSubscriptionType.CHANNEL_UPDATE: return '2'
            case TwitchWebsocketSubscriptionType.FOLLOW: return '2'
            case TwitchWebsocketSubscriptionType.RAID: return '1'
            case TwitchWebsocketSubscriptionType.STREAM_OFFLINE: return '1'
            case TwitchWebsocketSubscriptionType.STREAM_ONLINE: return '1'
            case TwitchWebsocketSubscriptionType.SUBSCRIBE: return '1'
            case TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT: return '1'
            case TwitchWebsocketSubscriptionType.SUBSCRIPTION_MESSAGE: return '1'
            case TwitchWebsocketSubscriptionType.USER_UPDATE: return '1'
            case _: raise RuntimeError(f'unknown TwitchWebsocketSubscriptionType: \"{self}\"')
