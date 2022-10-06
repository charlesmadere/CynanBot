import asyncio

from CynanBotCommon.backingDatabase import BackingDatabase
from CynanBotCommon.trivia.triviaEmoteGenerator import TriviaEmoteGenerator
from CynanBotCommon.trivia.triviaAnswerCompiler import TriviaAnswerCompiler

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

asyncio.run(main())
