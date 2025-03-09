import pytest

from src.chatterPreferredTts.helper.chatterPreferredTtsUserMessageHelper import ChatterPreferredTtsUserMessageHelper
from src.chatterPreferredTts.helper.chatterPreferredTtsUserMessageHelperInterface import \
    ChatterPreferredTtsUserMessageHelperInterface
from src.chatterPreferredTts.models.commodoreSam.commodoreSamPreferredTts import CommodoreSamPreferredTts
from src.chatterPreferredTts.models.decTalk.decTalkPreferredTts import DecTalkPreferredTts
from src.chatterPreferredTts.models.google.googlePreferredTts import GooglePreferredTts
from src.chatterPreferredTts.models.halfLife.halfLifePreferredTts import HalfLifePreferredTts
from src.chatterPreferredTts.models.microsoftSam.microsoftSamPreferredTts import MicrosoftSamPreferredTts
from src.chatterPreferredTts.models.streamElements.streamElementsPreferredTts import StreamElementsPreferredTts
from src.chatterPreferredTts.models.ttsMonster.ttsMonsterPreferredTts import TtsMonsterPreferredTts
from src.decTalk.mapper.decTalkVoiceMapper import DecTalkVoiceMapper
from src.decTalk.mapper.decTalkVoiceMapperInterface import DecTalkVoiceMapperInterface
from src.decTalk.models.decTalkVoice import DecTalkVoice
from src.halfLife.models.halfLifeVoice import HalfLifeVoice
from src.halfLife.parser.halfLifeVoiceParser import HalfLifeVoiceParser
from src.halfLife.parser.halfLifeVoiceParserInterface import HalfLifeVoiceParserInterface
from src.language.languageEntry import LanguageEntry
from src.language.languagesRepository import LanguagesRepository
from src.language.languagesRepositoryInterface import LanguagesRepositoryInterface
from src.microsoftSam.models.microsoftSamVoice import MicrosoftSamVoice
from src.microsoftSam.parser.microsoftSamJsonParser import MicrosoftSamJsonParser
from src.microsoftSam.parser.microsoftSamJsonParserInterface import MicrosoftSamJsonParserInterface
from src.streamElements.parser.streamElementsJsonParser import StreamElementsJsonParser
from src.streamElements.parser.streamElementsJsonParserInterface import StreamElementsJsonParserInterface
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.ttsMonster.mapper.ttsMonsterPrivateApiJsonMapper import TtsMonsterPrivateApiJsonMapper
from src.ttsMonster.mapper.ttsMonsterPrivateApiJsonMapperInterface import TtsMonsterPrivateApiJsonMapperInterface
from src.ttsMonster.models.ttsMonsterVoice import TtsMonsterVoice


class TestChatterPreferredTtsUserMessageHelper:

    decTalkVoiceMapper: DecTalkVoiceMapperInterface = DecTalkVoiceMapper()

    languagesRepository: LanguagesRepositoryInterface = LanguagesRepository()

    halfLifeVoiceParser: HalfLifeVoiceParserInterface = HalfLifeVoiceParser()

    microsoftSamJsonParser: MicrosoftSamJsonParserInterface = MicrosoftSamJsonParser()

    streamElementsJsonParser: StreamElementsJsonParserInterface = StreamElementsJsonParser()

    timber: TimberInterface = TimberStub()

    ttsMonsterPrivateApiJsonMapper: TtsMonsterPrivateApiJsonMapperInterface = TtsMonsterPrivateApiJsonMapper(
        timber = timber
    )

    helper: ChatterPreferredTtsUserMessageHelperInterface = ChatterPreferredTtsUserMessageHelper(
        decTalkVoiceMapper = decTalkVoiceMapper,
        halfLifeVoiceParser = halfLifeVoiceParser,
        languagesRepository = languagesRepository,
        microsoftSamJsonParser = microsoftSamJsonParser,
        streamElementsJsonParser = streamElementsJsonParser,
        ttsMonsterPrivateApiJsonMapper = ttsMonsterPrivateApiJsonMapper
    )

    @pytest.mark.asyncio
    async def test_parseUserMessage_withCommodoreSamStrings(self):
        result = await self.helper.parseUserMessage('commodoresam')
        assert isinstance(result, CommodoreSamPreferredTts)

        result = await self.helper.parseUserMessage('commodore sam')
        assert isinstance(result, CommodoreSamPreferredTts)

        result = await self.helper.parseUserMessage('commodore_sam')
        assert isinstance(result, CommodoreSamPreferredTts)

        result = await self.helper.parseUserMessage('commodore-sam')
        assert isinstance(result, CommodoreSamPreferredTts)

    @pytest.mark.asyncio
    async def test_parseUserMessage_withDecTalkStrings(self):
        result = await self.helper.parseUserMessage('dectalk')
        assert isinstance(result, DecTalkPreferredTts)
        assert result.voice is None

        result = await self.helper.parseUserMessage('dec talk')
        assert isinstance(result, DecTalkPreferredTts)
        assert result.voice is None

        result = await self.helper.parseUserMessage('dec_talk')
        assert isinstance(result, DecTalkPreferredTts)
        assert result.voice is None

        result = await self.helper.parseUserMessage('dec-talk')
        assert isinstance(result, DecTalkPreferredTts)
        assert result.voice is None

    @pytest.mark.asyncio
    async def test_parseUserMessage_withDecTalkAndHarry(self):
        result = await self.helper.parseUserMessage('dectalk harry')
        assert isinstance(result, DecTalkPreferredTts)
        assert result.voice is DecTalkVoice.HARRY

        result = await self.helper.parseUserMessage('dec talk harry')
        assert isinstance(result, DecTalkPreferredTts)
        assert result.voice is DecTalkVoice.HARRY

        result = await self.helper.parseUserMessage('dec_talk harry')
        assert isinstance(result, DecTalkPreferredTts)
        assert result.voice is DecTalkVoice.HARRY

        result = await self.helper.parseUserMessage('dec-talk harry')
        assert isinstance(result, DecTalkPreferredTts)
        assert result.voice is DecTalkVoice.HARRY

    @pytest.mark.asyncio
    async def test_parseUserMessage_withDecTalkAndPaul(self):
        result = await self.helper.parseUserMessage('dectalk paul')
        assert isinstance(result, DecTalkPreferredTts)
        assert result.voice is DecTalkVoice.PAUL

        result = await self.helper.parseUserMessage('dec talk paul')
        assert isinstance(result, DecTalkPreferredTts)
        assert result.voice is DecTalkVoice.PAUL

        result = await self.helper.parseUserMessage('dec_talk paul')
        assert isinstance(result, DecTalkPreferredTts)
        assert result.voice is DecTalkVoice.PAUL

        result = await self.helper.parseUserMessage('dec-talk paul')
        assert isinstance(result, DecTalkPreferredTts)
        assert result.voice is DecTalkVoice.PAUL

    @pytest.mark.asyncio
    async def test_parseUserMessage_withEmptyString(self):
        result = await self.helper.parseUserMessage('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseUserMessage_withGoogleStrings(self):
        result = await self.helper.parseUserMessage('goog')
        assert isinstance(result, GooglePreferredTts)
        assert result.languageEntry is None

        result = await self.helper.parseUserMessage('googl')
        assert isinstance(result, GooglePreferredTts)
        assert result.languageEntry is None

        result = await self.helper.parseUserMessage('google')
        assert isinstance(result, GooglePreferredTts)
        assert result.languageEntry is None

    @pytest.mark.asyncio
    async def test_parseUserMessage_withGoogleAndEnglish(self):
        result = await self.helper.parseUserMessage('goog english')
        assert isinstance(result, GooglePreferredTts)
        assert result.languageEntry is LanguageEntry.ENGLISH

    @pytest.mark.asyncio
    async def test_parseUserMessage_withGoogleAndGarbledText(self):
        result = await self.helper.parseUserMessage('google fdsiklahfkldsajlfdklsflad')
        assert isinstance(result, GooglePreferredTts)
        assert result.languageEntry is None

    @pytest.mark.asyncio
    async def test_parseUserMessage_withGoogleAndJapanese(self):
        result = await self.helper.parseUserMessage('googl ja')
        assert isinstance(result, GooglePreferredTts)
        assert result.languageEntry is LanguageEntry.JAPANESE

    @pytest.mark.asyncio
    async def test_parseUserMessage_withGoogleAndSwedish(self):
        result = await self.helper.parseUserMessage('google sweden')
        assert isinstance(result, GooglePreferredTts)
        assert result.languageEntry is LanguageEntry.SWEDISH

    @pytest.mark.asyncio
    async def test_parseUserMessage_withHalfLifeStrings(self):
        result = await self.helper.parseUserMessage('halflife')
        assert isinstance(result, HalfLifePreferredTts)

        result = await self.helper.parseUserMessage('half life')
        assert isinstance(result, HalfLifePreferredTts)

        result = await self.helper.parseUserMessage('half_life')
        assert isinstance(result, HalfLifePreferredTts)

        result = await self.helper.parseUserMessage('half-life')
        assert isinstance(result, HalfLifePreferredTts)

    @pytest.mark.asyncio
    async def test_parseUserMessage_withHalfLifeAndGarbledText(self):
        result = await self.helper.parseUserMessage('half life fdsiklahfkldsajlfdklsflad')
        assert isinstance(result, HalfLifePreferredTts)
        assert result.halfLifeVoiceEntry is HalfLifeVoice.ALL

    @pytest.mark.asyncio
    async def test_parseUserMessage_withHalfLifeAndScientist(self):
        result = await self.helper.parseUserMessage('half life scientist')
        assert isinstance(result, HalfLifePreferredTts)
        assert result.halfLifeVoiceEntry is HalfLifeVoice.SCIENTIST

    @pytest.mark.asyncio
    async def test_parseUserMessage_withHalfLifeAndBarney(self):
        result = await self.helper.parseUserMessage('half life barney')
        assert isinstance(result, HalfLifePreferredTts)
        assert result.halfLifeVoiceEntry is HalfLifeVoice.BARNEY

    @pytest.mark.asyncio
    async def test_parseUserMessage_withHalfLifeAndPolice(self):
        result = await self.helper.parseUserMessage('half life police')
        assert isinstance(result, HalfLifePreferredTts)
        assert result.halfLifeVoiceEntry is HalfLifeVoice.POLICE

    @pytest.mark.asyncio
    async def test_parseUserMessage_withMicrosoftSamStrings(self):
        result = await self.helper.parseUserMessage('microsoftsam')
        assert isinstance(result, MicrosoftSamPreferredTts)

        result = await self.helper.parseUserMessage('microsoft sam')
        assert isinstance(result, MicrosoftSamPreferredTts)

        result = await self.helper.parseUserMessage('microsoft_sam')
        assert isinstance(result, MicrosoftSamPreferredTts)

        result = await self.helper.parseUserMessage('microsoft-sam')
        assert isinstance(result, MicrosoftSamPreferredTts)

    @pytest.mark.asyncio
    async def test_parseUserMessage_withMicrosoftSamAndMaryForSpace(self):
        result = await self.helper.parseUserMessage('microsoft sam mary_space')
        assert isinstance(result, MicrosoftSamPreferredTts)
        assert result.voice is MicrosoftSamVoice.MARY_SPACE

    @pytest.mark.asyncio
    async def test_parseUserMessage_withMicrosoftSamAndBonziBuddy(self):
        result = await self.helper.parseUserMessage('microsoft sam bonzi_buddy')
        assert isinstance(result, MicrosoftSamPreferredTts)
        assert result.voice is MicrosoftSamVoice.BONZI_BUDDY

    @pytest.mark.asyncio
    async def test_parseUserMessage_withTtsMonsterStrings(self):
        result = await self.helper.parseUserMessage('ttsMonster')
        assert isinstance(result, TtsMonsterPreferredTts)

        result = await self.helper.parseUserMessage('tts monster')
        assert isinstance(result, TtsMonsterPreferredTts)

        result = await self.helper.parseUserMessage('tts-monster')
        assert isinstance(result, TtsMonsterPreferredTts)

        result = await self.helper.parseUserMessage('tts_monster')
        assert isinstance(result, TtsMonsterPreferredTts)

    @pytest.mark.asyncio
    async def test_parseUserMessage_withTtsMonsterAndShadow(self):
        result = await self.helper.parseUserMessage('tts monster shadow')
        assert isinstance(result, TtsMonsterPreferredTts)
        assert result.voice is TtsMonsterVoice.SHADOW

    @pytest.mark.asyncio
    async def test_parseUserMessage_withTtsMonsterAndZeroTwo(self):
        result = await self.helper.parseUserMessage('tts monster zerotwo')
        assert isinstance(result, TtsMonsterPreferredTts)
        assert result.voice is TtsMonsterVoice.ZERO_TWO

    @pytest.mark.asyncio
    async def test_parseUserMessage_withStreamElementsStrings(self):
        result = await self.helper.parseUserMessage('streamelements')
        assert isinstance(result, StreamElementsPreferredTts)

        result = await self.helper.parseUserMessage('streamElements')
        assert isinstance(result, StreamElementsPreferredTts)

        result = await self.helper.parseUserMessage('stream elements')
        assert isinstance(result, StreamElementsPreferredTts)

        result = await self.helper.parseUserMessage('stream-elements')
        assert isinstance(result, StreamElementsPreferredTts)

        result = await self.helper.parseUserMessage('stream_elements')
        assert isinstance(result, StreamElementsPreferredTts)

    @pytest.mark.asyncio
    async def test_parseUserMessage_withNone(self):
        result = await self.helper.parseUserMessage(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseUserMessage_withWhitespaceString(self):
        result = await self.helper.parseUserMessage(' ')
        assert result is None

    def test_sanity(self):
        assert self.helper is not None
        assert isinstance(self.helper, ChatterPreferredTtsUserMessageHelper)
        assert isinstance(self.helper, ChatterPreferredTtsUserMessageHelperInterface)
