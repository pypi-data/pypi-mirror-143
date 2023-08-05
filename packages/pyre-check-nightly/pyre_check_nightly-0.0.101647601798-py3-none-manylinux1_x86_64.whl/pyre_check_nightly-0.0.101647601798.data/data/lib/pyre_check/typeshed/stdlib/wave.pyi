import sys
from _typeshed import Self
from typing import IO, Any, BinaryIO, NamedTuple, NoReturn, Union

_File = Union[str, IO[bytes]]

class Error(Exception): ...

WAVE_FORMAT_PCM: int

class _wave_params(NamedTuple):
    nchannels: int
    sampwidth: int
    framerate: int
    nframes: int
    comptype: str
    compname: str

class Wave_read:
    def __init__(self, f: _File) -> None: ...
    def __enter__(self: Self) -> Self: ...
    def __exit__(self, *args: Any) -> None: ...
    def getfp(self) -> BinaryIO | None: ...
    def rewind(self) -> None: ...
    def close(self) -> None: ...
    def tell(self) -> int: ...
    def getnchannels(self) -> int: ...
    def getnframes(self) -> int: ...
    def getsampwidth(self) -> int: ...
    def getframerate(self) -> int: ...
    def getcomptype(self) -> str: ...
    def getcompname(self) -> str: ...
    def getparams(self) -> _wave_params: ...
    def getmarkers(self) -> None: ...
    def getmark(self, id: Any) -> NoReturn: ...
    def setpos(self, pos: int) -> None: ...
    def readframes(self, nframes: int) -> bytes: ...

class Wave_write:
    def __init__(self, f: _File) -> None: ...
    def __enter__(self: Self) -> Self: ...
    def __exit__(self, *args: Any) -> None: ...
    def setnchannels(self, nchannels: int) -> None: ...
    def getnchannels(self) -> int: ...
    def setsampwidth(self, sampwidth: int) -> None: ...
    def getsampwidth(self) -> int: ...
    def setframerate(self, framerate: float) -> None: ...
    def getframerate(self) -> int: ...
    def setnframes(self, nframes: int) -> None: ...
    def getnframes(self) -> int: ...
    def setcomptype(self, comptype: str, compname: str) -> None: ...
    def getcomptype(self) -> str: ...
    def getcompname(self) -> str: ...
    def setparams(self, params: _wave_params) -> None: ...
    def getparams(self) -> _wave_params: ...
    def setmark(self, id: Any, pos: Any, name: Any) -> NoReturn: ...
    def getmark(self, id: Any) -> NoReturn: ...
    def getmarkers(self) -> None: ...
    def tell(self) -> int: ...
    # should be any bytes-like object after 3.4, but we don't have a type for that
    def writeframesraw(self, data: bytes) -> None: ...
    def writeframes(self, data: bytes) -> None: ...
    def close(self) -> None: ...

# Returns a Wave_read if mode is rb and Wave_write if mode is wb
def open(f: _File, mode: str | None = ...) -> Any: ...

if sys.version_info < (3, 9):
    openfp = open
