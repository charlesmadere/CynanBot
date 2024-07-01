from dataclasses import dataclass

from CynanBot.twitch.api.twitchEmoteDetails import TwitchEmoteDetails


@dataclass(frozen = True)
class TwitchEmotesResponse():
    data: list[TwitchEmoteDetails]
    template: str
