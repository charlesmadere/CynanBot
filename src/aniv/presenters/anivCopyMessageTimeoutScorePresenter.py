from .anivCopyMessageTimeoutScorePresenterInterface import AnivCopyMessageTimeoutScorePresenterInterface
from ..models.preparedAnivCopyMessageTimeoutScore import PreparedAnivCopyMessageTimeoutScore
from ...language.languageEntry import LanguageEntry


class AnivCopyMessageTimeoutScorePresenter(AnivCopyMessageTimeoutScorePresenterInterface):

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

    async def getScoreString(
        self,
        language: LanguageEntry,
        preparedScore: PreparedAnivCopyMessageTimeoutScore,
    ) -> str:
        if not isinstance(language, LanguageEntry):
            raise TypeError(f'language argument is malformed: \"{language}\"')
        elif not isinstance(preparedScore, PreparedAnivCopyMessageTimeoutScore):
            raise TypeError(f'preparedScore argument is malformed: \"{preparedScore}\"')

        match language:
            case LanguageEntry.SPANISH:
                return await self.__getScoreStringSpanish(
                    preparedScore = preparedScore,
                )

            case _:
                return await self.__getScoreStringEnglish(
                    preparedScore = preparedScore,
                )

    async def __getScoreStringEnglish(
        self,
        preparedScore: PreparedAnivCopyMessageTimeoutScore,
    ) -> str:
        if preparedScore.dodgeScore == 0 and preparedScore.timeoutScore == 0:
            return f'ⓘ @{preparedScore.chatterUserName} has no aniv timeouts'

        dodgesString: str
        if preparedScore.dodgeScore == 1:
            dodgesString = f'{preparedScore.dodgeScoreStr} dodge'
        else:
            dodgesString = f'{preparedScore.dodgeScoreStr} dodges'

        timeoutsString: str
        if preparedScore.timeoutScore == 1:
            timeoutsString = f'{preparedScore.timeoutScoreStr} timeout'
        else:
            timeoutsString = f'{preparedScore.timeoutScoreStr} timeouts'

        dodgePercentString: str
        if preparedScore.dodgeScore == 0:
            dodgePercentString = '0%'
        elif preparedScore.timeoutScore == 0:
            dodgePercentString = '100%'
        else:
            totalDodgesAndTimeouts = preparedScore.dodgeScore + preparedScore.timeoutScore
            dodgePercent = round((float(preparedScore.dodgeScore) / float(totalDodgesAndTimeouts)) * float(100), 2)
            dodgePercentString = f'{dodgePercent}%'

        return f'ⓘ @{preparedScore.chatterUserName}\'s aniv timeout scores — {dodgesString} and {timeoutsString} (that\'s a {dodgePercentString} dodge rate)'

    async def __getScoreStringSpanish(
        self,
        preparedScore: PreparedAnivCopyMessageTimeoutScore,
    ) -> str:
        if preparedScore.dodgeScore == 0 and preparedScore.timeoutScore == 0:
            return f'ⓘ @{preparedScore.chatterUserName} no tiene suspensiones de aniv'

        dodgesString: str
        if preparedScore.dodgeScore == 1:
            dodgesString = f'{preparedScore.dodgeScoreStr} esquive'
        else:
            dodgesString = f'{preparedScore.dodgeScoreStr} esquives'

        timeoutsString: str
        if preparedScore.timeoutScore == 1:
            timeoutsString = f'{preparedScore.timeoutScoreStr} suspension'
        else:
            timeoutsString = f'{preparedScore.timeoutScoreStr} suspensiones'

        dodgePercentString: str
        if preparedScore.dodgeScore == 0:
            dodgePercentString = '0%'
        elif preparedScore.timeoutScore == 0:
            dodgePercentString = '100%'
        else:
            totalDodgesAndTimeouts = preparedScore.dodgeScore + preparedScore.timeoutScore
            dodgePercent = round((float(preparedScore.dodgeScore) / float(totalDodgesAndTimeouts)) * float(100), 2)
            dodgePercentString = f'{dodgePercent}%'

        return f'ⓘ el puntaje de suspension de aniv es @{preparedScore.chatterUserName} — {dodgesString} y {timeoutsString} (tasa de esquive de {dodgePercentString})'
