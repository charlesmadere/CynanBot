from dataclasses import dataclass


@dataclass(frozen = True)
class TtsMonsterPrivateApiTtsData:
    link: str
    warning: str | None
