from .beanStatsPresenterInterface import BeanStatsPresenterInterface
from .chatterBeanStats import ChatterBeanStats


class BeanStatsPresenter(BeanStatsPresenterInterface):

    async def toString(self, beanStats: ChatterBeanStats) -> str:
        if not isinstance(beanStats, ChatterBeanStats):
            raise TypeError(f'beanStats argument is malformed: \"{beanStats}\"')

        if beanStats.failedBeanAttempts == 0 and beanStats.successfulBeans == 0:
            return f'ⓘ @{beanStats.chatterUserName} has no bean attempts'

        successesString: str
        if beanStats.successfulBeans == 1:
            successesString = f'{beanStats.successfulBeansStr} bean'
        else:
            successesString = f'{beanStats.successfulBeansStr} beans'

        failsString: str
        if beanStats.failedBeanAttempts == 1:
            failsString = f'{beanStats.failedBeanAttemptsStr} fail'
        else:
            failsString = f'{beanStats.failedBeanAttemptsStr} fails'

        successPercentString: str
        if beanStats.successfulBeans == 0:
            successPercentString = '0%'
        elif beanStats.failedBeanAttempts == 0:
            successPercentString = '100%'
        else:
            totalSuccessesAndFails = beanStats.successfulBeans + beanStats.failedBeanAttempts
            successPercent = round((float(beanStats.successfulBeans) / float(totalSuccessesAndFails)) * float(100), 2)
            successPercentString = f'{successPercent}%'

        return f'ⓘ @{beanStats.chatterUserName}\'s bean scores — {successesString} and {failsString} (that\'s a {successPercentString} success rate)'
