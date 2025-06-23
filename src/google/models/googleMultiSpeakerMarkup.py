from dataclasses import dataclass

from frozenlist import FrozenList

from .googleMultiSpeakerMarkupTurn import GoogleMultiSpeakerMarkupTurn


@dataclass(frozen = True)
class GoogleMultiSpeakerMarkup:
    turns: FrozenList[GoogleMultiSpeakerMarkupTurn]
