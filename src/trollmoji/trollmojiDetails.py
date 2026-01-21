from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TrollmojiDetails:
    emoteText: str
    twitchChannelId: str
