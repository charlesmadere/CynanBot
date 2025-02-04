from dataclasses import dataclass


@dataclass(frozen = True)
class SoundPlaybackFile:
    volume: int | None
    filePath: str
