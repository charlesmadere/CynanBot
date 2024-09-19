from abc import ABC, abstractmethod

from frozenlist import FrozenList

from .ttsMonsterMessageToVoicePair import TtsMonsterMessageToVoicePair
from ..models.ttsMonsterVoice import TtsMonsterVoice


class TtsMonsterMessageToVoicesHelperInterface(ABC):

    @abstractmethod
    async def build(
        self,
        voices: frozenset[TtsMonsterVoice],
        message: str | None
    ) -> FrozenList[TtsMonsterMessageToVoicePair] | None:
        pass
