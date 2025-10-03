import asyncio
import csv
import hashlib
import sqlite3
from asyncio import AbstractEventLoop

import src.misc.utils as utils
from src.contentScanner.bannedWord import BannedWord
from src.contentScanner.bannedWordsRepository import BannedWordsRepository
from src.contentScanner.bannedWordsRepositoryInterface import BannedWordsRepositoryInterface
from src.contentScanner.contentScanner import ContentScanner
from src.contentScanner.contentScannerInterface import ContentScannerInterface
from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.misc.backgroundTaskHelper import BackgroundTaskHelper
from src.misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from src.storage.jsonFileReader import JsonFileReader
from src.storage.linesFileReader import LinesFileReader
from src.timber.timber import Timber
from src.timber.timberInterface import TimberInterface
from src.trivia.content.triviaContentScanner import TriviaContentScanner
from src.trivia.content.triviaContentScannerInterface import TriviaContentScannerInterface
from src.trivia.misc.triviaSourceParser import TriviaSourceParser
from src.trivia.misc.triviaSourceParserInterface import TriviaSourceParserInterface
from src.trivia.questions.triviaQuestionType import TriviaQuestionType
from src.trivia.settings.triviaSettingsRepository import TriviaSettingsRepository
from src.trivia.settings.triviaSettingsRepositoryInterface import TriviaSettingsRepositoryInterface
from src.trivia.triviaDifficulty import TriviaDifficulty

eventLoop: AbstractEventLoop = asyncio.get_event_loop()

backgroundTaskHelper: BackgroundTaskHelperInterface = BackgroundTaskHelper(
    eventLoop = eventLoop,
)

timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

timber: TimberInterface = Timber(
    backgroundTaskHelper = backgroundTaskHelper,
    timeZoneRepository = timeZoneRepository,
)

triviaSourceParser: TriviaSourceParserInterface = TriviaSourceParser()

triviaSettingsRepository: TriviaSettingsRepositoryInterface = TriviaSettingsRepository(
    settingsJsonReader = JsonFileReader(
        eventLoop = eventLoop,
        fileName = 'triviaSettingsRepository.json',
    ),
    triviaSourceParser = triviaSourceParser,
)

bannedWordsRepository: BannedWordsRepositoryInterface = BannedWordsRepository(
    bannedWordsLinesReader = LinesFileReader(
        eventLoop = eventLoop,
        fileName = 'bannedWords.txt',
    ),
    timber = timber,
)

contentScanner: ContentScannerInterface = ContentScanner(
    bannedWordsRepository = bannedWordsRepository,
    timber = timber,
)

triviaContentScanner: TriviaContentScannerInterface = TriviaContentScanner(
    bannedWordsRepository = bannedWordsRepository,
    contentScanner = contentScanner,
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository,
)

def readInCsvRows(fileName: str) -> list[list[str]]:
    if not utils.isValidStr(fileName):
        raise ValueError(f'fileName argument is malformed: \"{fileName}\"')

    bannedWords = bannedWordsRepository.getBannedWords()
    rows: list[list[str]] = list()

    with open(fileName) as file:
        reader = csv.reader(file, delimiter = ',')
        lineNumber: int = 0

        for row in reader:
            lineNumber = lineNumber + 1

            if not utils.hasItems(row):
                print(f'Row #{lineNumber} in \"{fileName}\" is null/empty: {row}')
                continue

            encounteredBannedWord = False

            for r in row:
                for bannedWord in bannedWords:
                    if isinstance(bannedWord, BannedWord) and bannedWord.word in r.lower():
                        encounteredBannedWord = True
                        break

                if encounteredBannedWord:
                    break

            if encounteredBannedWord:
                raise RuntimeError(f'Row #{lineNumber} in \"{fileName}\" contains a banned word: {row}')
            else:
                rows.append(row)

    if not utils.hasItems(rows):
        raise RuntimeError(f'Unable to read in any rows from \"{fileName}\": {rows}')

    print(f'Read in {len(rows)} row(s) from \"{fileName}\"')
    return rows

def writeRowsToSqlite(databaseName: str, rows: list[list[str]]):
    if not utils.isValidStr(databaseName):
        raise ValueError(f'databaseName argument is malformed: \"{databaseName}\"')
    elif not utils.hasItems(rows):
        raise ValueError(f'rows argument is malformed: \"{rows}\"')

    connection = sqlite3.connect(databaseName)
    cursor = connection.cursor()
    questionIds: set[str] = set()
    rowNumber: int = 0

    for row in rows:
        rowNumber = rowNumber + 1

        if not utils.hasItems(row):
            raise ValueError(f'Row #{rowNumber} is null/empty: {row}')

        originalQuestionId: str = utils.cleanStr(row[0])
        category: str = utils.cleanStr(row[1])
        subCategory: str = utils.cleanStr(row[2])
        question: str = utils.cleanStr(row[4])
        correctAnswerIndex: int = int(row[9]) - 1

        response0: str | None = None
        response1: str | None = None
        response2: str | None = None
        response3: str | None = None
        questionType: TriviaQuestionType | None = None

        try:
            if len(row) > 5:
                response0 = utils.cleanStr(row[5])
                response1 = utils.cleanStr(row[6])
                response2 = utils.cleanStr(row[7])
                response3 = utils.cleanStr(row[8])
                questionType = TriviaQuestionType.MULTIPLE_CHOICE
            elif len(row) == 5:
                questionType = TriviaQuestionType.TRUE_FALSE
            else:
                raise ValueError(f'triviaType at row #{rowNumber} can\'t be determined: \"{questionType}\"')
        except IndexError as e:
            raise ValueError(f'index error at row #{rowNumber}: {e}')

        difficulty: TriviaDifficulty = TriviaDifficulty.UNKNOWN
        try:
            difficulty = TriviaDifficulty.fromInt(int(row[3]))
        except ValueError as e:
            raise ValueError(f'difficulty at row #{rowNumber} is malformed: {row}: {e}')

        if not utils.isValidStr(originalQuestionId):
            raise ValueError(f'originalQuestionId at row #{rowNumber} is malformed: \"{originalQuestionId}\"')
        elif not utils.isValidStr(category):
            raise ValueError(f'category at row #{rowNumber} is malformed: \"{category}\"')
        elif not utils.isValidStr(subCategory):
            raise ValueError(f'subCategory at row #{rowNumber} is malformed: \"{subCategory}\"')
        elif not utils.isValidStr(question):
            raise ValueError(f'question at row #{rowNumber} is malformed: \"{question}\"')
        elif not utils.isValidInt(correctAnswerIndex) or correctAnswerIndex < 0 or correctAnswerIndex > 3:
            raise ValueError(f'correctAnswerIndex at row #{rowNumber} is malformed: \"{correctAnswerIndex}\"')
        elif not isinstance(difficulty, TriviaDifficulty):
            raise ValueError(f'difficulty at row #{rowNumber} is malformed: \"{difficulty}\"')
        elif not isinstance(questionType, TriviaQuestionType):
            raise ValueError(f'questionType at row #{rowNumber} is malformed: \"{questionType}\"')
        elif questionType is TriviaQuestionType.MULTIPLE_CHOICE and (not utils.isValidStr(response0) or not utils.isValidStr(response1) or not utils.isValidStr(response2) or not utils.isValidStr(response3)):
            raise ValueError(f'questionType {TriviaQuestionType.MULTIPLE_CHOICE} at row #{rowNumber} has malformed wrong answers (response0=\"{response0}\") (response1=\"{response1}\") (response2=\"{response2}\") (response3=\"{response3}\")')
        elif questionType is TriviaQuestionType.TRUE_FALSE:
            raise NotImplementedError(f'questionType {TriviaQuestionType.TRUE_FALSE} at row #{rowNumber} is not implemented yet')

        questionId: str = f'{originalQuestionId}:{category}:{difficulty.toStr()}:{questionType.toStr()}:{question}:{response0}:{response2}:{response3}:{correctAnswerIndex}'
        questionId = hashlib.md5(questionId.encode('utf-8')).hexdigest()

        if not utils.isValidStr(questionId):
            raise ValueError(f'questionId at row #{rowNumber} is malformed: \"{questionId}\"')
        elif questionId in questionIds:
            raise RuntimeError(f'questionId at row #{rowNumber} has collision: \"{questionId}\"')

        questionIds.add(questionId)

        try:
            cursor.execute(
                '''
                    INSERT INTO tqcQuestions (category, correctAnswerIndex, difficulty, originalQuestionId, question, questionId, questionType, response0, response1, response2, response3, subCategory)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
                ''',
                ( category, correctAnswerIndex, difficulty.toInt(), originalQuestionId, question, questionId, questionType.toStr(), response0, response1, response2, response3, subCategory )
            )
        except (sqlite3.IntegrityError, sqlite3.OperationalError) as e:
            raise RuntimeError(f'Unable to insert question into DB: {e}\ncategory=\"{category}\" correctAnswerIndex=\"{correctAnswerIndex}\" difficulty=\"{difficulty}\" question=\"{question}\" questionId=\"{questionId}\" originalQuestionId=\"{originalQuestionId}\" triviaType=\"{questionType}\" response0=\"{response0}\" response1=\"{response1}\" response2=\"{response2}\" response3=\"{response3}\": {e}')

    connection.commit()
    cursor.close()
    connection.close()

    print(f'Wrote {rowNumber} rows into \"{databaseName}\" database')


multipleChoice = readInCsvRows('questions.csv')
writeRowsToSqlite('lotr.sqlite', multipleChoice)
