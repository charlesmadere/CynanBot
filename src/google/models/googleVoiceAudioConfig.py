from dataclasses import dataclass

from .googleVoiceAudioEncoding import GoogleVoiceAudioEncoding


@dataclass(frozen = True, slots = True)
class GoogleVoiceAudioConfig:
    pitch: float | None
    speakingRate: float | None
    volumeGainDb: float | None
    audioEncoding: GoogleVoiceAudioEncoding
    sampleRateHertz: int | None
