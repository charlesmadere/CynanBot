from dataclasses import dataclass


@dataclass(frozen = True)
class CrowdControlAutomatorData:
    reoccurSeconds: int
    twitchChannelId: str
