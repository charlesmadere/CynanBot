import locale
from dataclasses import dataclass

from ..questions.triviaSource import TriviaSource


@dataclass(frozen = True, slots = True)
class TriviaQuestionOccurrences:
    occurrences: int
    triviaId: str
    triviaSource: TriviaSource

    @property
    def occurrencesStr(self) -> str:
        return locale.format_string("%d", self.occurrences, grouping = True)
