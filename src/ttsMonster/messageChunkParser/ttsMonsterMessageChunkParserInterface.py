from abc import ABC, abstractmethod

from frozenlist import FrozenList

from ..models.ttsMonsterMessageChunk import TtsMonsterMessageChunk
from ..models.ttsMonsterVoice import TtsMonsterVoice


class TtsMonsterMessageChunkParserInterface(ABC):

    @abstractmethod
    async def parse(
        self,
        message: str | None,
        defaultVoice: TtsMonsterVoice
    ) -> FrozenList[TtsMonsterMessageChunk] | None:
        pass
