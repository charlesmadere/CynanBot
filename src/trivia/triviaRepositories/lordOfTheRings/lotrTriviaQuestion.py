from dataclasses import dataclass

from frozenlist import FrozenList


@dataclass(frozen = True, slots = True)
class LotrTriviaQuestion:
    answers: FrozenList[str]
    category: str | None
    question: str
    triviaId: str
