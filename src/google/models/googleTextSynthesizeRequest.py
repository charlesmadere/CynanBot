from dataclasses import dataclass

from .googleTextSynthesisInput import GoogleTextSynthesisInput
from .googleVoiceAudioConfig import GoogleVoiceAudioConfig
from .googleVoiceSelectionParams import GoogleVoiceSelectionParams


@dataclass(frozen = True, slots = True)
class GoogleTextSynthesizeRequest:
    synthesisInput: GoogleTextSynthesisInput
    audioConfig: GoogleVoiceAudioConfig
    voice: GoogleVoiceSelectionParams
