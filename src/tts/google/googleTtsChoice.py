from dataclasses import dataclass

from ...google.models.googleVoiceAudioConfig import GoogleVoiceAudioConfig
from ...google.models.googleVoiceSelectionParams import GoogleVoiceSelectionParams


@dataclass(frozen = True)
class GoogleTtsChoice:
    audioConfig: GoogleVoiceAudioConfig
    selectionParams: GoogleVoiceSelectionParams
