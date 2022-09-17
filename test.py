import asyncio

from CynanBotCommon.backingDatabase import BackingDatabase
from CynanBotCommon.trivia.triviaEmoteGenerator import TriviaEmoteGenerator

backingDatabase = BackingDatabase()
triviaEmoteGenerator = TriviaEmoteGenerator(backingDatabase)

async def main():
    pass

    original = '👨🏾‍⚕️'
    emote = await triviaEmoteGenerator.getValidatedAndNormalizedEmote(original)
    print(f'{original}:{emote}')

    print(await triviaEmoteGenerator.getNextEmoteFor('blah'))

asyncio.run(main())
