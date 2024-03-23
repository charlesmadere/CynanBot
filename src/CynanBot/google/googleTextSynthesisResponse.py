from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.google.googleVoiceAudioConfig import GoogleVoiceAudioConfig


class GoogleTextSynthesisResponse():

    def __init__(
        self,
        audioConfig: GoogleVoiceAudioConfig | None,
        audioContent: str
    ):
        if audioConfig is not None and not isinstance(audioConfig, GoogleVoiceAudioConfig):
            raise TypeError(f'audioConfig argument is malformed: \"{audioConfig}\"')
        elif not utils.isValidStr(audioContent):
            raise TypeError(f'audioContent argument is malformed: \"{audioContent}\"')

        self.__audioConfig: GoogleVoiceAudioConfig | None = audioConfig
        self.__audioContent: str = audioContent

    def getAudioConfig(self) -> GoogleVoiceAudioConfig | None:
        return self.__audioConfig

    def getAudioContent(self) -> str:
        return self.__audioContent

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'audioConfig': self.__audioConfig,
            'audioContent': self.__audioContent
        }
