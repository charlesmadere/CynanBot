from dataclasses import dataclass


@dataclass(frozen = True)
class TriviaGameGlobalController():
    userId: str
    userName: str
