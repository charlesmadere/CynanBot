from .anivCopyMessageTimeoutScorePresenterInterface import AnivCopyMessageTimeoutScorePresenterInterface
from ..models.anivCopyMessageTimeoutScore import AnivCopyMessageTimeoutScore
from ...language.languageEntry import LanguageEntry
from ...misc import utils as utils


class AnivCopyMessageTimeoutScorePresenter(AnivCopyMessageTimeoutScorePresenterInterface):

    async def __english(
        self,
        score: AnivCopyMessageTimeoutScore | None,
        chatterUserName: str,
    ) -> str:
        if score is None or (score.dodgeScore == 0 and score.timeoutScore == 0):
            return f'ⓘ @{chatterUserName} has no aniv timeouts'

        dodgesString: str
        if score.dodgeScore == 1:
            dodgesString = f'{score.dodgeScoreStr} dodge'
        else:
            dodgesString = f'{score.dodgeScoreStr} dodges'

        timeoutsString: str
        if score.timeoutScore == 1:
            timeoutsString = f'{score.timeoutScoreStr} timeout'
        else:
            timeoutsString = f'{score.timeoutScoreStr} timeouts'

        dodgePercentString: str
        if score.dodgeScore == 0:
            dodgePercentString = '0%'
        elif score.timeoutScore == 0:
            dodgePercentString = '100%'
        else:
            totalDodgesAndTimeouts = score.dodgeScore + score.timeoutScore
            dodgePercent = round((float(score.dodgeScore) / float(totalDodgesAndTimeouts)) * float(100), 2)
            dodgePercentString = f'{dodgePercent}%'

        return f'ⓘ @{chatterUserName}\'s aniv timeout scores — {dodgesString} and {timeoutsString} (that\'s a {dodgePercentString} dodge rate)'

    async def getChannelEditorsCantPlayString(
        self,
        language: LanguageEntry,
    ) -> str:
        if not isinstance(language, LanguageEntry):
            raise TypeError(f'language argument is malformed: \"{language}\"')

        match language:
            case LanguageEntry.SPANISH:
                return 'ⓘ Lo sentimos, los moderadores editores no pueden participar en el juego de suspensiones de aniv'

            case _:
                return 'ⓘ Sorry, Twitch channel editors can\'t participate in the aniv timeout game'

    async def __spanish(
        self,
        score: AnivCopyMessageTimeoutScore | None,
        chatterUserName: str,
    ) -> str:
        if score is None or (score.dodgeScore == 0 and score.timeoutScore == 0):
            return f'ⓘ @{chatterUserName} no tiene suspensiones de aniv'

        dodgesString: str
        if score.dodgeScore == 1:
            dodgesString = f'{score.dodgeScoreStr} esquive'
        else:
            dodgesString = f'{score.dodgeScoreStr} esquives'

        timeoutsString: str
        if score.timeoutScore == 1:
            timeoutsString = f'{score.timeoutScoreStr} suspension'
        else:
            timeoutsString = f'{score.timeoutScoreStr} suspensiones'

        dodgePercentString: str
        if score.dodgeScore == 0:
            dodgePercentString = '0%'
        elif score.timeoutScore == 0:
            dodgePercentString = '100%'
        else:
            totalDodgesAndTimeouts = score.dodgeScore + score.timeoutScore
            dodgePercent = round((float(score.dodgeScore) / float(totalDodgesAndTimeouts)) * float(100), 2)
            dodgePercentString = f'{dodgePercent}%'

        return f'ⓘ el puntaje de suspension de aniv es @{chatterUserName} — {dodgesString} y {timeoutsString} (tasa de esquive de {dodgePercentString})'

    async def toString(
        self,
        score: AnivCopyMessageTimeoutScore | None,
        language: LanguageEntry,
        chatterUserName: str,
    ) -> str:
        if score is not None and not isinstance(score, AnivCopyMessageTimeoutScore):
            raise TypeError(f'score argument is malformed: \"{score}\"')
        elif not isinstance(language, LanguageEntry):
            raise TypeError(f'language argument is malformed: \"{language}\"')
        elif not utils.isValidStr(chatterUserName):
            raise TypeError(f'chatterUserName argument is malformed: \"{chatterUserName}\"')

        match language:
            case LanguageEntry.SPANISH:
                return await self.__spanish(
                    score = score,
                    chatterUserName = chatterUserName
                )

            case _:
                return await self.__english(
                    score = score,
                    chatterUserName = chatterUserName
                )
