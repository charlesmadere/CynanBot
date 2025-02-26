from abc import ABC, abstractmethod

from ...tts.models.ttsProvider import TtsProvider


class AbsPreferredTts(ABC):

    @property
    @abstractmethod
    def preferredTtsProvider(self) -> TtsProvider:
        pass
