import asyncio
import json
from pathlib import Path
from tempfile import gettempdir
from typing import IO, Any, Dict, List

from aiofile import async_open

import CynanBotCommon.utils as utils
from CynanBotCommon.trivia.triviaAnswerCompiler import TriviaAnswerCompiler

fileName = 'authRepository.json'
triviaAnswerCompiler = TriviaAnswerCompiler()
eventLoop = asyncio.get_event_loop()

async def doStuff():
    jsonContents = None

    async with async_open(fileName, 'r') as file:
        data = await file.read()
        jsonContents = json.loads(data)

    print(jsonContents)

    result = await triviaAnswerCompiler.compileTextAnswers([
        '(Justice) Roberts'
    ])
    print(result)

    result = await triviaAnswerCompiler.compileTextAnswer('<b>an bean bag chairs</b>\n\n')
    print(f'\"{result}\"')

    dictionary: List[Dict[str, object]] = {'id': 90431, 'answer': '<i>Brigadoon</i>', 'question': '"Almost Like Being In Love","I\'ll Go Home With Bonnie Jean"', 'value': 400, 'airdate': '2009-03-17T12:00:00.000Z', 'created_at': '2014-02-14T01:56:08.785Z', 'updated_at': '2014-02-14T01:56:08.785Z', 'category_id': 11951, 'game_id': None, 'invalid_count': None, 'category': {'id': 11951, 'title': 'shows by show tunes', 'created_at': '2014-02-14T01:56:08.399Z', 'updated_at': '2014-02-14T01:56:08.399Z', 'clues_count': 5}}
    answer = '<i>Brigadoon</i>'
    cleanedAnswer = utils.getStrFromDict(dictionary, 'answer', clean = True, removeCarrots = True)
    print(f'{answer}, {cleanedAnswer}, {utils.cleanStr(answer, removeCarrots = True)}')

    await asyncio.sleep(3)
    pass


eventLoop.run_until_complete(doStuff())
