from dataclasses import dataclass

from .halfLifeVoice import HalfLifeVoice


@dataclass(frozen = True, slots = True)
class HalfLifeSoundFile:
    voice: HalfLifeVoice
    path: str
    text: str
