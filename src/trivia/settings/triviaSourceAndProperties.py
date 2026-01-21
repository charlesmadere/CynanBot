from dataclasses import dataclass

from ..questions.triviaSource import TriviaSource


@dataclass(frozen = True, slots = True)
class TriviaSourceAndProperties:
    isEnabled: bool
    weight: int
    triviaSource: TriviaSource
