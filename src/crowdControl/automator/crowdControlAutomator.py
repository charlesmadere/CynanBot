from .crowdControlAutomatorData import CrowdControlAutomatorData
from .crowdControlAutomatorInterface import CrowdControlAutomatorInterface
from ..crowdControlMachineInterface import CrowdControlMachineInterface
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...timber.timberInterface import TimberInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ...users.usersRepositoryInterface import UsersRepositoryInterface


class CrowdControlAutomator(CrowdControlAutomatorInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        crowdControlMachine: CrowdControlMachineInterface,
        timber: TimberInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(crowdControlMachine, CrowdControlMachineInterface):
            raise TypeError(f'crowdControlMachine argument is malformed: \"{crowdControlMachine}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__crowdControlMachine: CrowdControlMachineInterface = crowdControlMachine
        self.__timber: TimberInterface = timber
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository

        self.__isStarted: bool = False
        self.__automatorData: dict[str, CrowdControlAutomatorData | None] = dict()

    async def applyGameShuffleAutomator(self, automatorData: CrowdControlAutomatorData):
        if not isinstance(automatorData, CrowdControlAutomatorData):
            raise TypeError(f'automatorData argument is malformed: \"{automatorData}\"')

        # TODO
        pass

    def start(self):
        if self.__isStarted:
            self.__timber.log('CrowdControlAutomator', 'Not starting CrowdControlAutomator as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('CrowdControlAutomator', 'Starting CrowdControlAutomator...')
        self.__backgroundTaskHelper.createTask(self.__startRefreshLoop())

    async def __startRefreshLoop(self):
        # TODO
        pass

    async def stopGameShuffleAutomator(self, twitchChannelId: str):
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        # TODO
        pass
