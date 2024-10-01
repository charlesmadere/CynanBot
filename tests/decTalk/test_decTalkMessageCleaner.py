import pytest

from src.decTalk.decTalkMessageCleaner import DecTalkMessageCleaner
from src.decTalk.decTalkMessageCleanerInterface import DecTalkMessageCleanerInterface
from src.emojiHelper.emojiHelper import EmojiHelper
from src.emojiHelper.emojiHelperInterface import EmojiHelperInterface
from src.emojiHelper.emojiRepository import EmojiRepository
from src.emojiHelper.emojiRepositoryInterface import EmojiRepositoryInterface
from src.storage.jsonStaticReader import JsonStaticReader
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub


class TestDecTalkMessageCleaner:

    timber: TimberInterface = TimberStub()

    emojiRepository: EmojiRepositoryInterface = EmojiRepository(
        emojiJsonReader = JsonStaticReader(
            jsonContents = {
                'emojis': [
                    {
                        'code': [
                            "1F600"
                        ],
                        'emoji': '😀',
                        'name': 'grinning face',
                        'category': 'Smileys & Emotion',
                        'subcategory': 'face-smiling',
                        'support': {
                            'apple': True,
                            'google': True,
                            'windows': True
                        }
                    },
                    {
                        'code': [
                            "1F988"
                        ],
                        'emoji': '🦈',
                        'name': 'shark',
                        'category': 'Animals & Nature',
                        'subcategory': 'animal-marine',
                        'support': {
                            'apple': True,
                            'google': True,
                            'windows': True
                        }
                    }
                ]
            }
        ),
        timber = timber
    )

    emojiHelper: EmojiHelperInterface = EmojiHelper(
        emojiRepository = emojiRepository
    )

    cleaner: DecTalkMessageCleanerInterface = DecTalkMessageCleaner(
        emojiHelper = emojiHelper,
        timber = timber
    )

    @pytest.mark.asyncio
    async def test_clean_withEmptyString(self):
        result = await self.cleaner.clean('')
        assert result is None

    @pytest.mark.asyncio
    async def test_clean_withNone(self):
        result = await self.cleaner.clean(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_clean_withEmojiString(self):
        result = await self.cleaner.clean('shark 🦈 shark 😀 🤔')
        assert result == 'shark shark shark grinning face'

    @pytest.mark.asyncio
    async def test_clean_withWhitespaceString(self):
        result = await self.cleaner.clean(' ')
        assert result is None
