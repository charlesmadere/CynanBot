import random
import re
import traceback
from typing import Any, Dict, List, Optional, Pattern

import CynanBot.misc.utils as utils
from CynanBot.network.exceptions import GenericNetworkException
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.pkmn.pokepediaContestType import PokepediaContestType
from CynanBot.pkmn.pokepediaDamageClass import PokepediaDamageClass
from CynanBot.pkmn.pokepediaElementType import PokepediaElementType
from CynanBot.pkmn.pokepediaGeneration import PokepediaGeneration
from CynanBot.pkmn.pokepediaMachine import PokepediaMachine
from CynanBot.pkmn.pokepediaMachineType import PokepediaMachineType
from CynanBot.pkmn.pokepediaMove import PokepediaMove
from CynanBot.pkmn.pokepediaMoveGeneration import PokepediaMoveGeneration
from CynanBot.pkmn.pokepediaNature import PokepediaNature
from CynanBot.pkmn.pokepediaPokemon import PokepediaPokemon
from CynanBot.pkmn.pokepediaStat import PokepediaStat
from CynanBot.pkmn.pokepediaUtilsInterface import PokepediaUtilsInterface
from CynanBot.timber.timberInterface import TimberInterface


class PokepediaRepository():

    def __init__(
        self,
        networkClientProvider: NetworkClientProvider,
        pokepediaUtils: PokepediaUtilsInterface,
        timber: TimberInterface
    ):
        assert isinstance(networkClientProvider, NetworkClientProvider), f"malformed {networkClientProvider=}"
        assert isinstance(pokepediaUtils, PokepediaUtilsInterface), f"malformed {pokepediaUtils=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"

        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__pokepediaUtils: PokepediaUtilsInterface = pokepediaUtils
        self.__timber: TimberInterface = timber

        self.__pokeApiIdRegEx: Pattern = re.compile(r'^.+\/(\d+)\/$', re.IGNORECASE)

    async def __buildMachineFromJsonResponse(self, jsonResponse: Dict[str, Any]) -> PokepediaMachine:
        if not utils.hasItems(jsonResponse):
            raise ValueError(f'jsonResponse argument is malformed: \"{jsonResponse}\"')

        generation = PokepediaGeneration.fromStr(utils.getStrFromDict(jsonResponse['version_group'], 'name'))
        machineName = utils.getStrFromDict(jsonResponse['item'], 'name').upper()
        machineType = PokepediaMachineType.fromStr(machineName)
        machineNumber = await self.__pokepediaUtils.getMachineNumber(machineName)

        return PokepediaMachine(
            machineId = utils.getIntFromDict(jsonResponse, 'id'),
            machineNumber = machineNumber,
            generation = generation,
            machineType = machineType,
            machineName = machineName,
            moveName = utils.getStrFromDict(jsonResponse['move'], 'name')
        )

    async def __buildMoveFromJsonResponse(self, jsonResponse: Dict[str, Any]) -> PokepediaMove:
        if not utils.hasItems(jsonResponse):
            raise ValueError(f'jsonResponse argument is malformed: \"{jsonResponse}\"')

        contestType: Optional[PokepediaContestType] = None
        if utils.hasItems(jsonResponse.get('contest_type')):
            contestType = PokepediaContestType.fromStr(utils.getStrFromDict(jsonResponse['contest_type'], 'name', fallback = ''))

        damageClass = PokepediaDamageClass.fromStr(jsonResponse['damage_class']['name'])

        generationMachines: Optional[Dict[PokepediaGeneration, List[PokepediaMachine]]] = None
        if utils.hasItems(jsonResponse.get('machines')):
            generationMachines = await self.__fetchMoveMachines(jsonResponse['machines'])

        generationMoves = await self.__getMoveGenerationDictionary(jsonResponse)

        critRate = 0
        drain = 0
        flinchChance = 0
        if 'meta' in jsonResponse and utils.hasItems(jsonResponse['meta']):
            critRate = utils.getIntFromDict(jsonResponse['meta'], 'crit_rate', fallback = 0)
            drain = utils.getIntFromDict(jsonResponse['meta'], 'drain', fallback = 0)
            flinchChance = utils.getIntFromDict(jsonResponse['meta'], 'flinch_chance', fallback = 0)

        initialGeneration = PokepediaGeneration.fromStr(utils.getStrFromDict(jsonResponse['generation'], 'name'))

        return PokepediaMove(
            contestType = contestType,
            damageClass = damageClass,
            generationMachines = generationMachines,
            generationMoves = generationMoves,
            critRate = critRate,
            drain = drain,
            flinchChance = flinchChance,
            moveId = utils.getIntFromDict(jsonResponse, 'id'),
            initialGeneration = initialGeneration,
            description = await self.__getEnDescription(jsonResponse),
            name = await self.__getEnName(jsonResponse),
            rawName = utils.getStrFromDict(jsonResponse, 'name')
        )

    async def __buildPokemonFromJsonResponse(self, jsonResponse: Dict[str, Any]) -> PokepediaPokemon:
        if not utils.hasItems(jsonResponse):
            raise ValueError(f'jsonResponse argument is malformed: \"{jsonResponse}\"')

        pokedexId = utils.getIntFromDict(jsonResponse, 'id')
        initialGeneration = PokepediaGeneration.fromPokedexId(pokedexId)

        generationElementTypes = await self.__getElementTypeGenerationDictionary(
            jsonResponse = jsonResponse,
            initialGeneration = initialGeneration
        )

        return PokepediaPokemon(
            generationElementTypes = generationElementTypes,
            initialGeneration = initialGeneration,
            height = utils.getIntFromDict(jsonResponse, 'height'),
            pokedexId = pokedexId,
            weight = utils.getIntFromDict(jsonResponse, 'weight'),
            name = utils.getStrFromDict(jsonResponse, 'name').title()
        )

    async def fetchMachine(self, machineId: int) -> PokepediaMachine:
        if not utils.isValidInt(machineId):
            raise ValueError(f'machineId argument is malformed: \"{machineId}\"')

        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(f'https://pokeapi.co/api/v2/machine/{machineId}')
        except GenericNetworkException as e:
            self.__timber.log('PokepediaRepository', f'Encountered network error from PokeAPI when fetching machine with ID \"{machineId}\": {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'PokepediaRepository encountered network error from PokeAPI when fetching machine with ID \"{machineId}\": {e}')

        if response.getStatusCode() != 200:
            self.__timber.log('PokepediaRepository', f'Encountered non-200 HTTP status code from PokeAPI when fetching machine with ID \"{machineId}\": \"{response.getStatusCode()}\"')
            raise GenericNetworkException(f'PokepediaRepository encountered non-200 HTTP status code from PokeAPI when fetching machine with ID \"{machineId}\": \"{response.getStatusCode()}\"')

        jsonResponse: Optional[Dict[str, Any]] = await response.json()
        await response.close()

        if not utils.hasItems(jsonResponse):
            self.__timber.log('PokepediaRepository', f'Encountered data error from PokeAPI when fetching machine with ID \"{machineId}\": {jsonResponse}')
            raise GenericNetworkException(f'PokepediaRepository encountered data error from PokeAPI when fetching machine with ID \"{machineId}\": {jsonResponse}')

        return await self.__buildMachineFromJsonResponse(jsonResponse)

    async def fetchMove(self, moveId: int) -> PokepediaMove:
        if not utils.isValidInt(moveId):
            raise ValueError(f'moveId argument is malformed: \"{moveId}\"')

        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(f'https://pokeapi.co/api/v2/move/{moveId}')
        except GenericNetworkException as e:
            self.__timber.log('PokepediaRepository', f'Encountered network error from PokeAPI when fetching move with ID \"{moveId}\": {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'PokepediaRepository encountered network error from PokeAPI when fetching move with ID \"{moveId}\": {e}')

        if response.getStatusCode() != 200:
            self.__timber.log('PokepediaRepository', f'Encountered non-200 HTTP status code from PokeAPI when fetching move with ID \"{moveId}\": \"{response.getStatusCode()}\"')
            raise GenericNetworkException(f'PokepediaRepository encountered non-200 HTTP status code from PokeAPI when fetching move with ID \"{moveId}\": \"{response.getStatusCode()}\"')

        jsonResponse: Optional[Dict[str, Any]] = await response.json()
        await response.close()

        if not utils.hasItems(jsonResponse):
            self.__timber.log('PokepediaRepository', f'Encountered data error from PokeAPI when fetching move with ID \"{moveId}\": {jsonResponse}')
            raise GenericNetworkException(f'PokepediaRepository encountered data error from PokeAPI when fetching move with ID \"{moveId}\": {jsonResponse}')

        return await self.__buildMoveFromJsonResponse(jsonResponse)

    async def __fetchMoveMachines(
        self,
        machinesJson: Optional[List[Dict[str, Any]]]
    ) -> Optional[Dict[PokepediaGeneration, List[PokepediaMachine]]]:
        if not utils.hasItems(machinesJson):
            return None

        generationMachines: Dict[PokepediaGeneration, List[PokepediaMachine]] = dict()

        for machineJson in machinesJson:
            machineUrl = utils.getStrFromDict(machineJson['machine'], 'url', fallback = '')
            if not utils.isValidStr(machineUrl):
                continue

            machineIdMatch = self.__pokeApiIdRegEx.fullmatch(machineUrl)
            if machineIdMatch is None:
                continue

            machineIdStr = machineIdMatch.group(1)
            if not utils.isValidStr(machineIdStr):
                continue

            machineIdInt: Optional[int] = None

            try:
                machineIdInt = int(machineIdStr)
            except ValueError as e:
                self.__timber.log('PokepediaRepository', f'Encountered exception when attempting to convert a machine ID into an int: \"{machineIdStr}\": {e}', e, traceback.format_exc())

            if not utils.isValidInt(machineIdInt):
                continue

            machine = await self.fetchMachine(machineIdInt)

            if machine.getGeneration() not in generationMachines:
                generationMachines[machine.getGeneration()] = list()

            generationMachines[machine.getGeneration()].append(machine)

        for machines in generationMachines.values():
            machines.sort(key = lambda machine: (machine.getGeneration(), machine.getMachineId()))

        return generationMachines

    async def fetchNature(self, natureId: int) -> PokepediaNature:
        if not utils.isValidInt(natureId):
            raise ValueError(f'natureId argument is malformed: \"{natureId}\"')

        return PokepediaNature.fromInt(natureId)

    async def fetchRandomMove(self, maxGeneration: PokepediaGeneration) -> PokepediaMove:
        assert isinstance(maxGeneration, PokepediaGeneration), f"malformed {maxGeneration=}"

        randomMoveId = random.randint(1, maxGeneration.getMaxMoveId())
        return await self.fetchMove(randomMoveId)

    async def fetchRandomNature(self) -> PokepediaNature:
        allNatures = list(PokepediaNature)
        randomNature = random.choice(allNatures)
        return await self.fetchNature(randomNature.getNatureId())

    async def fetchRandomPokemon(self, maxGeneration: PokepediaGeneration) -> PokepediaPokemon:
        assert isinstance(maxGeneration, PokepediaGeneration), f"malformed {maxGeneration=}"

        randomPokemonId = random.randint(1, maxGeneration.getMaxPokedexId())
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(f'https://pokeapi.co/api/v2/pokemon/{randomPokemonId}')
        except GenericNetworkException as e:
            self.__timber.log('PokepediaRepository', f'Encountered network error from PokeAPI when fetching Pokemon with ID \"{randomPokemonId}\": {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'PokepediaRepository encountered network error from PokeAPI when fetching Pokemon with ID \"{randomPokemonId}\": {e}')

        if response.getStatusCode() != 200:
            self.__timber.log('PokepediaRepository', f'Encountered non-200 HTTP status code from PokeAPI when fetching Pokemon with ID \"{randomPokemonId}\": \"{response.getStatusCode()}\"')
            raise GenericNetworkException(f'PokepediaRepository encountered non-200 HTTP status code from PokeAPI when fetching Pokemon with ID \"{randomPokemonId}\": \"{response.getStatusCode()}\"')

        jsonResponse: Optional[Dict[str, Any]] = await response.json()
        await response.close()

        if not utils.hasItems(jsonResponse):
            self.__timber.log('PokepediaRepository', f'Encountered data error from PokeAPI when fetching Pokemon with ID \"{randomPokemonId}\": {jsonResponse}')
            raise GenericNetworkException(f'PokepediaRepository encountered data error from PokeAPI when fetching Pokemon with ID \"{randomPokemonId}\": {jsonResponse}')

        return await self.__buildPokemonFromJsonResponse(jsonResponse)

    async def fetchRandomStat(self) -> PokepediaStat:
        allStats = list(PokepediaStat)
        randomStat = random.choice(allStats)
        return await self.fetchStat(randomStat.getStatId())

    async def fetchStat(self, statId: int) -> PokepediaStat:
        if not utils.isValidInt(statId):
            raise ValueError(f'statId argument is malformed: \"{statId}\"')

        return PokepediaStat.fromInt(statId)

    async def __getElementTypeGenerationDictionary(
        self,
        jsonResponse: Dict[str, Any],
        initialGeneration: PokepediaGeneration
    ) -> Dict[PokepediaGeneration, List[PokepediaElementType]]:
        if jsonResponse is None:
            raise ValueError(f'jsonResponse argument is malformed: \"{jsonResponse}\"')
        assert isinstance(initialGeneration, PokepediaGeneration), f"malformed {initialGeneration=}"

        currentTypesJson: Optional[List[Dict[str, Any]]] = jsonResponse.get('types')
        if not utils.hasItems(currentTypesJson):
            raise ValueError(f'\"types\" field in JSON response is null or empty: {jsonResponse}')

        # begin with current generation types
        currentTypesList: List[PokepediaElementType] = list()
        for currentTypeJson in currentTypesJson:
            currentTypesList.append(PokepediaElementType.fromStr(currentTypeJson['type']['name']))

        pastTypesJson: Optional[List[Dict[str, Any]]] = jsonResponse.get('past_types')
        if pastTypesJson is None:
            raise ValueError(f'\"past_types\" field in JSON response is null: {jsonResponse}')

        elementTypeGenerationDictionary: Dict[PokepediaGeneration, List[PokepediaElementType]] = dict()

        # iterate backwards and insert into dictionary once a generation is found.
        # then 'un-patch' for previous generations.
        for pokepediaGeneration in reversed(PokepediaGeneration):
            for pastTypeJson in pastTypesJson:
                generation = PokepediaGeneration.fromStr(pastTypeJson['generation']['name'])

                if generation is pokepediaGeneration:
                    currentTypesList = list()

                    typesJson = pastTypeJson.get('types')
                    if not utils.hasItems(typesJson):
                        raise ValueError(f'\"types\" field in \"past_types\" JSON array is null or empty: {jsonResponse}')

                    for typeJson in typesJson:
                        currentTypesList.append(PokepediaElementType.fromStr(typeJson['type']['name']))

            elementTypeGenerationDictionary[pokepediaGeneration] = currentTypesList

        # only store typing for generations where this Pokemon actually existed
        for pokepediaGeneration in PokepediaGeneration:
            if pokepediaGeneration.value < initialGeneration.value:
                del elementTypeGenerationDictionary[pokepediaGeneration]

        # remove duplicates
        removeDuplicatesTypesList: Optional[List[PokepediaElementType]] = None
        for pokepediaGeneration in PokepediaGeneration:
            if pokepediaGeneration in elementTypeGenerationDictionary:
                if removeDuplicatesTypesList is None:
                    removeDuplicatesTypesList = elementTypeGenerationDictionary[pokepediaGeneration]
                elif removeDuplicatesTypesList == elementTypeGenerationDictionary[pokepediaGeneration]:
                    del elementTypeGenerationDictionary[pokepediaGeneration]
                else:
                    removeDuplicatesTypesList = elementTypeGenerationDictionary[pokepediaGeneration]

        return elementTypeGenerationDictionary

    async def __getEnDescription(self, jsonResponse: Dict[str, Any]) -> str:
        if not utils.hasItems(jsonResponse):
            raise ValueError(f'jsonResponse argument is malformed: \"{jsonResponse}\"')

        flavorTextEntries = jsonResponse.get('flavor_text_entries')
        if not utils.hasItems(flavorTextEntries):
            raise ValueError(f'\"flavor_text_entries\" field in JSON response is null or empty: {jsonResponse}')

        for flavorTextEntry in flavorTextEntries:
            if flavorTextEntry['language']['name'] == 'en':
                return utils.getStrFromDict(flavorTextEntry, 'flavor_text', clean = True)

        raise RuntimeError(f'can\'t find \"en\" language name in \"flavor_text_entries\" field: {jsonResponse}')

    async def __getEnName(self, jsonResponse: Dict[str, Any]) -> str:
        if not utils.hasItems(jsonResponse):
            raise ValueError(f'jsonResponse argument is malformed: \"{jsonResponse}\"')

        names = jsonResponse.get('names')
        if not utils.hasItems(names):
            raise ValueError(f'\"names\" field in JSON response is null or empty: {jsonResponse}')

        for name in names:
            if name['language']['name'] == 'en':
                return utils.getStrFromDict(name, 'name', clean = True).title()

        raise RuntimeError(f'can\'t find \"en\" language name in \"names\" field: {jsonResponse}')

    async def __getMoveGenerationDictionary(
        self,
        jsonResponse: Dict[str, Any]
    ) -> Dict[PokepediaGeneration, PokepediaMoveGeneration]:
        if not utils.hasItems(jsonResponse):
            raise ValueError(f'jsonResponse argument is malformed: \"{jsonResponse}\"')

        # begin with current generation stats
        accuracy: Optional[int] = jsonResponse.get('accuracy')
        power: Optional[int] = jsonResponse.get('power')
        pp = utils.getIntFromDict(jsonResponse, 'pp')
        damageClass = PokepediaDamageClass.fromStr(jsonResponse['damage_class']['name'])
        elementType = PokepediaElementType.fromStr(jsonResponse['type']['name'])
        move: Optional[PokepediaMoveGeneration] = None

        pastValuesJson = jsonResponse.get('past_values')
        if pastValuesJson is None:
            raise ValueError(f'\"past_values\" field in JSON response is null: {jsonResponse}')

        moveGenerationDictionary: Dict[PokepediaGeneration, PokepediaMoveGeneration] = dict()

        # iterate backwards and insert into dictionary once a generation is found.
        # then 'un-patch' for previous generations.
        for pokepediaGeneration in reversed(PokepediaGeneration):
            for pastValueJson in pastValuesJson:
                generation = PokepediaGeneration.fromStr(pastValueJson['version_group']['name'])

                if generation is pokepediaGeneration:
                    if generation.isEarlyGeneration() and damageClass is not PokepediaDamageClass.STATUS:
                        damageClass = PokepediaDamageClass.getTypeBasedDamageClass(elementType)

                    moveGenerationDictionary[generation] = PokepediaMoveGeneration(
                        accuracy = accuracy,
                        power = power,
                        pp = pp,
                        damageClass = damageClass,
                        elementType = elementType,
                        generation = generation
                    )

                    if utils.isValidNum(pastValueJson.get('accuracy')):
                        accuracy = utils.getIntFromDict(pastValueJson, 'accuracy')

                    if utils.isValidNum(pastValueJson.get('power')):
                        power = utils.getIntFromDict(pastValueJson, 'power')

                    if utils.isValidNum(pastValueJson.get('pp')):
                        pp = utils.getIntFromDict(pastValueJson, 'pp')

                    if pastValueJson.get('type') is not None:
                        elementType = PokepediaElementType.fromStr(pastValueJson['type']['name'])

        generation = PokepediaGeneration.fromStr(jsonResponse['generation']['name'])

        if generation.isEarlyGeneration() and damageClass is not PokepediaDamageClass.STATUS:
            damageClass = PokepediaDamageClass.getTypeBasedDamageClass(elementType)

        move = PokepediaMoveGeneration(
            accuracy = accuracy,
            power = power,
            pp = pp,
            damageClass = damageClass,
            elementType = elementType,
            generation = generation
        )

        moveGenerationDictionary[generation] = move

        # scan for case where gen4+ type changed but not reflected in past_values JSON array
        if PokepediaGeneration.GENERATION_4 not in moveGenerationDictionary:
            if PokepediaGeneration.GENERATION_3 in moveGenerationDictionary:
                if moveGenerationDictionary[PokepediaGeneration.GENERATION_3].getDamageClass() != damageClass:
                    move = PokepediaMoveGeneration(
                        accuracy = moveGenerationDictionary[PokepediaGeneration.GENERATION_3].getAccuracy(),
                        power = moveGenerationDictionary[PokepediaGeneration.GENERATION_3].getPower(),
                        pp = moveGenerationDictionary[PokepediaGeneration.GENERATION_3].getPp(),
                        damageClass = damageClass,
                        elementType = moveGenerationDictionary[PokepediaGeneration.GENERATION_3].getElementType(),
                        generation = PokepediaGeneration.GENERATION_4
                    )

                    moveGenerationDictionary[PokepediaGeneration.GENERATION_4] = move
            elif PokepediaGeneration.GENERATION_2 in moveGenerationDictionary:
                if moveGenerationDictionary[PokepediaGeneration.GENERATION_2].getDamageClass() != damageClass:
                    move = PokepediaMoveGeneration(
                        accuracy = moveGenerationDictionary[PokepediaGeneration.GENERATION_2].getAccuracy(),
                        power = moveGenerationDictionary[PokepediaGeneration.GENERATION_2].getPower(),
                        pp = moveGenerationDictionary[PokepediaGeneration.GENERATION_2].getPp(),
                        damageClass = damageClass,
                        elementType = moveGenerationDictionary[PokepediaGeneration.GENERATION_2].getElementType(),
                        generation = PokepediaGeneration.GENERATION_4
                    )

                    moveGenerationDictionary[PokepediaGeneration.GENERATION_4] = move
            elif PokepediaGeneration.GENERATION_1 in moveGenerationDictionary:
                if moveGenerationDictionary[PokepediaGeneration.GENERATION_1].getDamageClass() != damageClass:
                    move = PokepediaMoveGeneration(
                        accuracy = moveGenerationDictionary[PokepediaGeneration.GENERATION_1].getAccuracy(),
                        power = moveGenerationDictionary[PokepediaGeneration.GENERATION_1].getPower(),
                        pp = moveGenerationDictionary[PokepediaGeneration.GENERATION_1].getPp(),
                        damageClass = damageClass,
                        elementType = moveGenerationDictionary[PokepediaGeneration.GENERATION_1].getElementType(),
                        generation = PokepediaGeneration.GENERATION_4
                    )

                    moveGenerationDictionary[PokepediaGeneration.GENERATION_4] = move

        # This loop goes through the dictionary of generational moves we've now built up and stored
        # within moveGenerationDictionary and removes any generations that are exact duplicates,
        # UNLESS there exists a generation between the duplicate(s) that is different.
        move = None
        for pokepediaGeneration in PokepediaGeneration:
            if pokepediaGeneration not in moveGenerationDictionary:
                continue
            elif move is None:
                move = moveGenerationDictionary[pokepediaGeneration]
            else:
                comparison = moveGenerationDictionary[pokepediaGeneration]

                if move.getAccuracy() == comparison.getAccuracy() and move.getDamageClass() is comparison.getDamageClass() and move.getElementType() is comparison.getElementType() and move.getPower() == comparison.getPower() and move.getPp() == comparison.getPp():
                    del moveGenerationDictionary[pokepediaGeneration]

                move = comparison

        return moveGenerationDictionary

    async def searchMoves(self, name: str) -> PokepediaMove:
        if not utils.isValidStr(name):
            raise ValueError(f'name argument is malformed: \"{name}\"')

        name = utils.cleanStr(name)
        name = name.replace(' ', '-')
        self.__timber.log('PokepediaRepository', f'Searching PokeAPI for move \"{name}\"...')
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(f'https://pokeapi.co/api/v2/move/{name}/')
        except GenericNetworkException as e:
            self.__timber.log('PokepediaRepository', f'Encountered network error from PokeAPI when searching for \"{name}\" move: {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'PokepediaRepository encountered network error from PokeAPI when searching for \"{name}\" move: {e}')

        if response.getStatusCode() != 200:
            self.__timber.log('PokepediaRepository', f'Encountered non-200 HTTP status code from PokeAPI when searching for \"{name}\" move: \"{response.getStatusCode()}\"')
            raise GenericNetworkException(f'PokepediaRepository encountered non-200 HTTP status code from PokeAPI when searching for \"{name}\" move: \"{response.getStatusCode()}\"')

        jsonResponse: Optional[Dict[str, Any]] = await response.json()
        await response.close()

        if not utils.hasItems(jsonResponse):
            self.__timber.log('PokepediaRepository', f'Encountered data error from PokeAPI when searching for \"{name}\" move: {jsonResponse}')
            raise GenericNetworkException(f'PokepediaRepository encountered data error from PokeAPI when searching for \"{name}\" move: {jsonResponse}')

        return await self.__buildMoveFromJsonResponse(jsonResponse)

    async def searchPokemon(self, name: str) -> PokepediaPokemon:
        if not utils.isValidStr(name):
            raise ValueError(f'name argument is malformed: \"{name}\"')

        name = utils.cleanStr(name)
        name = name.replace(' ', '-')
        self.__timber.log('PokepediaRepository', f'Searching PokeAPI for Pokemon \"{name}\"...')
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(f'https://pokeapi.co/api/v2/pokemon/{name}/')
        except GenericNetworkException as e:
            self.__timber.log('PokepediaRepository', f'Encountered network error from PokeAPI when searching for \"{name}\" Pokemon: {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'PokepediaRepository encountered network error from PokeAPI when searching for \"{name}\" Pokemon: {e}')

        if response.getStatusCode() != 200:
            self.__timber.log('PokepediaRepository', f'Encountered non-200 HTTP status code from PokeAPI when searching for \"{name}\" Pokemon: \"{response.getStatusCode()}\"')
            raise GenericNetworkException(f'PokepediaRepository encountered non-200 HTTP status code from PokeAPI when searching for \"{name}\" Pokemon: \"{response.getStatusCode()}\"')

        jsonResponse: Optional[Dict[str, Any]] = await response.json()
        await response.close()

        if not utils.hasItems(jsonResponse):
            self.__timber.log('PokepediaRepository', f'Encountered data error from PokeAPI when searching for \"{name}\" Pokemon: {jsonResponse}')
            raise GenericNetworkException(f'PokepediaRepository encountered data error from PokeAPI when searching for \"{name}\" Pokemon: {jsonResponse}')

        return await self.__buildPokemonFromJsonResponse(jsonResponse)
