from CynanBot.google.googleVoiceAudioConfig import GoogleVoiceAudioConfig
from CynanBot.google.googleVoiceSelectionParams import \
    GoogleVoiceSelectionParams


class GoogleTtsChoice():

    def __init__(
        self,
        audioConfig: GoogleVoiceAudioConfig,
        selectionParams: GoogleVoiceSelectionParams
    ):
        if not isinstance(audioConfig, GoogleVoiceAudioConfig):
            raise TypeError(f'audioConfig argument is malformed: \"{audioConfig}\"')
        elif not isinstance(selectionParams, GoogleVoiceSelectionParams):
            raise TypeError(f'selectionParams argument is malformed: \"{selectionParams}\"')

        self.__audioConfig: GoogleVoiceAudioConfig = audioConfig
        self.__selectionParams: GoogleVoiceSelectionParams = selectionParams

    def getAudioConfig(self) -> GoogleVoiceAudioConfig:
        return self.__audioConfig

    def getSelectionParams(self) -> GoogleVoiceSelectionParams:
        return self.__selectionParams
