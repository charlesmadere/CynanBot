from enum import Enum, auto
from typing import Optional

import CynanBot.misc.utils as utils


class WebsocketNoticeType(Enum):

    ANNOUNCEMENT = auto()
    BITS_BADGE_TIER = auto()
    CHARITY_DONATION = auto()
    COMMUNITY_SUB_GIFT = auto()
    GIFT_PAID_UPGRADE = auto()
    PAY_IT_FORWARD = auto()
    PRIME_PAID_UPGRADE = auto()
    RAID = auto()
    RE_SUB = auto()
    SUB = auto()
    SUB_GIFT = auto()
    UN_RAID = auto()

    @classmethod
    def fromStr(cls, text: Optional[str]):
        if not utils.isValidStr(text):
            return None

        text = text.lower()

        if text == 'announcement':
            return WebsocketNoticeType.ANNOUNCEMENT
        elif text == 'bits_badge_tier':
            return WebsocketNoticeType.BITS_BADGE_TIER
        elif text == 'charity_donation':
            return WebsocketNoticeType.CHARITY_DONATION
        elif text == 'community_sub_gift':
            return WebsocketNoticeType.COMMUNITY_SUB_GIFT
        elif text == 'gift_paid_upgrade':
            return WebsocketNoticeType.GIFT_PAID_UPGRADE
        elif text == 'pay_it_forward':
            return WebsocketNoticeType.PAY_IT_FORWARD
        elif text == 'prime_paid_upgrade':
            return WebsocketNoticeType.PRIME_PAID_UPGRADE
        elif text == 'raid':
            return WebsocketNoticeType.RAID
        elif text in ('resub', 're_sub'):
            return WebsocketNoticeType.RE_SUB
        elif text == 'sub':
            return WebsocketNoticeType.SUB
        elif text == 'sub_gift':
            return WebsocketNoticeType.SUB_GIFT
        elif text in ('unraid', 'un_raid'):
            return WebsocketNoticeType.UN_RAID
        else:
            return None
