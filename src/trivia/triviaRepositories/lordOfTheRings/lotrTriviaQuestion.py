from dataclasses import dataclass

from frozenlist import FrozenList


@dataclass(frozen = True)
class LotrTriviaQuestion:
    answers: FrozenList[str]
    question: str
    triviaId: str
