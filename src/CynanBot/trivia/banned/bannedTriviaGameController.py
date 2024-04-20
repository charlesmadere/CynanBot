from dataclasses import dataclass


@dataclass(frozen = True)
class BannedTriviaGameController():
    userId: str
    userName: str
