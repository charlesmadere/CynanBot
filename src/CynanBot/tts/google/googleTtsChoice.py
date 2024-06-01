from dataclasses import dataclass

from CynanBot.google.googleVoiceAudioConfig import GoogleVoiceAudioConfig
from CynanBot.google.googleVoiceSelectionParams import \
    GoogleVoiceSelectionParams


@dataclass(frozen = True)
class GoogleTtsChoice():
    audioConfig: GoogleVoiceAudioConfig
    selectionParams: GoogleVoiceSelectionParams
