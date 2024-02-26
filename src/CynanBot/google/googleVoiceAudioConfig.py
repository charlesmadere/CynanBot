from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.google.googleVoiceAudioEncoding import GoogleVoiceAudioEncoding


class GoogleVoiceAudioConfig():

    def __init__(
        self,
        pitch: Optional[float],
        speakingRate: Optional[float],
        volumeGainDb: Optional[float],
        sampleRateHertz: Optional[int],
        audioEncoding: GoogleVoiceAudioEncoding
    ):
        if not utils.isValidNum(pitch):
            raise TypeError(f'pitch argument is malformed: \"{pitch}\"')
        elif not utils.isValidNum(speakingRate):
            raise TypeError(f'speakingRate argument is malformed: \"{speakingRate}\"')
        elif not utils.isValidNum(volumeGainDb):
            raise TypeError(f'volumeGainDb argument is malformed: \"{volumeGainDb}\"')
        elif not utils.isValidInt(sampleRateHertz):
            raise TypeError(f'sampleRateHertz argument is malformed: \"{sampleRateHertz}\"')
        elif not isinstance(audioEncoding, GoogleVoiceAudioEncoding):
            raise TypeError(f'audioEncoding argument is malformed: \"{audioEncoding}\"')

        self.__pitch: Optional[float] = pitch
        self.__speakingRate: Optional[float] = speakingRate
        self.__volumeGainDb: Optional[float] = volumeGainDb
        self.__sampleRateHertz: Optional[int] = sampleRateHertz
        self.__audioEncoding: GoogleVoiceAudioEncoding = audioEncoding

    def getAudioEncoding(self) -> GoogleVoiceAudioEncoding:
        return self.__audioEncoding

    def getPitch(self) -> Optional[float]:
        return self.__pitch

    def getSampleRateHertz(self) -> Optional[int]:
        return self.__sampleRateHertz

    def getSpeakingRate(self) -> Optional[float]:
        return self.__speakingRate

    def getVolumeGainDb(self) -> Optional[float]:
        return self.__volumeGainDb

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'audioEncoding': self.__audioEncoding,
            'pitch': self.__pitch,
            'sampleRateHertz': self.__sampleRateHertz,
            'speakingRate': self.__speakingRate,
            'volumeGainDb': self.__volumeGainDb
        }
