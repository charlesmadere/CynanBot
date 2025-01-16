from abc import ABC, abstractmethod

from .models.microsoftSamVoice import MicrosoftSamVoice
from .models.microsoftSamVoiceData import MicrosoftSamVoiceData


class MicrosoftSamVoiceMapperInterface(ABC):

    @abstractmethod
    def data(self, voice: MicrosoftSamVoice) -> MicrosoftSamVoiceData:
        pass
