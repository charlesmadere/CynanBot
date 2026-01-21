from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class WillFryTriviaQuestionText:
    text: str
