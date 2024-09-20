from abc import ABC, abstractmethod
from typing import Collection


class MultipleChoiceResponsesBuilderInterface(ABC):

    @abstractmethod
    async def build(
        self,
        correctAnswers: Collection[str],
        multipleChoiceResponses: Collection[str]
    ) -> list[str]:
        pass
