from dataclasses import dataclass


@dataclass(frozen = True)
class DecTalkSongBoosterPack:
    rewardId: str
    song: str
