import asyncio
import json
from pathlib import Path
from tempfile import gettempdir
from typing import IO, Any

from aiofile import async_open

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

    await asyncio.sleep(3)
    pass


eventLoop.run_until_complete(doStuff())
