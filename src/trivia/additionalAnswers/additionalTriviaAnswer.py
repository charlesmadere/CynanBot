from dataclasses import dataclass


@dataclass(frozen = True)
class AdditionalTriviaAnswer:
    answer: str
    userId: str
    userName: str
