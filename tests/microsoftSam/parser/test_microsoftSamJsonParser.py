import pytest

from src.microsoftSam.models.microsoftSamVoice import MicrosoftSamVoice
from src.microsoftSam.parser.microsoftSamJsonParser import MicrosoftSamJsonParser
from src.microsoftSam.parser.microsoftSamJsonParserInterface import MicrosoftSamJsonParserInterface


class TestMicrosoftSamJsonParser:

    parser: MicrosoftSamJsonParserInterface = MicrosoftSamJsonParser()

    @pytest.mark.asyncio
    async def test_parseVoice_withAdultFemale1(self):
        result = await self.parser.parseVoice('adult_female_1')
        assert result is MicrosoftSamVoice.ADULT_FEMALE_1

        result = await self.parser.parseVoice('adult-female-1')
        assert result is MicrosoftSamVoice.ADULT_FEMALE_1

        result = await self.parser.parseVoice('adult female 1')
        assert result is MicrosoftSamVoice.ADULT_FEMALE_1

        result = await self.parser.parseVoice('adultfemale1')
        assert result is MicrosoftSamVoice.ADULT_FEMALE_1

        result = await self.parser.parseVoice('adult_female')
        assert result is MicrosoftSamVoice.ADULT_FEMALE_1

        result = await self.parser.parseVoice('adult-female')
        assert result is MicrosoftSamVoice.ADULT_FEMALE_1

        result = await self.parser.parseVoice('adult female')
        assert result is MicrosoftSamVoice.ADULT_FEMALE_1

        result = await self.parser.parseVoice('adultfemale')
        assert result is MicrosoftSamVoice.ADULT_FEMALE_1

    @pytest.mark.asyncio
    async def test_parseVoice_withAdultFemale2(self):
        result = await self.parser.parseVoice('adult_female_2')
        assert result is MicrosoftSamVoice.ADULT_FEMALE_2

        result = await self.parser.parseVoice('adult-female-2')
        assert result is MicrosoftSamVoice.ADULT_FEMALE_2

        result = await self.parser.parseVoice('adult female 2')
        assert result is MicrosoftSamVoice.ADULT_FEMALE_2

        result = await self.parser.parseVoice('adultfemale2')
        assert result is MicrosoftSamVoice.ADULT_FEMALE_2

    @pytest.mark.asyncio
    async def test_parseVoice_withAdultFemaleWhisper(self):
        result = await self.parser.parseVoice('adult_female_whisper')
        assert result is MicrosoftSamVoice.ADULT_FEMALE_WHISPER

        result = await self.parser.parseVoice('adult-female-whisper')
        assert result is MicrosoftSamVoice.ADULT_FEMALE_WHISPER

        result = await self.parser.parseVoice('adult female whisper')
        assert result is MicrosoftSamVoice.ADULT_FEMALE_WHISPER

        result = await self.parser.parseVoice('adultfemalewhisper')
        assert result is MicrosoftSamVoice.ADULT_FEMALE_WHISPER

    @pytest.mark.asyncio
    async def test_parseVoice_withAdultMale1(self):
        result = await self.parser.parseVoice('adult_male_1')
        assert result is MicrosoftSamVoice.ADULT_MALE_1

        result = await self.parser.parseVoice('adult-male-1')
        assert result is MicrosoftSamVoice.ADULT_MALE_1

        result = await self.parser.parseVoice('adult male 1')
        assert result is MicrosoftSamVoice.ADULT_MALE_1

        result = await self.parser.parseVoice('adultmale1')
        assert result is MicrosoftSamVoice.ADULT_MALE_1

        result = await self.parser.parseVoice('adult_male')
        assert result is MicrosoftSamVoice.ADULT_MALE_1

        result = await self.parser.parseVoice('adult-male')
        assert result is MicrosoftSamVoice.ADULT_MALE_1

        result = await self.parser.parseVoice('adult male')
        assert result is MicrosoftSamVoice.ADULT_MALE_1

        result = await self.parser.parseVoice('adultmale')
        assert result is MicrosoftSamVoice.ADULT_MALE_1

    @pytest.mark.asyncio
    async def test_parseVoice_withAdultMale2(self):
        result = await self.parser.parseVoice('adult_male_2')
        assert result is MicrosoftSamVoice.ADULT_MALE_2

        result = await self.parser.parseVoice('adult-male-2')
        assert result is MicrosoftSamVoice.ADULT_MALE_2

        result = await self.parser.parseVoice('adult male 2')
        assert result is MicrosoftSamVoice.ADULT_MALE_2

        result = await self.parser.parseVoice('adultmale2')
        assert result is MicrosoftSamVoice.ADULT_MALE_2

    @pytest.mark.asyncio
    async def test_parseVoice_withAdultMale3(self):
        result = await self.parser.parseVoice('adult_male_3')
        assert result is MicrosoftSamVoice.ADULT_MALE_3

        result = await self.parser.parseVoice('adult-male-3')
        assert result is MicrosoftSamVoice.ADULT_MALE_3

        result = await self.parser.parseVoice('adult male 3')
        assert result is MicrosoftSamVoice.ADULT_MALE_3

        result = await self.parser.parseVoice('adultmale3')
        assert result is MicrosoftSamVoice.ADULT_MALE_3

    @pytest.mark.asyncio
    async def test_parseVoice_withAdultMale4(self):
        result = await self.parser.parseVoice('adult_male_4')
        assert result is MicrosoftSamVoice.ADULT_MALE_4

        result = await self.parser.parseVoice('adult-male-4')
        assert result is MicrosoftSamVoice.ADULT_MALE_4

        result = await self.parser.parseVoice('adult male 4')
        assert result is MicrosoftSamVoice.ADULT_MALE_4

        result = await self.parser.parseVoice('adultmale4')
        assert result is MicrosoftSamVoice.ADULT_MALE_4

    @pytest.mark.asyncio
    async def test_parseVoice_withAdultMale5(self):
        result = await self.parser.parseVoice('adult_male_5')
        assert result is MicrosoftSamVoice.ADULT_MALE_5

        result = await self.parser.parseVoice('adult-male-5')
        assert result is MicrosoftSamVoice.ADULT_MALE_5

        result = await self.parser.parseVoice('adult male 5')
        assert result is MicrosoftSamVoice.ADULT_MALE_5

        result = await self.parser.parseVoice('adultmale5')
        assert result is MicrosoftSamVoice.ADULT_MALE_5

    @pytest.mark.asyncio
    async def test_parseVoice_withAdultMale6(self):
        result = await self.parser.parseVoice('adult_male_6')
        assert result is MicrosoftSamVoice.ADULT_MALE_6

        result = await self.parser.parseVoice('adult-male-6')
        assert result is MicrosoftSamVoice.ADULT_MALE_6

        result = await self.parser.parseVoice('adult male 6')
        assert result is MicrosoftSamVoice.ADULT_MALE_6

        result = await self.parser.parseVoice('adultmale6')
        assert result is MicrosoftSamVoice.ADULT_MALE_6

    @pytest.mark.asyncio
    async def test_parseVoice_withAdultMale7(self):
        result = await self.parser.parseVoice('adult_male_7')
        assert result is MicrosoftSamVoice.ADULT_MALE_7

        result = await self.parser.parseVoice('adult-male-7')
        assert result is MicrosoftSamVoice.ADULT_MALE_7

        result = await self.parser.parseVoice('adult male 7')
        assert result is MicrosoftSamVoice.ADULT_MALE_7

        result = await self.parser.parseVoice('adultmale7')
        assert result is MicrosoftSamVoice.ADULT_MALE_7

    @pytest.mark.asyncio
    async def test_parseVoice_withAdultMale8(self):
        result = await self.parser.parseVoice('adult_male_8')
        assert result is MicrosoftSamVoice.ADULT_MALE_8

        result = await self.parser.parseVoice('adult-male-8')
        assert result is MicrosoftSamVoice.ADULT_MALE_8

        result = await self.parser.parseVoice('adult male 8')
        assert result is MicrosoftSamVoice.ADULT_MALE_8

        result = await self.parser.parseVoice('adultmale8')
        assert result is MicrosoftSamVoice.ADULT_MALE_8

    @pytest.mark.asyncio
    async def test_parseVoice_withBonziBuddy(self):
        result = await self.parser.parseVoice('bonzi_buddy')
        assert result is MicrosoftSamVoice.BONZI_BUDDY

        result = await self.parser.parseVoice('bonzi-buddy')
        assert result is MicrosoftSamVoice.BONZI_BUDDY

        result = await self.parser.parseVoice('bonzi buddy')
        assert result is MicrosoftSamVoice.BONZI_BUDDY

        result = await self.parser.parseVoice('bonzibuddy')
        assert result is MicrosoftSamVoice.BONZI_BUDDY

    @pytest.mark.asyncio
    async def test_parseVoice_withMary(self):
        result = await self.parser.parseVoice('mary')
        assert result is MicrosoftSamVoice.MARY

    @pytest.mark.asyncio
    async def test_parseVoice_withMaryHall(self):
        result = await self.parser.parseVoice('mary_hall')
        assert result is MicrosoftSamVoice.MARY_HALL

        result = await self.parser.parseVoice('mary-hall')
        assert result is MicrosoftSamVoice.MARY_HALL

        result = await self.parser.parseVoice('mary hall')
        assert result is MicrosoftSamVoice.MARY_HALL

        result = await self.parser.parseVoice('maryhall')
        assert result is MicrosoftSamVoice.MARY_HALL

    @pytest.mark.asyncio
    async def test_parseVoice_withMaryPhone(self):
        result = await self.parser.parseVoice('mary_phone')
        assert result is MicrosoftSamVoice.MARY_TELEPHONE

        result = await self.parser.parseVoice('mary-phone')
        assert result is MicrosoftSamVoice.MARY_TELEPHONE

        result = await self.parser.parseVoice('mary phone')
        assert result is MicrosoftSamVoice.MARY_TELEPHONE

        result = await self.parser.parseVoice('maryphone')
        assert result is MicrosoftSamVoice.MARY_TELEPHONE

    @pytest.mark.asyncio
    async def test_parseVoice_withMarySpace(self):
        result = await self.parser.parseVoice('mary_space')
        assert result is MicrosoftSamVoice.MARY_SPACE

        result = await self.parser.parseVoice('mary-space')
        assert result is MicrosoftSamVoice.MARY_SPACE

        result = await self.parser.parseVoice('mary space')
        assert result is MicrosoftSamVoice.MARY_SPACE

        result = await self.parser.parseVoice('maryspace')
        assert result is MicrosoftSamVoice.MARY_SPACE

    @pytest.mark.asyncio
    async def test_parseVoice_withMaryInSpace(self):
        result = await self.parser.parseVoice('mary_in_space')
        assert result is MicrosoftSamVoice.MARY_SPACE

        result = await self.parser.parseVoice('mary-in-space')
        assert result is MicrosoftSamVoice.MARY_SPACE

        result = await self.parser.parseVoice('mary in space')
        assert result is MicrosoftSamVoice.MARY_SPACE

        result = await self.parser.parseVoice('maryinspace')
        assert result is MicrosoftSamVoice.MARY_SPACE

    @pytest.mark.asyncio
    async def test_parseVoice_withMaryStadium(self):
        result = await self.parser.parseVoice('mary_stadium')
        assert result is MicrosoftSamVoice.MARY_STADIUM

        result = await self.parser.parseVoice('mary-stadium')
        assert result is MicrosoftSamVoice.MARY_STADIUM

        result = await self.parser.parseVoice('mary stadium')
        assert result is MicrosoftSamVoice.MARY_STADIUM

        result = await self.parser.parseVoice('marystadium')
        assert result is MicrosoftSamVoice.MARY_STADIUM

    @pytest.mark.asyncio
    async def test_parseVoice_withMaryTelephone(self):
        result = await self.parser.parseVoice('mary_telephone')
        assert result is MicrosoftSamVoice.MARY_TELEPHONE

        result = await self.parser.parseVoice('mary-telephone')
        assert result is MicrosoftSamVoice.MARY_TELEPHONE

        result = await self.parser.parseVoice('mary telephone')
        assert result is MicrosoftSamVoice.MARY_TELEPHONE

        result = await self.parser.parseVoice('marytelephone')
        assert result is MicrosoftSamVoice.MARY_TELEPHONE

    @pytest.mark.asyncio
    async def test_parseVoice_withMike(self):
        result = await self.parser.parseVoice('mike')
        assert result is MicrosoftSamVoice.MIKE

    @pytest.mark.asyncio
    async def test_parseVoice_withMikeHall(self):
        result = await self.parser.parseVoice('mike_hall')
        assert result is MicrosoftSamVoice.MIKE_HALL

        result = await self.parser.parseVoice('mike-hall')
        assert result is MicrosoftSamVoice.MIKE_HALL

        result = await self.parser.parseVoice('mike hall')
        assert result is MicrosoftSamVoice.MIKE_HALL

        result = await self.parser.parseVoice('mikehall')
        assert result is MicrosoftSamVoice.MIKE_HALL

    @pytest.mark.asyncio
    async def test_parseVoice_withMikeSpace(self):
        result = await self.parser.parseVoice('mike_space')
        assert result is MicrosoftSamVoice.MIKE_SPACE

        result = await self.parser.parseVoice('mike-space')
        assert result is MicrosoftSamVoice.MIKE_SPACE

        result = await self.parser.parseVoice('mike space')
        assert result is MicrosoftSamVoice.MIKE_SPACE

        result = await self.parser.parseVoice('mikespace')
        assert result is MicrosoftSamVoice.MIKE_SPACE

    @pytest.mark.asyncio
    async def test_parseVoice_withMikeInSpace(self):
        result = await self.parser.parseVoice('mike_in_space')
        assert result is MicrosoftSamVoice.MIKE_SPACE

        result = await self.parser.parseVoice('mike-in-space')
        assert result is MicrosoftSamVoice.MIKE_SPACE

        result = await self.parser.parseVoice('mike in space')
        assert result is MicrosoftSamVoice.MIKE_SPACE

        result = await self.parser.parseVoice('mikeinspace')
        assert result is MicrosoftSamVoice.MIKE_SPACE

    @pytest.mark.asyncio
    async def test_parseVoice_withMikeStadium(self):
        result = await self.parser.parseVoice('mike_stadium')
        assert result is MicrosoftSamVoice.MIKE_STADIUM

        result = await self.parser.parseVoice('mike-stadium')
        assert result is MicrosoftSamVoice.MIKE_STADIUM

        result = await self.parser.parseVoice('mike stadium')
        assert result is MicrosoftSamVoice.MIKE_STADIUM

        result = await self.parser.parseVoice('mikestadium')
        assert result is MicrosoftSamVoice.MIKE_STADIUM

    @pytest.mark.asyncio
    async def test_parseVoice_withMikeTelephone(self):
        result = await self.parser.parseVoice('mike_telephone')
        assert result is MicrosoftSamVoice.MIKE_TELEPHONE

        result = await self.parser.parseVoice('mike-telephone')
        assert result is MicrosoftSamVoice.MIKE_TELEPHONE

        result = await self.parser.parseVoice('mike telephone')
        assert result is MicrosoftSamVoice.MIKE_TELEPHONE

        result = await self.parser.parseVoice('miketelephone')
        assert result is MicrosoftSamVoice.MIKE_TELEPHONE

    @pytest.mark.asyncio
    async def test_parseVoice_withMikePhone(self):
        result = await self.parser.parseVoice('mike_phone')
        assert result is MicrosoftSamVoice.MIKE_TELEPHONE

        result = await self.parser.parseVoice('mike-phone')
        assert result is MicrosoftSamVoice.MIKE_TELEPHONE

        result = await self.parser.parseVoice('mike phone')
        assert result is MicrosoftSamVoice.MIKE_TELEPHONE

        result = await self.parser.parseVoice('mikephone')
        assert result is MicrosoftSamVoice.MIKE_TELEPHONE

    @pytest.mark.asyncio
    async def test_parseVoice_withRobo1(self):
        result = await self.parser.parseVoice('robo_1')
        assert result is MicrosoftSamVoice.ROBO_1

        result = await self.parser.parseVoice('robo-1')
        assert result is MicrosoftSamVoice.ROBO_1

        result = await self.parser.parseVoice('robo 1')
        assert result is MicrosoftSamVoice.ROBO_1

        result = await self.parser.parseVoice('robo1')
        assert result is MicrosoftSamVoice.ROBO_1

        result = await self.parser.parseVoice('robo')
        assert result is MicrosoftSamVoice.ROBO_1

    @pytest.mark.asyncio
    async def test_parseVoice_withRobo2(self):
        result = await self.parser.parseVoice('robo_2')
        assert result is MicrosoftSamVoice.ROBO_2

        result = await self.parser.parseVoice('robo-2')
        assert result is MicrosoftSamVoice.ROBO_2

        result = await self.parser.parseVoice('robo 2')
        assert result is MicrosoftSamVoice.ROBO_2

        result = await self.parser.parseVoice('robo2')
        assert result is MicrosoftSamVoice.ROBO_2

    @pytest.mark.asyncio
    async def test_parseVoice_withRobo3(self):
        result = await self.parser.parseVoice('robo_3')
        assert result is MicrosoftSamVoice.ROBO_3

        result = await self.parser.parseVoice('robo-3')
        assert result is MicrosoftSamVoice.ROBO_3

        result = await self.parser.parseVoice('robo 3')
        assert result is MicrosoftSamVoice.ROBO_3

        result = await self.parser.parseVoice('robo3')
        assert result is MicrosoftSamVoice.ROBO_3

    @pytest.mark.asyncio
    async def test_parseVoice_withRobo4(self):
        result = await self.parser.parseVoice('robo_4')
        assert result is MicrosoftSamVoice.ROBO_4

        result = await self.parser.parseVoice('robo-4')
        assert result is MicrosoftSamVoice.ROBO_4

        result = await self.parser.parseVoice('robo 4')
        assert result is MicrosoftSamVoice.ROBO_4

        result = await self.parser.parseVoice('robo4')
        assert result is MicrosoftSamVoice.ROBO_4

    @pytest.mark.asyncio
    async def test_parseVoice_withRobo5(self):
        result = await self.parser.parseVoice('robo_5')
        assert result is MicrosoftSamVoice.ROBO_5

        result = await self.parser.parseVoice('robo-5')
        assert result is MicrosoftSamVoice.ROBO_5

        result = await self.parser.parseVoice('robo 5')
        assert result is MicrosoftSamVoice.ROBO_5

        result = await self.parser.parseVoice('robo5')
        assert result is MicrosoftSamVoice.ROBO_5

    @pytest.mark.asyncio
    async def test_parseVoice_withRobo6(self):
        result = await self.parser.parseVoice('robo_6')
        assert result is MicrosoftSamVoice.ROBO_6

        result = await self.parser.parseVoice('robo-6')
        assert result is MicrosoftSamVoice.ROBO_6

        result = await self.parser.parseVoice('robo 6')
        assert result is MicrosoftSamVoice.ROBO_6

        result = await self.parser.parseVoice('robo6')
        assert result is MicrosoftSamVoice.ROBO_6

    @pytest.mark.asyncio
    async def test_parseVoice_withSam(self):
        result = await self.parser.parseVoice('sam')
        assert result is MicrosoftSamVoice.SAM

    @pytest.mark.asyncio
    async def test_requireVoice_withAdultFemale1(self):
        result = await self.parser.requireVoice('adult_female_1')
        assert result is MicrosoftSamVoice.ADULT_FEMALE_1

        result = await self.parser.requireVoice('adult-female-1')
        assert result is MicrosoftSamVoice.ADULT_FEMALE_1

        result = await self.parser.requireVoice('adult female 1')
        assert result is MicrosoftSamVoice.ADULT_FEMALE_1

        result = await self.parser.requireVoice('adult_female')
        assert result is MicrosoftSamVoice.ADULT_FEMALE_1

        result = await self.parser.requireVoice('adult-female')
        assert result is MicrosoftSamVoice.ADULT_FEMALE_1

        result = await self.parser.requireVoice('adult female')
        assert result is MicrosoftSamVoice.ADULT_FEMALE_1

        result = await self.parser.requireVoice('adultfemale')
        assert result is MicrosoftSamVoice.ADULT_FEMALE_1

    @pytest.mark.asyncio
    async def test_requireVoice_withAdultMale1(self):
        result = await self.parser.requireVoice('adult_male_1')
        assert result is MicrosoftSamVoice.ADULT_MALE_1

        result = await self.parser.requireVoice('adult-male-1')
        assert result is MicrosoftSamVoice.ADULT_MALE_1

        result = await self.parser.requireVoice('adult male 1')
        assert result is MicrosoftSamVoice.ADULT_MALE_1

        result = await self.parser.requireVoice('adult_male')
        assert result is MicrosoftSamVoice.ADULT_MALE_1

        result = await self.parser.requireVoice('adult male')
        assert result is MicrosoftSamVoice.ADULT_MALE_1

        result = await self.parser.requireVoice('adultmale')
        assert result is MicrosoftSamVoice.ADULT_MALE_1

    @pytest.mark.asyncio
    async def test_requireVoice_withBonziBuddy(self):
        result = await self.parser.requireVoice('bonzi_buddy')
        assert result is MicrosoftSamVoice.BONZI_BUDDY

    @pytest.mark.asyncio
    async def test_requireVoice_withMary(self):
        result = await self.parser.requireVoice('mary')
        assert result is MicrosoftSamVoice.MARY

    @pytest.mark.asyncio
    async def test_requireVoice_withMike(self):
        result = await self.parser.requireVoice('mike')
        assert result is MicrosoftSamVoice.MIKE

    @pytest.mark.asyncio
    async def test_requireVoice_withRobo1(self):
        result = await self.parser.requireVoice('robo_1')
        assert result is MicrosoftSamVoice.ROBO_1

        result = await self.parser.requireVoice('robo-1')
        assert result is MicrosoftSamVoice.ROBO_1

        result = await self.parser.requireVoice('robo_1')
        assert result is MicrosoftSamVoice.ROBO_1

        result = await self.parser.requireVoice('robo1')
        assert result is MicrosoftSamVoice.ROBO_1

        result = await self.parser.requireVoice('robo')
        assert result is MicrosoftSamVoice.ROBO_1

    @pytest.mark.asyncio
    async def test_requireVoice_withSam(self):
        result = await self.parser.requireVoice('sam')
        assert result is MicrosoftSamVoice.SAM

    def test_sanity(self):
        assert self.parser is not None
        assert isinstance(self.parser, MicrosoftSamJsonParser)
        assert isinstance(self.parser, MicrosoftSamJsonParserInterface)

    @pytest.mark.asyncio
    async def test_serializeVoice_withAdultFemale1(self):
        result = await self.parser.serializeVoice(MicrosoftSamVoice.ADULT_FEMALE_1)
        assert result == 'adult_female_1'

    @pytest.mark.asyncio
    async def test_serializeVoice_withAdultMale1(self):
        result = await self.parser.serializeVoice(MicrosoftSamVoice.ADULT_MALE_1)
        assert result == 'adult_male_1'

    @pytest.mark.asyncio
    async def test_serializeVoice_withBonziBuddy(self):
        result = await self.parser.serializeVoice(MicrosoftSamVoice.BONZI_BUDDY)
        assert result == 'bonzi_buddy'

    @pytest.mark.asyncio
    async def test_serializeVoice_withMary(self):
        result = await self.parser.serializeVoice(MicrosoftSamVoice.MARY)
        assert result == 'mary'

    @pytest.mark.asyncio
    async def test_serializeVoice_withMike(self):
        result = await self.parser.serializeVoice(MicrosoftSamVoice.MIKE)
        assert result == 'mike'

    @pytest.mark.asyncio
    async def test_serializeVoice_withSam(self):
        result = await self.parser.serializeVoice(MicrosoftSamVoice.SAM)
        assert result == 'sam'
