from dataclasses import dataclass

from CynanBot.google.googleVoiceAudioConfig import GoogleVoiceAudioConfig


@dataclass(frozen = True)
class GoogleTextSynthesisResponse():
    audioConfig: GoogleVoiceAudioConfig | None
    audioContent: str
