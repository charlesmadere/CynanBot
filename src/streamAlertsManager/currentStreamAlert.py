from typing import Any

from .streamAlert import StreamAlert
from .streamAlertState import StreamAlertState
from ..soundPlayerManager.soundAlert import SoundAlert
from ..tts.models.ttsEvent import TtsEvent


class CurrentStreamAlert:

    def __init__(self, streamAlert: StreamAlert):
        if not isinstance(streamAlert, StreamAlert):
            raise TypeError(f'streamAlert argument is malformed: \"{streamAlert}\"')

        self.__streamAlert: StreamAlert = streamAlert
        self.__alertState: StreamAlertState = StreamAlertState.NOT_STARTED

    @property
    def alertState(self) -> StreamAlertState:
        return self.__alertState

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def setAlertState(self, state: StreamAlertState):
        if not isinstance(state, StreamAlertState):
            raise TypeError(f'state argument is malformed: \"{state}\"')

        self.__alertState = state

    @property
    def soundAlert(self) -> SoundAlert | None:
        return self.__streamAlert.soundAlert

    @property
    def streamAlert(self) -> StreamAlert:
        return self.__streamAlert

    @property
    def ttsEvent(self) -> TtsEvent | None:
        return self.__streamAlert.ttsEvent

    @property
    def twitchChannel(self) -> str:
        return self.__streamAlert.twitchChannel

    @property
    def twitchChannelId(self) -> str:
        return self.__streamAlert.twitchChannelId

    def toDictionary(self) -> dict[str, Any]:
        return {
            'alertState': self.__alertState,
            'streamAlert': self.__streamAlert
        }
