from CynanBot.aniv.anivCopyMessageTimeoutScore import \
    AnivCopyMessageTimeoutScore
from CynanBot.aniv.anivCopyMessageTimeoutScorePresenterInterface import \
    AnivCopyMessageTimeoutScorePresenterInterface


class AnivCopyMessageTimeoutScorePresenter(AnivCopyMessageTimeoutScorePresenterInterface):

    async def toString(self, score: AnivCopyMessageTimeoutScore) -> str:
        if not isinstance(score, AnivCopyMessageTimeoutScore):
            raise TypeError(f'score argument is malformed: \"{score}\"')

        if score.dodgeScore == 0 and score.timeoutScore == 0:
            return f'ⓘ @{score.chatterUserName} has no aniv timeouts'

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

        return f'@{score.chatterUserName}\'s aniv timeout scores — {dodgesString} and {timeoutsString} (that\'s a {dodgePercentString} dodge rate)'
