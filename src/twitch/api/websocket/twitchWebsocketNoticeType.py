from enum import Enum, auto

from ....misc import utils as utils


class TwitchWebsocketNoticeType(Enum):

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
    def fromStr(cls, text: str | None):
        if not utils.isValidStr(text):
            return None

        text = text.lower()

        match text:
            case 'announcement': return TwitchWebsocketNoticeType.ANNOUNCEMENT
            case 'bits_badge_tier': return TwitchWebsocketNoticeType.BITS_BADGE_TIER
            case 'charity_donation': return TwitchWebsocketNoticeType.CHARITY_DONATION
            case 'community_sub_gift': return TwitchWebsocketNoticeType.COMMUNITY_SUB_GIFT
            case 'gift_paid_upgrade':  return TwitchWebsocketNoticeType.GIFT_PAID_UPGRADE
            case 'pay_it_forward': return TwitchWebsocketNoticeType.PAY_IT_FORWARD
            case 'prime_paid_upgrade': return TwitchWebsocketNoticeType.PRIME_PAID_UPGRADE
            case 'raid': return TwitchWebsocketNoticeType.RAID
            case 'resub': return TwitchWebsocketNoticeType.RE_SUB
            case 'sub': return TwitchWebsocketNoticeType.SUB
            case 'sub_gift': return TwitchWebsocketNoticeType.SUB_GIFT
            case 'unraid': return TwitchWebsocketNoticeType.UN_RAID
            case _: return None
