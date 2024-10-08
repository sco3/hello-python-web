import typing as T
from _typeshed import Incomplete

class HandlerNotFound(Exception):
    event: Incomplete
    handler: Incomplete
    def __init__(self, event: str, handler: T.Callable) -> None: ...

class EventNotFound(Exception):
    event: Incomplete
    def __init__(self, event: str) -> None: ...

class Observable:
    def __init__(self) -> None: ...
    def get_all_handlers(self) -> dict[str, list[T.Callable]]: ...
    def get_handlers(self, event: str) -> list[T.Callable]: ...
    def is_registered(self, event: str, handler: T.Callable) -> bool: ...
    def on(self, event: str, *handlers: T.Callable) -> T.Callable: ...
    def off(self, event: T.Union[str,None] = None, *handlers: T.Callable) -> None: ...
    def once(self, event: str, *handlers: T.Callable) -> T.Callable: ...
    def trigger(self, event: str, *args: T.Any, **kw: T.Any) -> bool: ...
