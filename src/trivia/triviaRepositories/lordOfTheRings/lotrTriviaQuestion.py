from dataclasses import dataclass

from frozenlist import FrozenList


@dataclass(frozen = True)
class LotrTriviaQuestion:
    answers: FrozenList[str]
    category: str | None
    question: str
    triviaId: str
