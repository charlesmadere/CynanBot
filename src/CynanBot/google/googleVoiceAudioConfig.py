from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.google.googleVoiceAudioEncoding import GoogleVoiceAudioEncoding


class GoogleVoiceAudioConfig():

    def __init__(
        self,
        pitch: float | None,
        speakingRate: float | None,
        volumeGainDb: float | None,
        sampleRateHertz: int | None,
        audioEncoding: GoogleVoiceAudioEncoding
    ):
        if pitch is not None and not utils.isValidNum(pitch):
            raise TypeError(f'pitch argument is malformed: \"{pitch}\"')
        elif speakingRate is not None and not utils.isValidNum(speakingRate):
            raise TypeError(f'speakingRate argument is malformed: \"{speakingRate}\"')
        elif volumeGainDb is not None and not utils.isValidNum(volumeGainDb):
            raise TypeError(f'volumeGainDb argument is malformed: \"{volumeGainDb}\"')
        elif sampleRateHertz is not None and not utils.isValidInt(sampleRateHertz):
            raise TypeError(f'sampleRateHertz argument is malformed: \"{sampleRateHertz}\"')
        elif not isinstance(audioEncoding, GoogleVoiceAudioEncoding):
            raise TypeError(f'audioEncoding argument is malformed: \"{audioEncoding}\"')

        self.__pitch: float | None = pitch
        self.__speakingRate: float | None = speakingRate
        self.__volumeGainDb: float | None = volumeGainDb
        self.__sampleRateHertz: int | None = sampleRateHertz
        self.__audioEncoding: GoogleVoiceAudioEncoding = audioEncoding

    def getAudioEncoding(self) -> GoogleVoiceAudioEncoding:
        return self.__audioEncoding

    def getPitch(self) -> float | None:
        return self.__pitch

    def getSampleRateHertz(self) -> int | None:
        return self.__sampleRateHertz

    def getSpeakingRate(self) -> float | None:
        return self.__speakingRate

    def getVolumeGainDb(self) -> float | None:
        return self.__volumeGainDb

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'audioEncoding': self.__audioEncoding,
            'pitch': self.__pitch,
            'sampleRateHertz': self.__sampleRateHertz,
            'speakingRate': self.__speakingRate,
            'volumeGainDb': self.__volumeGainDb
        }
