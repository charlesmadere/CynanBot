from dataclasses import dataclass
from typing import Any

import CynanBot.misc.utils as utils


# This class intends to directly correspond to Twitch's "Ban User" API:
# https://dev.twitch.tv/docs/api/reference/#ban-user
@dataclass(frozen = True)
class TwitchBanRequest():
    duration: int | None
    broadcasterUserId: str
    moderatorUserId: str
    reason: str | None
    userIdToBan: str

    def toJson(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            'user_id': self.userIdToBan
        }

        if utils.isValidInt(self.duration):
            data['duration'] = self.duration

        if utils.isValidStr(self.reason):
            data['reason'] = self.reason

        return {
            'data': data
        }
