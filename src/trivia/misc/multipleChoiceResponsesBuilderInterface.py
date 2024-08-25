from abc import ABC
from typing import Collection


class MultipleChoiceResponsesBuilderInterface(ABC):

    async def build(
        self,
        correctAnswers: Collection[str],
        multipleChoiceResponses: Collection[str]
    ) -> list[str]:
        pass
