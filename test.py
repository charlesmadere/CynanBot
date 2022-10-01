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

    connection = await backingDatabase.getConnection()
    await connection.execute(
        '''
            ALTER TABLE triviaScores
            RENAME COLUMN totalLosses TO triviaLosses
        '''
    )

    await connection.execute(
        '''
            ALTER TABLE triviaScores
            RENAME COLUMN totalWins TO triviaWins
        '''
    )

    cursor = await connection.execute(
        '''
            SELECT streak, superTriviaWins, triviaLosses, triviaWins, twitchChannel, userId FROM triviaScores
            ORDER BY twitchChannel ASC
        '''
    )

    rows = await cursor.fetchall()

    for row in rows:
        streak: str = row[0]
        superTriviaWins: int = row[1]
        triviaLosses: int = row[2]
        triviaWins: int = row[3]
        twitchChannel: str = row[4]
        userId: str = row[5]

        newTriviaWins: int = triviaWins - superTriviaWins

        await cursor.execute(
            '''
                UPDATE triviaScores
                SET streak = ?, superTriviaWins = ?, triviaLosses = ?, triviaWins = ?
                WHERE twitchChannel = ? AND userId = ?
            ''',
            ( streak, superTriviaWins, triviaLosses, newTriviaWins, twitchChannel, userId )
        )

    await connection.commit()
    await cursor.close()
    await connection.close()

asyncio.run(main())
