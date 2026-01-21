from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class AdditionalTriviaAnswer:
    answer: str
    userId: str
    userName: str
