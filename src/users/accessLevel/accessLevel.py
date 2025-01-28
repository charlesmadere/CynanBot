from enum import Enum, auto

class AccessLevel(Enum):

    ANY = auto()
    EDITOR = auto()
    FOLLOWER = auto()
    MODERATOR = auto()
    STREAMER = auto()
    SUBSCRIBER = auto()
    T1 = auto()
    T2 = auto()
    T3 = auto()
    VIP = auto()

    @property
    def accessLevel(self) -> str:
        match self:
            case AccessLevel.ANY: return 'any'
            case AccessLevel.EDITOR: return 'editor'
            case AccessLevel.FOLLOWER: return 'follower'
            case AccessLevel.MODERATOR: return 'moderator'
            case AccessLevel.STREAMER: return 'streamer'
            case AccessLevel.SUBSCRIBER: return 'subscriber'
            case AccessLevel.T1: return 't1'
            case AccessLevel.T2: return 't2'
            case AccessLevel.T3: return 't3'
            case AccessLevel.VIP: return 'vip'
            case _: raise RuntimeError(f'unknown TtsChatterAccessLevel: \"{self}\"')
