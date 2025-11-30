from typing import Any

from .soundPlayerJsonMapperInterface import SoundPlayerJsonMapperInterface
from ..soundPlayerType import SoundPlayerType


class SoundPlayerJsonMapper(SoundPlayerJsonMapperInterface):

    def parseSoundPlayerType(
        self,
        soundPlayerType: str | Any | None,
    ) -> SoundPlayerType:
        if not isinstance(soundPlayerType, str):
            raise TypeError(f'soundPlayerType argument is malformed: \"{soundPlayerType}\"')

        soundPlayerType = soundPlayerType.lower()

        match soundPlayerType:
            case 'audio_player': return SoundPlayerType.AUDIO_PLAYER
            case 'stub': return SoundPlayerType.STUB
            case 'vlc': return SoundPlayerType.VLC
            case _: raise ValueError(f'Unknown SoundPlayerType value: \"{soundPlayerType}\"')
