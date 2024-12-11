from dataclasses import dataclass


@dataclass(frozen = True)
class DecTalkSongBoosterPack:
    song: str
    rewardId: str
