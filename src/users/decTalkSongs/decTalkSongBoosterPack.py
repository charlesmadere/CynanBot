from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class DecTalkSongBoosterPack:
    rewardId: str
    song: str
