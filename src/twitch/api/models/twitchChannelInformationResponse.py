from dataclasses import dataclass

from frozenlist import FrozenList

from .twitchChannelInformation import TwitchChannelInformation


@dataclass(frozen = True, slots = True)
class TwitchChannelInformationResponse:
    data: FrozenList[TwitchChannelInformation]
