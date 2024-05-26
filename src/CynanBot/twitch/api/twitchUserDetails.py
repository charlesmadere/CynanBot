from dataclasses import dataclass

from CynanBot.twitch.api.twitchBroadcasterType import TwitchBroadcasterType
from CynanBot.twitch.api.twitchUserType import TwitchUserType


@dataclass(frozen = True)
class TwitchUserDetails():
    displayName: str
    login: str
    userId: str
    broadcasterType: TwitchBroadcasterType
    userType: TwitchUserType
