from abc import ABC, abstractmethod

from .preferredTtsProvider import PreferredTtsProvider


class AbsPreferredTts(ABC):

    @property
    @abstractmethod
    def preferredTtsProvider(self) -> PreferredTtsProvider:
        pass
