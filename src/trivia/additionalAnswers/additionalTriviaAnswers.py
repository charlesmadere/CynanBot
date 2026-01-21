from dataclasses import dataclass

from frozenlist import FrozenList

from .additionalTriviaAnswer import AdditionalTriviaAnswer
from ..questions.triviaQuestionType import TriviaQuestionType
from ..questions.triviaSource import TriviaSource


@dataclass(frozen = True, slots = True)
class AdditionalTriviaAnswers:
    answers: FrozenList[AdditionalTriviaAnswer]
    triviaId: str
    triviaQuestionType: TriviaQuestionType
    triviaSource: TriviaSource

    @property
    def answerStrings(self) -> list[str]:
        answerStrings: list[str] = list()

        for answer in self.answers:
            answerStrings.append(answer.answer)

        return answerStrings
