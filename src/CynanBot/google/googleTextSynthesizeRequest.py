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
        if not isinstance(input, GoogleTextSynthesisInput):
            raise TypeError(f'input argument is malformed: \"{input}\"')
        elif not isinstance(voice, GoogleVoiceSelectionParams):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')
        elif not isinstance(audioConfig, GoogleVoiceAudioConfig):
            raise TypeError(f'audioConfig argument is malformed: \"{audioConfig}\"')

        self.__input: GoogleTextSynthesisInput = input
        self.__voice: GoogleVoiceSelectionParams = voice
        self.__audioConfig: GoogleVoiceAudioConfig = audioConfig

    def getAudioConfig(self) -> GoogleVoiceAudioConfig:
        return self.__audioConfig

    def getInput(self) -> GoogleTextSynthesisInput:
        return self.__input

    def getVoice(self) -> GoogleVoiceSelectionParams:
        return self.__voice

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'audioConfig': self.__audioConfig,
            'input': self.__input,
            'voice': self.__voice
        }
