from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class FuntoonTriviaQuestion:
    categoryId: int
    triviaId: int
    answer: str
    category: str
    clue: str
