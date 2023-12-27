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
    result = await triviaAnswerCompiler.compileTextAnswersList('Garfield the cat')
    print(f'result=\"{result}\"')
    pass

eventLoop.run_until_complete(main())

# wordTheWordRegEx: Pattern = re.compile(r'^(\w+)\s+(a|an|the)\s+(\w+)$', re.IGNORECASE)
# match = wordTheWordRegEx.fullmatch('Silvervale of twitch')
# print(match)

# if match is not None:
#     print(match.group())
#     print(match.group(1))
#     print(match.group(2))
#     print(match.group(3))
#     answer = f'{match.group(1)} ({match.group(2)}) {match.group(3)}'
#     print(answer)
