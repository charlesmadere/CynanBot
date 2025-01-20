from .absChatSoundAlert import AbsChatSoundAlert
from .chatSoundAlertQualifier import ChatSoundAlertQualifer
from .chatSoundAlertType import ChatSoundAlertType
from ...soundPlayerManager.soundAlert import SoundAlert


class SoundAlertChatSoundAlert(AbsChatSoundAlert):

    def __init__(
        self,
        qualifier: ChatSoundAlertQualifer,
        cooldownSeconds: int | None,
        volume: int | None,
        soundAlert: SoundAlert,
        message: str
    ):
        super().__init__(
            qualifier = qualifier,
            cooldownSeconds = cooldownSeconds,
            volume = volume,
            message = message
        )

        if not isinstance(soundAlert, SoundAlert):
            raise TypeError(f'soundAlert argument is malformed: \"{soundAlert}\"')

        self.__soundAlert: SoundAlert = soundAlert

    @property
    def alertType(self) -> ChatSoundAlertType:
        return ChatSoundAlertType.SOUND_ALERT

    @property
    def soundAlert(self) -> SoundAlert:
        return self.__soundAlert
