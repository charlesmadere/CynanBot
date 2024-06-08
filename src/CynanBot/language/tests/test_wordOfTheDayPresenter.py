from datetime import datetime

import pytest

from CynanBot.language.languagesRepository import LanguagesRepository
from CynanBot.language.languagesRepositoryInterface import \
    LanguagesRepositoryInterface
from CynanBot.language.wordOfTheDayPresenter import WordOfTheDayPresenter
from CynanBot.language.wordOfTheDayPresenterInterface import \
    WordOfTheDayPresenterInterface
from CynanBot.language.wordOfTheDayResponse import WordOfTheDayResponse
from CynanBot.location.timeZoneRepository import TimeZoneRepository
from CynanBot.location.timeZoneRepositoryInterface import \
    TimeZoneRepositoryInterface
from CynanBot.transparent.transparentResponse import TransparentResponse


class TestWordOfTheDayPresenter():

    languagesRepository: LanguagesRepositoryInterface = LanguagesRepository()
    timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()
    presenter: WordOfTheDayPresenterInterface = WordOfTheDayPresenter()

    @pytest.mark.asyncio
    async def test_toString_with(self):
        spanish = await self.languagesRepository.requireLanguageForCommand('spanish')

        transparentResponse = TransparentResponse(
            date = datetime.now(self.timeZoneRepository.getDefault()),
            enPhrase = 'to eat',
            fnPhrase = 'comer',
            langName = None,
            notes = None,
            phraseSoundUrl = None,
            translation = 'comer',
            transliteratedSentence = None,
            transliteratedWord = None,
            word = 'eat',
            wordSoundUrl = None,
            wordType = 'verb'
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

        assert isinstance(string, str)

    def test_sanity(self):
        assert self.presenter is not None
        assert isinstance(self.presenter, WordOfTheDayPresenter)
        assert isinstance(self.presenter, WordOfTheDayPresenterInterface)
