from dataclasses import dataclass

from .ttsMonsterPrivateApiTtsData import TtsMonsterPrivateApiTtsData


@dataclass(frozen = True)
class TtsMonsterPrivateApiTtsResponse:
    status: int
    data: TtsMonsterPrivateApiTtsData
