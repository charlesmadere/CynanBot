from dataclasses import dataclass


@dataclass(frozen = True)
class TrollmojiDetails:
    emoteText: str
    twitchChannelId: str
