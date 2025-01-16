import pytest

from src.storage.jsonStaticReader import JsonStaticReader
from src.trivia.misc.multipleChoiceResponsesBuilder import MultipleChoiceResponsesBuilder
from src.trivia.misc.multipleChoiceResponsesBuilderInterface import MultipleChoiceResponsesBuilderInterface
from src.trivia.triviaSettingsRepository import TriviaSettingsRepository
from src.trivia.triviaSettingsRepositoryInterface import TriviaSettingsRepositoryInterface


class TestMultipleChoicesResponsesBuilder:

    triviaSettingsRepository: TriviaSettingsRepositoryInterface = TriviaSettingsRepository(
        settingsJsonReader = JsonStaticReader(dict())
    )

    builder: MultipleChoiceResponsesBuilderInterface = MultipleChoiceResponsesBuilder(
        triviaSettingsRepository = triviaSettingsRepository
    )

    @pytest.mark.asyncio
    async def test_build_withBasicResponseList(self):
        correctAnswers: list[str] = [ 'Pikachu' ]
        multipleChoiceResponses: list[str] = [ 'Bulbasaur', 'Charmander', 'Squirtle', 'None of the above' ]

        result = await self.builder.build(
            correctAnswers = correctAnswers,
            multipleChoiceResponses = multipleChoiceResponses
        )

        assert isinstance(result, list)
        assert len(result) == 5
        assert result[0] == 'Bulbasaur'
        assert result[1] == 'Charmander'
        assert result[2] == 'Pikachu'
        assert result[3] == 'Squirtle'
        assert result[4] == 'None of the above'
