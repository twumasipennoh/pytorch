import dataclasses
import inspect
import sys
from typing import Callable, Tuple


@dataclasses.dataclass
class Kernel:
    """Models a (function, source location)"""

    func: Callable
    source: str

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


class RegistrationHandle:
    """Does something when someone calls .destroy() on it"""

    def __init__(self, on_destroy: Callable):
        self._on_destroy = on_destroy

    def destroy(self) -> None:
        self._on_destroy()


def get_source(stacklevel: int) -> str:
    """Get a string that represents the caller.

    Example: "/path/to/foo.py:42"

    Use stacklevel=1 to get the caller's source
    Use stacklevel=2 to get the caller's caller's source
    etc.
    """
    frame = inspect.getframeinfo(sys._getframe(stacklevel))
    source = f"{frame.filename}:{frame.lineno}"
    return source


def parse_namespace(name: str) -> Tuple[str, str]:
    splits = name.split("::")
    if len(splits) != 2:
        raise ValueError(
            f"Expected `name` to be of the form "
            f'"namespace::name", but got {name}. '
            f"Operator names in PyTorch consist of a name "
            f"and a namespace, e.g. aten::sin"
        )
    return splits[0], splits[1]
