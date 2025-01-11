#  Copyright (c) 2025. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

from typing import overload, Union
from typing_extensions import Literal

var = 2
if var == 1:
    # python3中增加了Function Annotation(函数注解,能够声明类型)的功能,可以使用类型检查工具如mypy达到类型静态检查的效果
    def foo(name: str) -> str:
        return "csdn id:" + name


    print(foo("fengbingchun"))
elif var == 2:
    @overload
    def myfunc(arg: Literal[True]) -> str:
        ...


    @overload
    def myfunc(arg: Literal[False]) -> int:
        ...


    @overload
    def myfunc(arg: bool) -> Union[str, int]:  # Union[str, int] == str | int
        ...


    def myfunc(arg: bool) -> Union[int, str]:
        if arg:
            return "something"
        else:
            return 0


    print(myfunc(True))
    print(myfunc(False))

    variable = True
    print(myfunc(variable))

print("test finish")
