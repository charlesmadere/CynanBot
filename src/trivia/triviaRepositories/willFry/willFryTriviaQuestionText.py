from dataclasses import dataclass


@dataclass(frozen = True)
class WillFryTriviaQuestionText:
    text: str
