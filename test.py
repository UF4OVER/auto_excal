from typing import overload, Union
from typing_extensions import Literal


@overload
def myfunc(arg: Literal[True]) -> type:
    pass


@overload
def myfunc(arg: Literal[False]) -> type:
    pass


@overload
def myfunc(arg: bool) -> Union[type, type]:
    pass


def myfunc(arg: bool) -> Union[type, type]:
    if arg:
        # todo
        pass
    else:
        # todo
        pass
