from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class SoundPlayerRandomizerDirectoryScanResult:
    soundFiles: list[str]
    shinySoundFiles: list[str]
