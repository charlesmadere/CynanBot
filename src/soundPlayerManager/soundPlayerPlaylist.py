from dataclasses import dataclass

from frozenlist import FrozenList

from .soundPlaybackFile import SoundPlaybackFile


@dataclass(frozen = True)
class SoundPlayerPlaylist:
    playlist: FrozenList[SoundPlaybackFile]
