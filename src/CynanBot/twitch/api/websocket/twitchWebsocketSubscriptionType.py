from enum import Enum, auto
from typing import Optional

import CynanBot.misc.utils as utils


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
    CHEER = auto()
    FOLLOW = auto()
    RAID = auto()
    SUBSCRIBE = auto()
    SUBSCRIPTION_GIFT = auto()
    SUBSCRIPTION_MESSAGE = auto()

    @classmethod
    def fromStr(cls, text: Optional[str]):
        if not utils.isValidStr(text):
            return None

        text = text.lower()

        if text == 'channel.channel_points_custom_reward_redemption.add':
            return TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION
        elif text == 'channel.poll.begin':
            return TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN
        elif text == 'channel.poll.end':
            return TwitchWebsocketSubscriptionType.CHANNEL_POLL_END
        elif text == 'channel.poll.progress':
            return TwitchWebsocketSubscriptionType.CHANNEL_POLL_PROGRESS
        elif text == 'channel.prediction.begin':
            return TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN
        elif text == 'channel.prediction.end':
            return TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END
        elif text == 'channel.prediction.lock':
            return TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK
        elif text == 'channel.prediction.progress':
            return TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS
        elif text == 'channel.update':
            return TwitchWebsocketSubscriptionType.CHANNEL_UPDATE
        elif text == 'channel.cheer':
            return TwitchWebsocketSubscriptionType.CHEER
        elif text == 'channel.follow':
            return TwitchWebsocketSubscriptionType.FOLLOW
        elif text == 'channel.raid':
            return TwitchWebsocketSubscriptionType.RAID
        elif text == 'channel.subscribe':
            return TwitchWebsocketSubscriptionType.SUBSCRIBE
        elif text == 'channel.subscription.gift':
            return TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT
        elif text == 'channel.subscription.message':
            return TwitchWebsocketSubscriptionType.SUBSCRIPTION_MESSAGE
        else:
            return None

    def getVersion(self) -> str:
        if self is TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION:
            return '1'
        elif self is TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN:
            return '1'
        elif self is TwitchWebsocketSubscriptionType.CHANNEL_POLL_END:
            return '1'
        elif self is TwitchWebsocketSubscriptionType.CHANNEL_POLL_PROGRESS:
            return '1'
        elif self is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN:
            return '1'
        elif self is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END:
            return '1'
        elif self is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK:
            return '1'
        elif self is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS:
            return '1'
        elif self is TwitchWebsocketSubscriptionType.CHANNEL_UPDATE:
            return '2'
        elif self is TwitchWebsocketSubscriptionType.CHEER:
            return '1'
        elif self is TwitchWebsocketSubscriptionType.FOLLOW:
            return '2'
        elif self is TwitchWebsocketSubscriptionType.RAID:
            return '1'
        elif self is TwitchWebsocketSubscriptionType.SUBSCRIBE:
            return '1'
        elif self is TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT:
            return '1'
        elif self is TwitchWebsocketSubscriptionType.SUBSCRIPTION_MESSAGE:
            return '1'
        else:
            raise RuntimeError(f'unknown WebsocketSubscriptionType: \"{self}\"')

    def toStr(self) -> str:
        if self is TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION:
            return 'channel.channel_points_custom_reward_redemption.add'
        elif self is TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN:
            return 'channel.poll.begin'
        elif self is TwitchWebsocketSubscriptionType.CHANNEL_POLL_END:
            return 'channel.poll.end'
        elif self is TwitchWebsocketSubscriptionType.CHANNEL_POLL_PROGRESS:
            return 'channel.poll.progress'
        elif self is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN:
            return 'channel.prediction.begin'
        elif self is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END:
            return 'channel.prediction.end'
        elif self is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK:
            return 'channel.prediction.lock'
        elif self is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS:
            return 'channel.prediction.progress'
        elif self is TwitchWebsocketSubscriptionType.CHANNEL_UPDATE:
            return 'channel.update'
        elif self is TwitchWebsocketSubscriptionType.CHEER:
            return 'channel.cheer'
        elif self is TwitchWebsocketSubscriptionType.FOLLOW:
            return 'channel.follow'
        elif self is TwitchWebsocketSubscriptionType.RAID:
            return 'channel.raid'
        elif self is TwitchWebsocketSubscriptionType.SUBSCRIBE:
            return 'channel.subscribe'
        elif self is TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT:
            return 'channel.subscription.gift'
        elif self is TwitchWebsocketSubscriptionType.SUBSCRIPTION_MESSAGE:
            return 'channel.subscription.message'
        else:
            raise RuntimeError(f'unknown WebsocketSubscriptionType: \"{self}\"')
