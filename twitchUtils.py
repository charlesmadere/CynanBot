from typing import List

import CynanBotCommon.utils as utils


async def safeSend(messageable, message: str):
    if messageable is None:
        raise ValueError(f'messageable argument is malformed: \"{messageable}\"')
    elif not utils.isValidStr(message):
        return

    messages: List[str] = list()
    messages.append(message)

    index = 0

    while index < len(messages):
        m = messages[index]

        if len(m) >= 500:
            spaceIndex = m.rfind(' ')

            while spaceIndex >= 450:
                spaceIndex = m[0:spaceIndex].rfind(' ')

            if spaceIndex == -1:
                raise RuntimeError(f'This message is insane and can\'t be sent (len is {len(message)}):\n{message}')

            messages[index] = m[0:spaceIndex].strip()
            messages.append(m[spaceIndex:len(m)].strip())

        index = index + 1

    if len(messages) > 3:
        raise RuntimeError(f'This message is just too long and won\'t be sent (len is {len(message)}):\n{message}')

    for m in messages:
        await messageable.send(m)
