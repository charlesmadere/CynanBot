from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.soundPlayerHelper.soundAlert import SoundAlert
from CynanBot.tts.ttsEvent import TtsEvent


class StreamAlert():

    def __init__(
        self,
        soundAlert: Optional[SoundAlert],
        twitchChannel: str,
        ttsEvent: Optional[TtsEvent]
    ):
        if soundAlert is not None and not isinstance(soundAlert, SoundAlert):
            raise TypeError(f'soundAlert argument is malformed: \"{soundAlert}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif ttsEvent is not None and not isinstance(ttsEvent, TtsEvent):
            raise TypeError(f'ttsEvent argument is malformed: \"{ttsEvent}\"')

        self.__soundAlert: Optional[SoundAlert] = soundAlert
        self.__twitchChannel: str = twitchChannel
        self.__ttsEvent: Optional[TtsEvent] = ttsEvent

    def getSoundAlert(self) -> Optional[SoundAlert]:
        return self.__soundAlert

    def getTtsEvent(self) -> Optional[TtsEvent]:
        return self.__ttsEvent

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'soundAlert': self.__soundAlert,
            'ttsEvent': self.__ttsEvent,
            'twitchChannel': self.__twitchChannel
        }
