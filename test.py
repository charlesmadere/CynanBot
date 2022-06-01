import asyncio
import json
from pathlib import Path
from tempfile import gettempdir
from typing import IO, Any, Dict, List

from aiofile import async_open

import CynanBotCommon.utils as utils
from CynanBotCommon.timber.timber import Timber
from CynanBotCommon.trivia.questionAnswerTriviaQuestion import \
    QuestionAnswerTriviaQuestion
from CynanBotCommon.trivia.triviaAnswerChecker import TriviaAnswerChecker
from CynanBotCommon.trivia.triviaAnswerCompiler import TriviaAnswerCompiler
from CynanBotCommon.trivia.triviaDifficulty import TriviaDifficulty
from CynanBotCommon.trivia.triviaSettingsRepository import \
    TriviaSettingsRepository
from CynanBotCommon.trivia.triviaSource import TriviaSource

eventLoop = asyncio.get_event_loop()
timber = Timber(eventLoop = eventLoop)
triviaSettingsRepository = TriviaSettingsRepository()

fileName = 'authRepository.json'

triviaAnswerCompiler = TriviaAnswerCompiler()
triviaAnswerChecker = TriviaAnswerChecker(
    timber = timber,
    triviaAnswerCompiler = triviaAnswerCompiler,
    triviaSettingsRepository = triviaSettingsRepository
)
triviaQuestion = QuestionAnswerTriviaQuestion(
    correctAnswers = [ 'boars' ],
    cleanedCorrectAnswers = [ 'boars' ],
    category = 'Animals',
    question = 'What is another name for a pig?',
    triviaId = 'abc123',
    triviaDifficulty = TriviaDifficulty.UNKNOWN,
    triviaSource = TriviaSource.J_SERVICE
)

async def doStuff():
    result = await triviaAnswerChecker.checkAnswer(
        answer = 'Boar',
        triviaQuestion = triviaQuestion
    )

    print(f'result: \"{result}\"')

    await asyncio.sleep(3)
    pass


eventLoop.run_until_complete(doStuff())
