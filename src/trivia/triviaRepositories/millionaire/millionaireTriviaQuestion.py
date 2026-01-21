from dataclasses import dataclass

from frozenlist import FrozenList


@dataclass(frozen = True, slots = True)
class MillionaireTriviaQuestion:
    incorrectAnswers: FrozenList[str]
    correctAnswer: str
    question: str
    questionId: str
