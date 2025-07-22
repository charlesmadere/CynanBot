from dataclasses import dataclass

from .halfLifeVoice import HalfLifeVoice


@dataclass(frozen = True)
class HalfLifeSoundFile:
    voice: HalfLifeVoice
    path: str
    text: str
