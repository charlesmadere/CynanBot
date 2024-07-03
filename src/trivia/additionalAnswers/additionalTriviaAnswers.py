from dataclasses import dataclass

from .additionalTriviaAnswer import AdditionalTriviaAnswer
from ..questions.triviaQuestionType import TriviaQuestionType
from ..questions.triviaSource import TriviaSource


@dataclass(frozen = True)
class AdditionalTriviaAnswers():
    answers: list[AdditionalTriviaAnswer]
    triviaId: str
    triviaQuestionType: TriviaQuestionType
    triviaSource: TriviaSource

    @property
    def answerStrings(self) -> list[str]:
        answerStrings: list[str] = list()

        for answer in self.answers:
            answerStrings.append(answer.answer)

        return answerStrings
