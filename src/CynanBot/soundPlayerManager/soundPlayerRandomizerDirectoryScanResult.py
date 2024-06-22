from dataclasses import dataclass


@dataclass(frozen = True)
class SoundPlayerRandomizerDirectoryScanResult():
    soundFiles: list[str]
    shinySoundFiles: list[str]
