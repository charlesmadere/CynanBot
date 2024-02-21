from typing import Any, Dict, Optional

from CynanBot.soundPlayerManager.soundAlert import SoundAlert
from CynanBot.streamAlertsManager.streamAlert import StreamAlert
from CynanBot.streamAlertsManager.streamAlertState import StreamAlertState
from CynanBot.tts.ttsEvent import TtsEvent


class CurrentStreamAlert():

    def __init__(self, streamAlert: StreamAlert):
        assert isinstance(streamAlert, StreamAlert), f"malformed {streamAlert=}"

        self.__streamAlert: StreamAlert = streamAlert
        self.__alertState: StreamAlertState = StreamAlertState.NOT_STARTED

    def getAlertState(self) -> StreamAlertState:
        return self.__alertState

    def getSoundAlert(self) -> Optional[SoundAlert]:
        return self.__streamAlert.getSoundAlert()

    def getStreamAlert(self) -> StreamAlert:
        return self.__streamAlert

    def getTtsEvent(self) -> Optional[TtsEvent]:
        return self.__streamAlert.getTtsEvent()

    def getTwitchChannel(self) -> str:
        return self.__streamAlert.getTwitchChannel()

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def setAlertState(self, state: StreamAlertState):
        assert isinstance(state, StreamAlertState), f"malformed {state=}"

        self.__alertState = state

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'alertState': self.__alertState,
            'streamAlert': self.__streamAlert
        }
