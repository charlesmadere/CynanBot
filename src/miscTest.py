import asyncio
import re
from typing import Any, Optional, Pattern

from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.timber.timberStub import TimberStub
from CynanBot.trivia.compilers.triviaAnswerCompiler import TriviaAnswerCompiler
from CynanBot.trivia.compilers.triviaAnswerCompilerInterface import \
    TriviaAnswerCompilerInterface

timber: TimberInterface = TimberStub()
triviaAnswerCompiler: TriviaAnswerCompilerInterface = TriviaAnswerCompiler(timber = timber)

eventLoop = asyncio.get_event_loop()

async def main():
    pass
    result = await triviaAnswerCompiler.compileTextAnswersList([ 'Garfield the cat' ])
    print(f'result=\"{result}\"')
    pass

eventLoop.run_until_complete(main())
