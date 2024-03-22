from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.soundPlayerManager.soundAlert import SoundAlert
from CynanBot.tts.ttsEvent import TtsEvent


class StreamAlert():

    def __init__(
        self,
        soundAlert: SoundAlert | None,
        twitchChannel: str,
        ttsEvent: TtsEvent | None
    ):
        if soundAlert is not None and not isinstance(soundAlert, SoundAlert):
            raise TypeError(f'soundAlert argument is malformed: \"{soundAlert}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif ttsEvent is not None and not isinstance(ttsEvent, TtsEvent):
            raise TypeError(f'ttsEvent argument is malformed: \"{ttsEvent}\"')

        self.__soundAlert: SoundAlert | None = soundAlert
        self.__twitchChannel: str = twitchChannel
        self.__ttsEvent: TtsEvent | None = ttsEvent

    def getSoundAlert(self) -> SoundAlert | None:
        return self.__soundAlert

    def getTtsEvent(self) -> TtsEvent | None:
        return self.__ttsEvent

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'soundAlert': self.__soundAlert,
            'ttsEvent': self.__ttsEvent,
            'twitchChannel': self.__twitchChannel
        }
