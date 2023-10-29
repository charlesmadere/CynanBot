from typing import Any, Optional

x = 'hello'

def misc(query: str, *args: Optional[Any]):
    print(args is None)
    print(type(args))
    print(len(args))
    print(args)
    print(tuple(args))

misc(x)
misc(x, 1, 3)
