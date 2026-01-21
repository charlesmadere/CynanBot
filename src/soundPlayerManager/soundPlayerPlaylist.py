from dataclasses import dataclass

from frozenlist import FrozenList

from .soundPlaybackFile import SoundPlaybackFile


@dataclass(frozen = True, slots = True)
class SoundPlayerPlaylist:
    playlistFiles: FrozenList[SoundPlaybackFile]
    volume: int | None
