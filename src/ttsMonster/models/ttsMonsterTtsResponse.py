from dataclasses import dataclass


@dataclass(frozen = True)
class TtsMonsterTtsResponse:
    characterUsage: int | None
    status: int
    url: str
