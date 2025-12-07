from dataclasses import dataclass


@dataclass(frozen = True)
class NickNameData:
    chatterUserId: str
    nickName: str
    twitchChannelId: str
