from src.misc import utils

class MicrosoftSamVoiceData:
    def __init__(
        self,
        voice: str,
        pitch: str,
        speed: str
    ):
        if not utils.isValidStr(voice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')
        elif not utils.isValidStr(pitch):
            raise TypeError(f'pitch argument is malformed: \"{pitch}\"')
        elif not utils.isValidStr(speed):
            raise TypeError(f'speed argument is malformed: \"{speed}\"')

        self.__voice = voice
        self.__pitch = pitch
        self.__speed = speed

    @property
    def voice(self) -> str:
        return self.__voice

    @property
    def pitch(self) -> str:
        return self.__pitch

    @property
    def speed(self) -> str:
        return self.__speed