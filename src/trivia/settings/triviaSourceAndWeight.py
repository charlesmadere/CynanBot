from dataclasses import dataclass

from ..questions.triviaSource import TriviaSource


@dataclass(frozen = True)
class TriviaSourceAndWeight:
    isEnabled: bool
    weight: int
    triviaSource: TriviaSource
