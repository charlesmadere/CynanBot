import random

import CynanBot.misc.utils as utils
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.emotes.triviaEmoteGeneratorInterface import \
    TriviaEmoteGeneratorInterface
from CynanBot.trivia.emotes.triviaEmoteRepositoryInterface import \
    TriviaEmoteRepositoryInterface


class TriviaEmoteGenerator(TriviaEmoteGeneratorInterface):

    def __init__(
        self,
        timber: TimberInterface,
        triviaEmoteRepository: TriviaEmoteRepositoryInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber arguent is malformed: \"{timber}\"')
        elif not isinstance(triviaEmoteRepository, TriviaEmoteRepositoryInterface):
            raise TypeError(f'triviaEmoteRepository argument is malformed: \"{triviaEmoteRepository}\"')

        self.__timber: TimberInterface = timber
        self.__triviaEmoteRepository: TriviaEmoteRepositoryInterface = triviaEmoteRepository

        self.__emotesDict: dict[str, set[str] | None] = self.__createEmotesDict()
        self.__emotesList: list[str] = list(self.__emotesDict)

    def __createEmotesDict(self) -> dict[str, set[str] | None]:
        # Creates and returns a dictionary of emojis, with a set of emojis that should be
        # considered equivalent. For example: 👨‍🔬 (man scientist) and 👩‍🔬 (woman scientist)
        # should both be considered equivalents of the primary "root" 🧑‍🔬 (scientist) emoji.
        #
        # If a set is either None or empty, then the given emoji has no equivalent.

        emotesDict: dict[str, set[str] | None] = dict()
        emotesDict['🧮'] = None
        emotesDict['👽'] = None
        emotesDict['👾'] = None
        emotesDict['🥑'] = None
        emotesDict['🥓'] = None
        emotesDict['🎒'] = None
        emotesDict['🍌'] = None
        emotesDict['📊'] = None
        emotesDict['🏖️'] = { '⛱️', '☂️', '☔' }
        emotesDict['🫑'] = None
        emotesDict['🐦'] = { '🐤' }
        emotesDict['🎂'] = { '🍰' }
        emotesDict['🫐'] = None
        emotesDict['📚'] = None
        emotesDict['💼'] = None
        emotesDict['🚌'] = None
        emotesDict['🐪'] = { '🐫' }
        emotesDict['🍬'] = { '🍭' }
        emotesDict['📇'] = None
        emotesDict['🥕'] = None
        emotesDict['🧀'] = None
        emotesDict['🍒'] = None
        emotesDict['🏛️'] = { '🏦' }
        emotesDict['📋'] = None
        emotesDict['💽'] = { '📀', '💿' }
        emotesDict['🍪'] = { '🥠' }
        emotesDict['🐄'] = { '🐮', '🐂', '🐃' }
        emotesDict['🦀'] = None
        emotesDict['🖍️'] = None
        emotesDict['🧁'] = None
        emotesDict['🍛'] = None
        emotesDict['🖥️'] = { '💻' }
        emotesDict['🧬'] = None
        emotesDict['🐬'] = None
        emotesDict['🐉'] = { '🐲', '🦖' }
        emotesDict['🔌'] = { '⚡' }
        emotesDict['🐘'] = None
        emotesDict['🧐'] = None
        emotesDict['🚒'] = None
        emotesDict['🐟'] = { '🐡', '🎣', '🐠' }
        emotesDict['💾'] = None
        emotesDict['🐸'] = None
        emotesDict['👻'] = None
        emotesDict['🍇'] = None
        emotesDict['🍏'] = None
        emotesDict['🚁'] = None
        emotesDict['🐎'] = { '🐴' }
        emotesDict['🌶️'] = None
        emotesDict['🎃'] = None
        emotesDict['📒'] = { '📔', '🗒️' }
        emotesDict['💡'] = None
        emotesDict['🦁'] = None
        emotesDict['🕰️'] = None
        emotesDict['🍈'] = { '🍉' }
        emotesDict['🔬'] = { '⚗️' }
        emotesDict['🐒'] = { '🐵' }
        emotesDict['🍄'] = None
        emotesDict['🤓'] = None
        emotesDict['📓'] = None
        emotesDict['📦'] = { '🪤' }
        emotesDict['📎'] = None
        emotesDict['🍐'] = None
        emotesDict['🐧'] = None
        emotesDict['🥧'] = None
        emotesDict['🐖'] = { '🐷', '🐗' }
        emotesDict['🍍'] = None
        emotesDict['🍕'] = None
        emotesDict['🍿'] = { '🌽' }
        emotesDict['🧩'] = None
        emotesDict['🥔'] = None
        emotesDict['🍎'] = None
        emotesDict['🌈'] = None
        emotesDict['🍙'] = None
        emotesDict['🍠'] = None
        emotesDict['🤖'] = None
        emotesDict['🚀'] = None
        emotesDict['🏫'] = None
        emotesDict['🦐'] = { '🍤' }
        emotesDict['🐚'] = None
        emotesDict['🦑'] = { '🐙' }
        emotesDict['📏'] = None
        emotesDict['🍓'] = None
        emotesDict['🍊'] = None
        emotesDict['🔭'] = None
        emotesDict['🤔'] = None
        emotesDict['💭'] = None
        emotesDict['🐅'] = { '🐯' }
        emotesDict['🎩'] = None
        emotesDict['📐'] = None
        emotesDict['🎺'] = { '📯' }
        emotesDict['🌷'] = { '🌹' }
        emotesDict['🐢'] = None
        emotesDict['🌊'] = { '💧', '💦' }
        emotesDict['🐋'] = { '🐳' }

        return emotesDict

    async def getCurrentEmoteFor(self, twitchChannelId: str) -> str:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        emoteIndex = await self.__getCurrentEmoteIndexFor(twitchChannelId)
        return self.__emotesList[emoteIndex]

    async def __getCurrentEmoteIndexFor(self, twitchChannelId: str) -> int:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        emoteIndex = await self.__triviaEmoteRepository.getEmoteIndexFor(twitchChannelId)

        if not utils.isValidInt(emoteIndex) or emoteIndex < 0 or emoteIndex >= len(self.__emotesList):
            self.__timber.log('TriviaEmoteGenerator', f'emoteIndex value for {twitchChannelId=} is out of bounds or uninitialized ({emoteIndex=})')
            emoteIndex = 0

        return emoteIndex

    async def getNextEmoteFor(self, twitchChannelId: str) -> str:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        currentEmoteIndex = await self.__getCurrentEmoteIndexFor(twitchChannelId)
        newEmoteIndex = (currentEmoteIndex + 1) % len(self.__emotesList)

        await self.__triviaEmoteRepository.setEmoteIndexFor(
            emoteIndex = newEmoteIndex,
            twitchChannelId = twitchChannelId
        )

        return self.__emotesList[newEmoteIndex]

    def getRandomEmote(self) -> str:
        return random.choice(self.__emotesList)

    async def getValidatedAndNormalizedEmote(self, emote: str | None) -> str | None:
        if emote is not None and not isinstance(emote, str):
            raise TypeError(f'emote argument is malformed: \"{emote}\"')

        if not utils.isValidStr(emote):
            return None

        if emote in self.__emotesDict:
            return emote

        for emoteKey, equivalentEmotes in self.__emotesDict.items():
            if equivalentEmotes is not None and len(equivalentEmotes) >= 1 and emote in equivalentEmotes:
                return emoteKey

        return None
