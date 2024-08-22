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
        if not await aiofiles.ospath.exists(self.__triviaDatabaseFile):
            raise FileNotFoundError(f'Trivia Database trivia database file not found: \"{self.__triviaDatabaseFile}\"')

        connection = await aiosqlite.connect(self.__triviaDatabaseFile)
        cursor = await connection.execute(
            '''
                SELECT category, correctAnswer, difficulty, question, questionId, triviaType, wrongAnswer1, wrongAnswer2, wrongAnswer3 FROM tdQuestions
                ORDER BY RANDOM()
                LIMIT 1
            '''
        )

        row = await cursor.fetchone()
        if not utils.hasItems(row) or len(row) != 9:
            raise RuntimeError(f'Received malformed data from {self.triviaSource} database: {row}')

        triviaQuestionDict: dict[str, Any] = {
            'category': row[0],
            'correctAnswer': row[1],
            'difficulty': row[2],
            'question': row[3],
            'triviaId': row[4],
            'type': row[5],
            'wrongAnswers': [ row[6], row[7], row[8] ]
        }

        await cursor.close()
        await connection.close()
        return triviaQuestionDict

    async def hasQuestionSetAvailable(self) -> bool:
        if self.__hasQuestionSetAvailable is not None:
            return self.__hasQuestionSetAvailable

        hasQuestionSetAvailable = await aiofiles.ospath.exists(self.__triviaDatabaseFile)
        self.__hasQuestionSetAvailable = hasQuestionSetAvailable

        return hasQuestionSetAvailable
