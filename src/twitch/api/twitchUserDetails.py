from dataclasses import dataclass

from .twitchBroadcasterType import TwitchBroadcasterType
from .twitchUserType import TwitchUserType


@dataclass(frozen = True)
class TwitchUserDetails():
    displayName: str
    login: str
    userId: str
    broadcasterType: TwitchBroadcasterType
    userType: TwitchUserType
