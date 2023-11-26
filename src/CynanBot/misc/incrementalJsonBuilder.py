import json
from typing import Any, Dict, List, Optional

import CynanBot.misc.utils as utils


class IncrementalJsonBuilder():

    def __init__(self):
        self.__jsonString: Optional[str] = None

    async def buildDictionariesOrAppendInternalJsonCache(
        self,
        jsonString: Optional[str]
    ) -> Optional[List[Dict[Any, Any]]]:
        if not utils.isValidStr(jsonString):
            return None

        if self.__jsonString is None:
            self.__jsonString = jsonString
        else:
            self.__jsonString += jsonString

        if self.__jsonString[0] != '{':
            raise RuntimeError(f'Invalid internal JSON string state: \"{self.__jsonString}\"')

        inString: Optional[str] = None
        skipNext = False
        depth = 0
        index = 0
        dictionaries: List[Dict[Any, Any]] = list()

        for i in range(len(self.__jsonString)):
            if skipNext:
                skipNext = False
                continue

            c = self.__jsonString[i]

            if c == '\\':
                skipNext = True
            elif c == inString:
                # if we're in a string (inString is not None) and we've found a matching end,
                # then exit the string
                inString = None
            elif not inString and (c == "'" or c == '"'):
                # if we aren't in a string and we find the start of a string, mark it
                inString = c
            elif inString:
                # we're processing a character in a string, so we don't care about it
                pass
            elif c == '{':
                # mark that we're entering a new object
                depth += 1
            elif c == '}':
                # exit out of the last object, then if we're outside all objects, we're done
                depth -= 1

                if depth == 0:
                    jsonStringToParse = self.__jsonString[index:i + 1]
                    index = i + 1
                    dictionaries.append(json.loads(jsonStringToParse))

        if index >= len(self.__jsonString):
            self.__jsonString = None
        else:
            self.__jsonString = self.__jsonString[index:]

        if len(dictionaries) == 0:
            return None
        else:
            return dictionaries
