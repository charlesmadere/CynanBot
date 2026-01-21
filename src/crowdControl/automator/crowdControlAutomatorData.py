from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class CrowdControlAutomatorData:
    reoccurSeconds: int
    twitchChannelId: str
