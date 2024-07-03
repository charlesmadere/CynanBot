from typing import Any

from .streamAlert import StreamAlert
from .streamAlertState import StreamAlertState
from ..soundPlayerManager.soundAlert import SoundAlert
from ..tts.ttsEvent import TtsEvent


class CurrentStreamAlert():

    def __init__(self, streamAlert: StreamAlert):
        if not isinstance(streamAlert, StreamAlert):
            raise TypeError(f'streamAlert argument is malformed: \"{streamAlert}\"')

        self.__streamAlert: StreamAlert = streamAlert
        self.__alertState: StreamAlertState = StreamAlertState.NOT_STARTED

    def getAlertState(self) -> StreamAlertState:
        return self.__alertState

    def getSoundAlert(self) -> SoundAlert | None:
        return self.__streamAlert.soundAlert

    def getStreamAlert(self) -> StreamAlert:
        return self.__streamAlert

    def getTtsEvent(self) -> TtsEvent | None:
        return self.__streamAlert.ttsEvent

    def getTwitchChannel(self) -> str:
        return self.__streamAlert.twitchChannel

    def getTwitchChannelId(self) -> str:
        return self.__streamAlert.twitchChannelId

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def setAlertState(self, state: StreamAlertState):
        if not isinstance(state, StreamAlertState):
            raise TypeError(f'state argument is malformed: \"{state}\"')

        self.__alertState = state

    def toDictionary(self) -> dict[str, Any]:
        return {
            'alertState': self.__alertState,
            'streamAlert': self.__streamAlert
        }
