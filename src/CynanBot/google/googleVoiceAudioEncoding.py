from enum import Enum, auto


class GoogleVoiceAudioEncoding(Enum):

    ALAW = auto()
    LINEAR_16 = auto()
    MP3 = auto()
    MP3_64_KBPS = auto()
    MULAW = auto()
    OGG_OPUS = auto()
    UNSPECIFIED = auto()

    def toStr(self) -> str:
        if self is GoogleVoiceAudioEncoding.ALAW:
            return 'ALAW'
        elif self is GoogleVoiceAudioEncoding.LINEAR_16:
            return 'LINEAR16'
        if self is GoogleVoiceAudioEncoding.MP3:
            return 'MP3'
        elif self is GoogleVoiceAudioEncoding.MP3_64_KBPS:
            return 'MP3_64_KBPS'
        elif self is GoogleVoiceAudioEncoding.MULAW:
            return 'MULAW'
        elif self is GoogleVoiceAudioEncoding.OGG_OPUS:
            return 'OGG_OPUS'
        elif self is GoogleVoiceAudioEncoding.UNSPECIFIED:
            raise RuntimeError(f'unsupported GoogleVoiceAudioEncoding: \"{self}\"')
        else:
            raise RuntimeError(f'unknown GoogleVoiceAudioEncoding: \"{self}\"')
