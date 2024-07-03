from dataclasses import dataclass

from .googleVoiceAudioConfig import GoogleVoiceAudioConfig


@dataclass(frozen = True)
class GoogleTextSynthesisResponse():
    audioConfig: GoogleVoiceAudioConfig | None
    audioContent: str
