from datetime import datetime

import pytest
from src.language.languagesRepository import LanguagesRepository
from src.language.languagesRepositoryInterface import LanguagesRepositoryInterface
from src.language.wordOfTheDayPresenter import WordOfTheDayPresenter
from src.language.wordOfTheDayPresenterInterface import \
    WordOfTheDayPresenterInterface
from src.language.wordOfTheDayResponse import WordOfTheDayResponse
from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.transparent.transparentResponse import TransparentResponse


class TestWordOfTheDayPresenter():

    languagesRepository: LanguagesRepositoryInterface = LanguagesRepository()
    timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()
    presenter: WordOfTheDayPresenterInterface = WordOfTheDayPresenter()

    @pytest.mark.asyncio
    async def test_toString_with(self):
        spanish = await self.languagesRepository.requireLanguageForCommand('spanish')

        transparentResponse = TransparentResponse(
            date = datetime.now(self.timeZoneRepository.getDefault()),
            enPhrase = 'I like my steak medium rare.',
            fnPhrase = 'Me gusta el bistec medio cocido.',
            langName = 'Spanish',
            notes = None,
            phraseSoundUrl = None,
            translation = 'medium rare',
            transliteratedSentence = None,
            transliteratedWord = None,
            word = 'medio cocido',
            wordSoundUrl = None,
            wordType = 'adjective'
        )

        wordOfTheDay = WordOfTheDayResponse(
            languageEntry = spanish,
            romaji = None,
            transparentResponse = transparentResponse
        )

        string = await self.presenter.toString(
            includeRomaji = False,
            wordOfTheDay = wordOfTheDay
        )

        assert string == 'Spanish — medio cocido — medium rare. Example: Me gusta el bistec medio cocido. I like my steak medium rare.'

    def test_sanity(self):
        assert self.presenter is not None
        assert isinstance(self.presenter, WordOfTheDayPresenter)
        assert isinstance(self.presenter, WordOfTheDayPresenterInterface)
