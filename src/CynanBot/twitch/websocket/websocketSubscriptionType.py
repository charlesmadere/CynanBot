from enum import Enum, auto
from typing import Optional

import CynanBot.misc.utils as utils


class WebsocketSubscriptionType(Enum):

    CHANNEL_POINTS_REDEMPTION = auto()
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
            return WebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION
        elif text == 'channel.cheer':
            return WebsocketSubscriptionType.CHEER
        elif text == 'channel.prediction.begin':
            return WebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN
        elif text == 'channel.prediction.end':
            return WebsocketSubscriptionType.CHANNEL_PREDICTION_END
        elif text == 'channel.prediction.lock':
            return WebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK
        elif text == 'channel.prediction.progress':
            return WebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS
        elif text == 'channel.update':
            return WebsocketSubscriptionType.CHANNEL_UPDATE
        elif text == 'channel.follow':
            return WebsocketSubscriptionType.FOLLOW
        elif text == 'channel.raid':
            return WebsocketSubscriptionType.RAID
        elif text == 'channel.subscribe':
            return WebsocketSubscriptionType.SUBSCRIBE
        elif text == 'channel.subscription.gift':
            return WebsocketSubscriptionType.SUBSCRIPTION_GIFT
        elif text == 'channel.subscription.message':
            return WebsocketSubscriptionType.SUBSCRIPTION_MESSAGE
        else:
            return None

    def getVersion(self) -> str:
        if self is WebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION:
            return '1'
        elif self is WebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN:
            return '1'
        elif self is WebsocketSubscriptionType.CHANNEL_PREDICTION_END:
            return '1'
        elif self is WebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK:
            return '1'
        elif self is WebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS:
            return '1'
        elif self is WebsocketSubscriptionType.CHANNEL_UPDATE:
            return '2'
        elif self is WebsocketSubscriptionType.CHEER:
            return '1'
        elif self is WebsocketSubscriptionType.FOLLOW:
            return '2'
        elif self is WebsocketSubscriptionType.RAID:
            return '1'
        elif self is WebsocketSubscriptionType.SUBSCRIBE:
            return '1'
        elif self is WebsocketSubscriptionType.SUBSCRIPTION_GIFT:
            return '1'
        elif self is WebsocketSubscriptionType.SUBSCRIPTION_MESSAGE:
            return '1'
        else:
            raise RuntimeError(f'unknown WebsocketSubscriptionType: \"{self}\"')

    def toStr(self) -> str:
        if self is WebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION:
            return 'channel.channel_points_custom_reward_redemption.add'
        elif self is WebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN:
            return 'channel.prediction.begin'
        elif self is WebsocketSubscriptionType.CHANNEL_PREDICTION_END:
            return 'channel.prediction.end'
        elif self is WebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK:
            return 'channel.prediction.lock'
        elif self is WebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS:
            return 'channel.prediction.progress'
        elif self is WebsocketSubscriptionType.CHANNEL_UPDATE:
            return 'channel.update'
        elif self is WebsocketSubscriptionType.CHEER:
            return 'channel.cheer'
        elif self is WebsocketSubscriptionType.FOLLOW:
            return 'channel.follow'
        elif self is WebsocketSubscriptionType.RAID:
            return 'channel.raid'
        elif self is WebsocketSubscriptionType.SUBSCRIBE:
            return 'channel.subscribe'
        elif self is WebsocketSubscriptionType.SUBSCRIPTION_GIFT:
            return 'channel.subscription.gift'
        elif self is WebsocketSubscriptionType.SUBSCRIPTION_MESSAGE:
            return 'channel.subscription.message'
        else:
            raise RuntimeError(f'unknown WebsocketSubscriptionType: \"{self}\"')
