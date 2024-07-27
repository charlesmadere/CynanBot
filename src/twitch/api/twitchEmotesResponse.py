from dataclasses import dataclass

from .twitchEmoteDetails import TwitchEmoteDetails


@dataclass(frozen = True)
class TwitchEmotesResponse:
    emoteData: list[TwitchEmoteDetails]
    template: str
