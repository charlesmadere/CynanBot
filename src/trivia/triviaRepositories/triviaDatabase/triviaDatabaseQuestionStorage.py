from .triviaDatabaseQuestionStorageInterface import TriviaDatabaseQuestionStorageInterface
from .triviaDatabaseTriviaQuestion import TriviaDatabaseTriviaQuestion
from ....misc import utils as utils
from ....timber.timberInterface import TimberInterface


class TriviaDatabaseQuestionStorage(TriviaDatabaseQuestionStorageInterface):

    def __init__(
        self,
        timber: TimberInterface,
        databaseFile: str = 'triviaDatabaseTriviaQuestionRepository.sqlite'
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidStr(databaseFile):
            raise TypeError(f'databaseFile argument is malformed: \"{databaseFile}\"')

        self.__timber: TimberInterface = timber
        self.__databaseFile: str = databaseFile

        self.__hasQuestionSetAvailable: bool | None = None

    async def fetchTriviaQuestion(self) -> TriviaDatabaseTriviaQuestion:
        raise RuntimeError()

    async def hasQuestionSetAvailable(self) -> bool:
        raise RuntimeError()
