from enum import Enum


class AbsGoogleVoicePreset(Enum):

    @property
    def fullName(self) -> str:
        # child classes must implement this method
        raise NotImplementedError()

    @property
    def languageCode(self) -> str:
        # child classes must implement this method
        raise NotImplementedError()
