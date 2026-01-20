from dataclasses import dataclass

from ....misc import utils as utils


@dataclass(frozen = True, slots = True)
class TwitchWebsocketCondition:
    broadcasterUserId: str | None = None
    broadcasterUserLogin: str | None = None
    broadcasterUserName: str | None = None
    clientId: str | None = None
    fromBroadcasterUserId: str | None = None
    fromBroadcasterUserLogin: str | None = None
    fromBroadcasterUserName: str | None = None
    moderatorUserId: str | None = None
    moderatorUserLogin: str | None = None
    moderatorUserName: str | None = None
    rewardId: str | None = None
    toBroadcasterUserId: str | None = None
    toBroadcasterUserLogin: str | None = None
    toBroadcasterUserName: str | None = None
    userId: str | None = None
    userLogin: str | None = None
    userName: str | None = None

    def requireBroadcasterUserId(self) -> str:
        if not utils.isValidStr(self.broadcasterUserId):
            raise ValueError(f'broadcasterUserId has not been set: \"{self}\"')

        return self.broadcasterUserId

    def requireClientId(self) -> str:
        if not utils.isValidStr(self.clientId):
            raise ValueError(f'clientId has not been set: \"{self}\"')

        return self.clientId

    def requireFromBroadcasterUserId(self) -> str:
        if not utils.isValidStr(self.fromBroadcasterUserId):
            raise ValueError(f'fromBroadcasterUserId has not been set: \"{self}\"')

        return self.fromBroadcasterUserId

    def requireModeratorUserId(self) -> str:
        if not utils.isValidStr(self.moderatorUserId):
            raise ValueError(f'moderatorUserId has not been set: \"{self}\"')

        return self.moderatorUserId

    def requireRewardId(self) -> str:
        if not utils.isValidStr(self.rewardId):
            raise ValueError(f'rewardId has not been set: \"{self}\"')

        return self.rewardId

    def requireToBroadcasterUserId(self) -> str:
        if not utils.isValidStr(self.toBroadcasterUserId):
            raise ValueError(f'toBroadcasterUserId has not been set: \"{self}\"')

        return self.toBroadcasterUserId

    def requireUserId(self) -> str:
        if not utils.isValidStr(self.userId):
            raise ValueError(f'userId has not been set: \"{self}\"')

        return self.userId
