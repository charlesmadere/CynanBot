from typing import Any, Dict

from CynanBot.google.googleVoiceAudioEncoding import GoogleVoiceAudioEncoding


class GoogleVoiceAudioConfig():

    def __init__(
        self,
        audioEncoding: GoogleVoiceAudioEncoding
    ):
        if not isinstance(audioEncoding, GoogleVoiceAudioEncoding):
            raise TypeError(f'audioEncoding argument is malformed: \"{audioEncoding}\"')

        self.__audioEncoding: GoogleVoiceAudioEncoding = audioEncoding

    def getAudioEncoding(self) -> GoogleVoiceAudioEncoding:
        return self.__audioEncoding

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'audioEncoding': self.__audioEncoding
        }
