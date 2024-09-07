from dataclasses import dataclass

from frozenlist import FrozenList


@dataclass(frozen = True)
class MillionaireTriviaQuestion:
    incorrectAnswers: FrozenList[str]
    correctAnswer: str
    question: str
    questionId: str
