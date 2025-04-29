from dataclasses import dataclass

from ..questions.triviaSource import TriviaSource


@dataclass(frozen = True)
class TriviaQuestionOccurrences:
    occurrences: int
    triviaId: str
    triviaSource: TriviaSource
