import asyncio
from datetime import timedelta

from CynanBotCommon.backingDatabase import BackingDatabase
from CynanBotCommon.trivia.triviaAnswerCompiler import TriviaAnswerCompiler
from CynanBotCommon.trivia.triviaEmoteGenerator import TriviaEmoteGenerator
from CynanBotCommon.trivia.triviaErrorDict import TriviaErrorDict
from CynanBotCommon.trivia.triviaSource import TriviaSource

backingDatabase = BackingDatabase()
triviaAnswerCompiler = TriviaAnswerCompiler()
triviaEmoteGenerator = TriviaEmoteGenerator(backingDatabase)

async def main():
    pass

    original = '👨🏾‍⚕️'
    emote = await triviaEmoteGenerator.getValidatedAndNormalizedEmote(original)
    print(f'{original}:{emote}')

    answer = await triviaAnswerCompiler.compileTextAnswer('5')
    print(f'answer="{answer}"')

    answer = await triviaAnswerCompiler.compileTextAnswer('-5')
    print(f'answer="{answer}"')

    fallOffTimeDelta = timedelta(milliseconds = 250)
    ted = TriviaErrorDict(fallOffTimeDelta)
    print(f'{ted.incrementErrorCount(TriviaSource.MILLIONAIRE)}')

    for triviaSource in TriviaSource:
        print(f'{triviaSource}:{ted[triviaSource]}')


asyncio.run(main())
