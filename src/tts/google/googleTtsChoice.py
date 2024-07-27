from dataclasses import dataclass

from ...google.googleVoiceAudioConfig import GoogleVoiceAudioConfig
from ...google.googleVoiceSelectionParams import GoogleVoiceSelectionParams


@dataclass(frozen = True)
class GoogleTtsChoice:
    audioConfig: GoogleVoiceAudioConfig
    selectionParams: GoogleVoiceSelectionParams
