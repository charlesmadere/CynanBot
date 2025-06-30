from typing import Any, Final

from .streamAlert import StreamAlert
from .streamAlertState import StreamAlertState
from ..soundPlayerManager.soundAlert import SoundAlert
from ..soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ..tts.compositeTtsManagerInterface import CompositeTtsManagerInterface
from ..tts.models.ttsEvent import TtsEvent


class CurrentStreamAlert:

    def __init__(
        self,
        compositeTtsManager: CompositeTtsManagerInterface,
        soundPlayerManager: SoundPlayerManagerInterface,
        streamAlert: StreamAlert,
    ):
        if not isinstance(compositeTtsManager, CompositeTtsManagerInterface):
            raise TypeError(f'compositeTtsManager argument is malformed: \"{compositeTtsManager}\"')
        elif not isinstance(soundPlayerManager, SoundPlayerManagerInterface):
            raise TypeError(f'soundPlayerManager argument is malformed: \"{soundPlayerManager}\"')
        elif not isinstance(streamAlert, StreamAlert):
            raise TypeError(f'streamAlert argument is malformed: \"{streamAlert}\"')

        self.__compositeTtsManager: Final[CompositeTtsManagerInterface] = compositeTtsManager
        self.__soundPlayerManager: Final[SoundPlayerManagerInterface] = soundPlayerManager
        self.__streamAlert: Final[StreamAlert] = streamAlert

        self.__alertState: StreamAlertState = StreamAlertState.NOT_STARTED

    @property
    def alertState(self) -> StreamAlertState:
        return self.__alertState

    @property
    def compositeTtsManager(self) -> CompositeTtsManagerInterface:
        return self.__compositeTtsManager

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
    def soundPlayerManager(self) -> SoundPlayerManagerInterface:
        return self.__soundPlayerManager

    @property
    def streamAlert(self) -> StreamAlert:
        return self.__streamAlert

    def toDictionary(self) -> dict[str, Any]:
        return {
            'alertState': self.__alertState,
            'compositeTtsManager': self.__compositeTtsManager,
            'soundPlayerManager': self.__soundPlayerManager,
            'streamAlert': self.__streamAlert,
        }

    @property
    def ttsEvent(self) -> TtsEvent | None:
        return self.__streamAlert.ttsEvent

    @property
    def twitchChannel(self) -> str:
        return self.__streamAlert.twitchChannel

    @property
    def twitchChannelId(self) -> str:
        return self.__streamAlert.twitchChannelId
