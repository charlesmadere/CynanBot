from typing import Any, Dict

from CynanBot.google.googleTextSynthesisInput import GoogleTextSynthesisInput
from CynanBot.google.googleVoiceAudioConfig import GoogleVoiceAudioConfig
from CynanBot.google.googleVoiceSelectionParams import \
    GoogleVoiceSelectionParams


class GoogleTextSynthesizeRequest():

    def __init__(
        self,
        input: GoogleTextSynthesisInput,
        voice: GoogleVoiceSelectionParams,
        audioConfig: GoogleVoiceAudioConfig
    ):
        self.__input: GoogleTextSynthesisInput = input
        self.__voice: GoogleVoiceSelectionParams = voice
        self.__audioConfig: GoogleVoiceAudioConfig = audioConfig
