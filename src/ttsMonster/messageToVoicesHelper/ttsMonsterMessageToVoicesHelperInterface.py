from abc import ABC, abstractmethod
from typing import Collection

from frozenlist import FrozenList

from .ttsMonsterMessageToVoicePair import TtsMonsterMessageToVoicePair
from ..models.ttsMonsterVoice import TtsMonsterVoice


class TtsMonsterMessageToVoicesHelperInterface(ABC):

    @abstractmethod
    async def build(
        self,
        voices: Collection[TtsMonsterVoice],
        message: str
    ) -> FrozenList[TtsMonsterMessageToVoicePair]:
        pass
