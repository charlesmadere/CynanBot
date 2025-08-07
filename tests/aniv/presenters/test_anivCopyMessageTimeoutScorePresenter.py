import pytest

from src.aniv.models.anivCopyMessageTimeoutScore import AnivCopyMessageTimeoutScore
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

    def test_sanity(self):
        assert self.presenter is not None
        assert isinstance(self.presenter, AnivCopyMessageTimeoutScorePresenter)
        assert isinstance(self.presenter, AnivCopyMessageTimeoutScorePresenterInterface)

    @pytest.mark.asyncio
    async def test_toString_with0Dodges0TimeoutsScoreAndEnglish(self):
        chatterUserName = 'stashiocat'

        score = AnivCopyMessageTimeoutScore(
            mostRecentDodge = None,
            mostRecentTimeout = None,
            dodgeScore = 0,
            timeoutScore = 0,
            chatterUserId = 'abc123',
            chatterUserName = chatterUserName,
            twitchChannel = 'smCharles',
            twitchChannelId = 'def456'
        )

        printOut = await self.presenter.toString(
            score = score,
            language = LanguageEntry.ENGLISH,
            chatterUserName = 'stashiocat'
        )

        assert printOut == f'ⓘ @{chatterUserName} has no aniv timeouts'

    @pytest.mark.asyncio
    async def test_toString_with0Dodges0TimeoutsScoreAndSpanish(self):
        chatterUserName = 'stashiocat'

        score = AnivCopyMessageTimeoutScore(
            mostRecentDodge = None,
            mostRecentTimeout = None,
            dodgeScore = 0,
            timeoutScore = 0,
            chatterUserId = 'abc123',
            chatterUserName = chatterUserName,
            twitchChannel = 'smCharles',
            twitchChannelId = 'def456'
        )

        printOut = await self.presenter.toString(
            score = score,
            language = LanguageEntry.SPANISH,
            chatterUserName = chatterUserName
        )

        assert printOut == f'ⓘ @{chatterUserName} no tiene suspensiones de aniv'
