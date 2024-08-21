from dataclasses import dataclass

from frozenlist import FrozenList

from .willFryTriviaQuestionText import WillFryTriviaQuestionText
from .willFryTriviaQuestionType import WillFryTriviaQuestionType
from ...triviaDifficulty import TriviaDifficulty


@dataclass(frozen = True)
class WillFryTriviaQuestion:
    isNiche: bool
    incorrectAnswers: FrozenList[str]
    regions: FrozenList[str]
    tags: FrozenList[str]
    category: str | None
    correctAnswer: str
    triviaId: str
    difficulty: TriviaDifficulty
    question: WillFryTriviaQuestionText
    questionType: WillFryTriviaQuestionType
