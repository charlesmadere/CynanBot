from dataclasses import dataclass

from CynanBot.google.googleTextSynthesisInput import GoogleTextSynthesisInput
from CynanBot.google.googleVoiceAudioConfig import GoogleVoiceAudioConfig
from CynanBot.google.googleVoiceSelectionParams import \
    GoogleVoiceSelectionParams


@dataclass(frozen = True)
class GoogleTextSynthesizeRequest():
    input: GoogleTextSynthesisInput
    voice: GoogleVoiceSelectionParams
    audioConfig: GoogleVoiceAudioConfig
