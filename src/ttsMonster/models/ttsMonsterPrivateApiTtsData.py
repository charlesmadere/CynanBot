from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TtsMonsterPrivateApiTtsData:
    link: str
    warning: str | None
