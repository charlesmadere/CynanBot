import pytest

from src.decTalk.decTalkVoiceChooser import DecTalkVoiceChooser
from src.decTalk.decTalkVoiceChooserInterface import DecTalkVoiceChooserInterface
from src.decTalk.decTalkVoiceMapper import DecTalkVoiceMapper
from src.decTalk.decTalkVoiceMapperInterface import DecTalkVoiceMapperInterface
from src.decTalk.models.decTalkVoice import DecTalkVoice


class TestDecTalkVoiceChooser:

    decTalkVoiceMapper: DecTalkVoiceMapperInterface = DecTalkVoiceMapper()

    decTalkVoiceChooser: DecTalkVoiceChooserInterface = DecTalkVoiceChooser()

    @pytest.mark.asyncio
    async def test_choose_withEmptyString(self):
        result = await self.decTalkVoiceChooser.choose('')
        assert result is None

    @pytest.mark.asyncio
    async def test_choose_withNone(self):
        result = await self.decTalkVoiceChooser.choose(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_choose_withWhitespace(self):
        result = await self.decTalkVoiceChooser.choose(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_choose_withVoiceBetty(self):
        await self.__assertChooseWithVoice(DecTalkVoice.BETTY)

    @pytest.mark.asyncio
    async def test_choose_withVoiceDennis(self):
        await self.__assertChooseWithVoice(DecTalkVoice.DENNIS)

    @pytest.mark.asyncio
    async def test_choose_withVoiceFrank(self):
        await self.__assertChooseWithVoice(DecTalkVoice.FRANK)

    @pytest.mark.asyncio
    async def test_choose_withVoiceHarry(self):
        await self.__assertChooseWithVoice(DecTalkVoice.HARRY)

    @pytest.mark.asyncio
    async def test_choose_withVoiceKit(self):
        await self.__assertChooseWithVoice(DecTalkVoice.KIT)

    @pytest.mark.asyncio
    async def test_choose_withVoicePaul(self):
        await self.__assertChooseWithVoice(DecTalkVoice.PAUL)

    @pytest.mark.asyncio
    async def test_choose_withVoiceRita(self):
        await self.__assertChooseWithVoice(DecTalkVoice.RITA)

    @pytest.mark.asyncio
    async def test_choose_withVoiceWendy(self):
        await self.__assertChooseWithVoice(DecTalkVoice.WENDY)

    @pytest.mark.asyncio
    async def test_choose_withVoiceUrsula(self):
        await self.__assertChooseWithVoice(DecTalkVoice.URSULA)

    @pytest.mark.asyncio
    async def __assertChooseWithVoice(self, voice: DecTalkVoice):
        for _ in range(100):
            voiceString = await self.decTalkVoiceMapper.toString(voice)

            message = f'{voiceString} Hello, World!'
            updatedMessage = await self.decTalkVoiceChooser.choose(message)
            assert updatedMessage is None

            message = f'Hello,{voiceString}World!'
            updatedMessage = await self.decTalkVoiceChooser.choose(message)
            assert updatedMessage is None

            message = f'Hello, World!{voiceString}'
            updatedMessage = await self.decTalkVoiceChooser.choose(message)
            assert updatedMessage is None
