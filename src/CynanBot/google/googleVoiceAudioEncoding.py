from enum import Enum, auto


class GoogleVoiceAudioEncoding(Enum):

    MP3 = auto()
    MP3_64_KBPS = auto()
    OGG_OPUS = auto()

    def toStr(self) -> str:
        if self is GoogleVoiceAudioEncoding.MP3:
            return 'MP3'
        elif self is GoogleVoiceAudioEncoding.MP3_64_KBPS:
            return 'MP3_64_KBPS'
        elif self is GoogleVoiceAudioEncoding.OGG_OPUS:
            return 'OGG_OPUS'
        else:
            raise RuntimeError(f'unknown GoogleVoiceAudioEncoding: \"{self}\"')
