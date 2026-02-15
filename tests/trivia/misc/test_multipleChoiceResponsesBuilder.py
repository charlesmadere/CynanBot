import pytest

from src.storage.jsonStaticReader import JsonStaticReader
from src.trivia.misc.multipleChoiceResponsesBuilder import MultipleChoiceResponsesBuilder
from src.trivia.misc.multipleChoiceResponsesBuilderInterface import MultipleChoiceResponsesBuilderInterface
from src.trivia.misc.triviaSourceParser import TriviaSourceParser
from src.trivia.misc.triviaSourceParserInterface import TriviaSourceParserInterface
from src.trivia.settings.triviaSettings import TriviaSettings
from src.trivia.settings.triviaSettingsInterface import TriviaSettingsInterface


class TestMultipleChoicesResponsesBuilder:

    triviaSourceParser: TriviaSourceParserInterface = TriviaSourceParser()

    triviaSettings: TriviaSettingsInterface = TriviaSettings(
        settingsJsonReader = JsonStaticReader(dict()),
        triviaSourceParser = triviaSourceParser,
    )

    builder: MultipleChoiceResponsesBuilderInterface = MultipleChoiceResponsesBuilder(
        triviaSettings = triviaSettings,
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

    def test_sanity(self):
        assert self.builder is not None
        assert isinstance(self.builder, MultipleChoiceResponsesBuilder)
        assert isinstance(self.builder, MultipleChoiceResponsesBuilderInterface)
