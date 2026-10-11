from typing import Final

import pytest

from src.emojiHelper.emojiHelper import EmojiHelper
from src.emojiHelper.emojiHelperInterface import EmojiHelperInterface
from src.emojiHelper.emojiRepository import EmojiRepository
from src.emojiHelper.emojiRepositoryInterface import EmojiRepositoryInterface
from src.google.googleTtsMessageCleaner import GoogleTtsMessageCleaner
from src.google.googleTtsMessageCleanerInterface import GoogleTtsMessageCleanerInterface
from src.google.jsonMapper.googleJsonMapper import GoogleJsonMapper
from src.google.jsonMapper.googleJsonMapperInterface import GoogleJsonMapperInterface
from src.google.settings.googleSettingsRepository import GoogleSettingsRepository
from src.google.settings.googleSettingsRepositoryInterface import GoogleSettingsRepositoryInterface
from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.misc.randomUtils import RandomUtils
from src.misc.randomUtilsInterface import RandomUtilsInterface
from src.storage.jsonStaticReader import JsonStaticReader
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.tts.jsonMapper.ttsJsonMapper import TtsJsonMapper
from src.tts.jsonMapper.ttsJsonMapperInterface import TtsJsonMapperInterface
from src.tts.settings.ttsSettingsRepository import TtsSettingsRepository
from src.tts.settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface


class TestDecTalkMessageCleaner:

    timber: Final[TimberInterface] = TimberStub()

    randomUtils: Final[RandomUtilsInterface] = RandomUtils()

    emojiRepository: Final[EmojiRepositoryInterface] = EmojiRepository(
        emojiJsonReader = JsonStaticReader(
            jsonContents = {
                'emojis': [
                    {
                        'code': [
                            "1F600",
                        ],
                        'emoji': '😀',
                        'name': 'grinning face',
                        'category': 'Smileys & Emotion',
                        'subcategory': 'face-smiling',
                        'support': {
                            'apple': True,
                            'google': True,
                            'windows': True,
                        },
                    },
                    {
                        'code': [
                            "1F988",
                        ],
                        'emoji': '🦈',
                        'name': 'shark',
                        'category': 'Animals & Nature',
                        'subcategory': 'animal-marine',
                        'support': {
                            'apple': True,
                            'google': True,
                            'windows': True,
                        },
                    },
                ],
            },
        ),
        timber = timber,
    )

    emojiHelper: Final[EmojiHelperInterface] = EmojiHelper(
        emojiRepository = emojiRepository,
        randomUtils = randomUtils,
    )

    timeZoneRepository: Final[TimeZoneRepositoryInterface] = TimeZoneRepository()

    googleJsonMapper: Final[GoogleJsonMapperInterface] = GoogleJsonMapper(
        timber = timber,
        timeZoneRepository = timeZoneRepository,
    )

    googleSettingsRepository: Final[GoogleSettingsRepositoryInterface] = GoogleSettingsRepository(
        googleJsonMapper = googleJsonMapper,
        settingsJsonReader = JsonStaticReader({
            'maxConsecutiveEmojis': 3,
        }),
    )

    ttsJsonMapper: Final[TtsJsonMapperInterface] = TtsJsonMapper(
        timber = timber,
    )

    ttsSettingsRepository: Final[TtsSettingsRepositoryInterface] = TtsSettingsRepository(
        settingsJsonReader = JsonStaticReader(dict()),
        ttsJsonMapper = ttsJsonMapper,
    )

    cleaner: Final[GoogleTtsMessageCleanerInterface] = GoogleTtsMessageCleaner(
        googleSettingsRepository = googleSettingsRepository,
        ttsSettingsRepository = ttsSettingsRepository,
    )

    @pytest.mark.asyncio
    async def test_clean_withEmptyString(self):
        result = await self.cleaner.clean('')
        assert result is None

    @pytest.mark.asyncio
    async def test_clean_withExtraWhitespaceAndEmojiString(self):
        result = await self.cleaner.clean('   👶 🍼 🧸 🎀 👶 🍼 🧸 🎀 👶  What\'s  up?!   GL  👶   🍼 🧸 🎀 👶 🍼 🧸 🎀 👶     today!!!    \n\n')
        assert result == '👶 🍼 🧸 What\'s up?! GL 👶 🍼 🧸 today!!!'

    @pytest.mark.asyncio
    async def test_clean_withHelloWorld(self):
        result = await self.cleaner.clean('Hello, World!')
        assert result == 'Hello, World!'

    @pytest.mark.asyncio
    async def test_clean_withNone(self):
        result = await self.cleaner.clean(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_clean_withWhitespaceString(self):
        result = await self.cleaner.clean(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_clean_withZoeTimeForTheLittleOnesMessage(self):
        result = await self.cleaner.clean('Zoë subscribed! 👶 🍼 🧸 🎀 👶 🍼 🧸 🎀 👶 🍼 🧸 🎀 👶 🍼 🧸 🎀 👶 🍼 🧸 🎀 👶 🍼 🧸 🎀 👶 🍼 🧸 🎀 TIME FOR THE LITTLE ONES 👶 🍼 🧸 🎀 👶 🍼 🧸 🎀 👶 🍼 🧸 🎀 👶 🍼 🧸 🎀 👶 🍼 🧸 🎀 👶 🍼 🧸 🎀 👶 🍼 🧸 🎀 👶 🍼 🧸 🎀 👶 🍼 🧸 🎀👶 🍼 🧸 🎀👶 🍼 🧸 🎀👶 🍼 🧸 🎀 👶 🍼 🧸 🎀 👶 🍼 🧸 🎀 👶 🍼 🧸 🎀 👶 🍼 🧸 🎀 👶 🍼 🧸 🎀 👶 🍼 🧸 🎀 TIME FOR THE LITTLE ONES 👶 🍼 🧸 🎀 👶 🍼 🧸 🎀 👶 🍼 🧸 🎀 TIME FOR THE LITTLE ONES👶🍼 🧸 🎀 👶 🍼 🧸 🎀 👶 🍼 🧸 🎀 👶 🍼 🧸 🎀 👶 🍼 🧸 🎀👶 🍼 🧸 🎀')
        assert result == 'Zoë subscribed! 👶 🍼 🧸 TIME FOR THE LITTLE ONES 👶 🍼 🧸 TIME FOR THE LITTLE ONES 👶 🍼 🧸 TIME FOR THE LITTLE ONES👶🍼 🧸'

    def test_sanity(self):
        assert self.cleaner is not None
        assert isinstance(self.cleaner, GoogleTtsMessageCleaner)
        assert isinstance(self.cleaner, GoogleTtsMessageCleanerInterface)
