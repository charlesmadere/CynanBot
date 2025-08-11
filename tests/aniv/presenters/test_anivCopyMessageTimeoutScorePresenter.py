import pytest

from src.aniv.models.anivCopyMessageTimeoutScore import AnivCopyMessageTimeoutScore
from src.aniv.models.preparedAnivCopyMessageTimeoutScore import PreparedAnivCopyMessageTimeoutScore
from src.aniv.presenters.anivCopyMessageTimeoutScorePresenter import AnivCopyMessageTimeoutScorePresenter
from src.aniv.presenters.anivCopyMessageTimeoutScorePresenterInterface import \
    AnivCopyMessageTimeoutScorePresenterInterface
from src.language.languageEntry import LanguageEntry


class TestAnivCopyMessageTimeoutScorePresenter:

    presenter: AnivCopyMessageTimeoutScorePresenterInterface = AnivCopyMessageTimeoutScorePresenter()

    @pytest.mark.asyncio
    async def test_getChannelEditorsCantPlayString_withEnglish(self):
        printOut = await self.presenter.getChannelEditorsCantPlayString(LanguageEntry.ENGLISH)
        assert printOut == 'ⓘ Sorry, Twitch channel editors can\'t participate in the aniv timeout game'

    @pytest.mark.asyncio
    async def test_getChannelEditorsCantPlayString_withSpanish(self):
        printOut = await self.presenter.getChannelEditorsCantPlayString(LanguageEntry.SPANISH)
        assert printOut == 'ⓘ Lo sentimos, los moderadores editores no pueden participar en el juego de suspensiones de aniv'

    @pytest.mark.asyncio
    async def test_getScoreString_with0Dodges0TimeoutsScoreAndEnglish(self):
        preparedScore = PreparedAnivCopyMessageTimeoutScore(
            score = AnivCopyMessageTimeoutScore(
                mostRecentDodge = None,
                mostRecentTimeout = None,
                dodgeScore = 0,
                timeoutScore = 0,
                chatterUserId = 'abc123',
                twitchChannelId = 'def456',
            ),
            chatterUserName = 'stashiocat',
            twitchChannel = 'Oatsngoats',
        )

        printOut = await self.presenter.getScoreString(
            language = LanguageEntry.ENGLISH,
            preparedScore = preparedScore,
        )

        assert printOut == f'ⓘ @{preparedScore.chatterUserName} has no aniv timeouts'

    @pytest.mark.asyncio
    async def test_getScoreString_with0Dodges0TimeoutsScoreAndSpanish(self):
        preparedScore = PreparedAnivCopyMessageTimeoutScore(
            score = AnivCopyMessageTimeoutScore(
                mostRecentDodge = None,
                mostRecentTimeout = None,
                dodgeScore = 0,
                timeoutScore = 0,
                chatterUserId = 'abc123',
                twitchChannelId = 'def456',
            ),
            chatterUserName = 'stashiocat',
            twitchChannel = 'Oatsngoats',
        )

        printOut = await self.presenter.getScoreString(
            language = LanguageEntry.SPANISH,
            preparedScore = preparedScore,
        )

        assert printOut == f'ⓘ @{preparedScore.chatterUserName} no tiene suspensiones de aniv'

    def test_sanity(self):
        assert self.presenter is not None
        assert isinstance(self.presenter, AnivCopyMessageTimeoutScorePresenter)
        assert isinstance(self.presenter, AnivCopyMessageTimeoutScorePresenterInterface)
