from typing import Any, Dict, Optional

from CynanBot.soundPlayerHelper.soundAlert import SoundAlert
from CynanBot.streamAlertsManager.streamAlert import StreamAlert
from CynanBot.streamAlertsManager.streamAlertState import StreamAlertState
from CynanBot.tts.ttsEvent import TtsEvent


class CurrentStreamAlert():

    def __init__(self, streamAlert: StreamAlert):
        if not isinstance(streamAlert, StreamAlert):
            raise TypeError(f'streamAlert argument is malformed: \"{streamAlert}\"')

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

    def setAlertState(self, alertState: StreamAlertState):
        if not isinstance(alertState, StreamAlertState):
            raise TypeError(f'alertState argument is malformed: \"{alertState}\"')

        self.__alertState = alertState

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'alertState': self.__alertState,
            'streamAlert': self.__streamAlert
        }
