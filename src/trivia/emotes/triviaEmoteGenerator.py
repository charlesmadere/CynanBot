import random
from typing import Final

from frozendict import frozendict
from frozenlist import FrozenList

from .triviaEmoteGeneratorInterface import TriviaEmoteGeneratorInterface
from .triviaEmoteRepositoryInterface import TriviaEmoteRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class TriviaEmoteGenerator(TriviaEmoteGeneratorInterface):

    def __init__(
        self,
        timber: TimberInterface,
        triviaEmoteRepository: TriviaEmoteRepositoryInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaEmoteRepository, TriviaEmoteRepositoryInterface):
            raise TypeError(f'triviaEmoteRepository argument is malformed: \"{triviaEmoteRepository}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__triviaEmoteRepository: Final[TriviaEmoteRepositoryInterface] = triviaEmoteRepository

        self.__emojiToEquivalents: Final[frozendict[str, frozenset[str] | None]] = self.__createEmojiToEquivalentsDictionary()
        self.__emojiEquivalents: Final[FrozenList[str]] = FrozenList(self.__emojiToEquivalents)
        self.__emojiEquivalents.freeze()

    def __createEmojiToEquivalentsDictionary(self) -> frozendict[str, frozenset[str] | None]:
        # Creates and returns a dictionary of emojis, with a set of emojis that should be
        # considered equivalent. For example: 👨‍🔬 (man scientist) and 👩‍🔬 (woman scientist)
        # should both be considered equivalents of the primary "root" 🧑‍🔬 (scientist) emoji.
        #
        # If a set is either None or empty, then the given emoji has no equivalent.

        return frozendict({
            '🧮': None,
            '👽': None,
            '👾': None,
            '🎨': None,
            '🥑': None,
            '🥓': None,
            '🎒': None,
            '🍌': None,
            '📊': None,
            '🔋': frozenset({'🪫'}),
            '🏖️': frozenset({'⛱️', '☂️', '☔'}),
            '🦫': None,
            '🫑': None,
            '🐦': frozenset({'🐤'}),
            '🎂': frozenset({'🍰'}),
            '🫐': None,
            '📚': None,
            '💼': None,
            '🥦': None,
            '🚌': None,
            '🐪': frozenset({'🐫'}),
            '🍬': frozenset({'🍭'}),
            '📇': None,
            '🎏': None,
            '🖼️': frozenset({'🏞️'}),
            '🥕': None,
            '🧀': None,
            '🍒': None,
            '🥢': None,
            '🏛️': frozenset({'🏦'}),
            '📋': None,
            '💽': frozenset({'📀', '💿'}),
            '🍪': frozenset({'🥠'}),
            '🐄': frozenset({'🐮', '🐂', '🐃'}),
            '🦀': None,
            '🖍️': None,
            '🧁': None,
            '🍛': None,
            '🖥️': frozenset({'💻'}),
            '🧬': None,
            '🐬': frozenset({'🦈'}),
            '🐉': frozenset({'🐲', '🦖'}),
            '🔌': frozenset({'⚡'}),
            '🐘': frozenset({'𓃰'}),
            '🧐': None,
            '🚒': None,
            '🐟': frozenset({'🐡', '🎣', '🐠'}),
            '💾': None,
            '🐸': None,
            '💎': frozenset({'💍'}),
            '👻': None,
            '🍇': None,
            '🍏': None,
            '🚁': None,
            '🐎': frozenset({'🐴'}),
            '🌶️': None,
            '🎃': None,
            '📒': frozenset({'📔', '🗒️'}),
            '💡': None,
            '🦁': None,
            '🕰️': None,
            '🍈': frozenset({'🍉'}),
            '🔬': frozenset({'⚗️'}),
            '🗿': None,
            '🐒': frozenset({'🐵'}),
            '🍄': None,
            '🤓': None,
            '📓': None,
            '📦': frozenset({'🪤'}),
            '📎': None,
            '🍐': None,
            '🐧': None,
            '🥧': None,
            '🐖': frozenset({'🐷', '🐗'}),
            '🍍': None,
            '🍕': None,
            '🍿': frozenset({'🌽'}),
            '🥔': None,
            '🥨': None,
            '🧩': None,
            '🌈': None,
            '🍎': None,
            '🏮': None,
            '🍙': None,
            '🍠': None,
            '🤖': None,
            '🚀': None,
            '🎢': None,
            '🏫': None,
            '🦭': None,
            '🦐': frozenset({'🍤'}),
            '🧦': None,
            '🐚': None,
            '🦑': frozenset({'🐙'}),
            '📏': None,
            '🍓': None,
            '🍊': None,
            '🔭': None,
            '🤔': None,
            '💭': None,
            '🐅': frozenset({'🐯'}),
            '🎩': None,
            '📐': None,
            '🎺': frozenset({'📯'}),
            '🌷': frozenset({'🌹'}),
            '🐢': None,
            '📼': None,
            '🌊': frozenset({'💧', '💦'}),
            '🐋': frozenset({'🐳'}),
        })

    async def getCurrentEmoteFor(self, twitchChannelId: str) -> str:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        currentEmoteIndex = await self.__getCurrentEmoteIndexFor(twitchChannelId)
        return self.__emojiEquivalents[currentEmoteIndex]

    async def __getCurrentEmoteIndexFor(self, twitchChannelId: str) -> int:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        emoteIndex = await self.__triviaEmoteRepository.getEmoteIndexFor(twitchChannelId)

        if emoteIndex is None or emoteIndex < 0 or emoteIndex >= len(self.__emojiEquivalents):
            self.__timber.log('TriviaEmoteGenerator', f'The emoteIndex value is out of bounds or uninitialized ({emoteIndex=}) ({twitchChannelId=})')
            emoteIndex = 0

        return emoteIndex

    async def getNextEmoteFor(self, twitchChannelId: str) -> str:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        currentEmoteIndex = await self.__getCurrentEmoteIndexFor(twitchChannelId)
        newEmoteIndex = (currentEmoteIndex + 1) % len(self.__emojiEquivalents)

        await self.__triviaEmoteRepository.setEmoteIndexFor(
            emoteIndex = newEmoteIndex,
            twitchChannelId = twitchChannelId,
        )

        return self.__emojiEquivalents[newEmoteIndex]

    def getRandomEmote(self) -> str:
        return random.choice(self.__emojiEquivalents)

    async def getValidatedAndNormalizedEmote(self, emote: str | None) -> str | None:
        if emote is not None and not isinstance(emote, str):
            raise TypeError(f'emote argument is malformed: \"{emote}\"')

        if not utils.isValidStr(emote):
            return None

        if emote in self.__emojiToEquivalents:
            return emote

        for emoteKey, equivalentEmotes in self.__emojiToEquivalents.items():
            if equivalentEmotes is not None and len(equivalentEmotes) >= 1 and emote in equivalentEmotes:
                return emoteKey

        return None
