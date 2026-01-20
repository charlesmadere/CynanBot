from dataclasses import dataclass

from .absGoogleTextSynthesisInput import AbsGoogleTextSynthesisInput
from .googleVoiceAudioConfig import GoogleVoiceAudioConfig
from .googleVoiceSelectionParams import GoogleVoiceSelectionParams


@dataclass(frozen = True, slots = True)
class GoogleTextSynthesizeRequest:
    synthesisInput: AbsGoogleTextSynthesisInput
    audioConfig: GoogleVoiceAudioConfig
    voice: GoogleVoiceSelectionParams
