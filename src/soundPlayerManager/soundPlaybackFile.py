from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class SoundPlaybackFile:
    volume: int | None
    filePath: str
