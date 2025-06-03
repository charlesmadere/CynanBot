from abc import ABC, abstractmethod

from ...tts.models.ttsProvider import TtsProvider


class AbsTtsProperties(ABC):

    @property
    @abstractmethod
    def provider(self) -> TtsProvider:
        pass
