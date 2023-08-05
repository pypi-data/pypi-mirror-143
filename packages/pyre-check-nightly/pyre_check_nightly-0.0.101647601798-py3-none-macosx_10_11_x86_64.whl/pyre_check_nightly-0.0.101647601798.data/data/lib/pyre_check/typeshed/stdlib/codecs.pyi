import sys
import types
from _typeshed import Self
from abc import abstractmethod
from typing import IO, Any, BinaryIO, Callable, Generator, Iterable, Iterator, Protocol, TextIO, Tuple, Type, TypeVar, overload
from typing_extensions import Literal

# TODO: this only satisfies the most common interface, where
# bytes is the raw form and str is the cooked form.
# In the long run, both should become template parameters maybe?
# There *are* bytes->bytes and str->str encodings in the standard library.
# They are much more common in Python 2 than in Python 3.

class _Encoder(Protocol):
    def __call__(self, input: str, errors: str = ...) -> Tuple[bytes, int]: ...  # signature of Codec().encode

class _Decoder(Protocol):
    def __call__(self, input: bytes, errors: str = ...) -> Tuple[str, int]: ...  # signature of Codec().decode

class _StreamReader(Protocol):
    def __call__(self, stream: IO[bytes], errors: str = ...) -> StreamReader: ...

class _StreamWriter(Protocol):
    def __call__(self, stream: IO[bytes], errors: str = ...) -> StreamWriter: ...

class _IncrementalEncoder(Protocol):
    def __call__(self, errors: str = ...) -> IncrementalEncoder: ...

class _IncrementalDecoder(Protocol):
    def __call__(self, errors: str = ...) -> IncrementalDecoder: ...

# The type ignore on `encode` and `decode` is to avoid issues with overlapping overloads, for more details, see #300
# mypy and pytype disagree about where the type ignore can and cannot go, so alias the long type
_BytesToBytesEncodingT = Literal[
    "base64",
    "base_64",
    "base64_codec",
    "bz2",
    "bz2_codec",
    "hex",
    "hex_codec",
    "quopri",
    "quotedprintable",
    "quoted_printable",
    "quopri_codec",
    "uu",
    "uu_codec",
    "zip",
    "zlib",
    "zlib_codec",
]

@overload
def encode(obj: bytes, encoding: _BytesToBytesEncodingT, errors: str = ...) -> bytes: ...
@overload
def encode(obj: str, encoding: Literal["rot13", "rot_13"] = ..., errors: str = ...) -> str: ...  # type: ignore
@overload
def encode(obj: str, encoding: str = ..., errors: str = ...) -> bytes: ...
@overload
def decode(obj: bytes, encoding: _BytesToBytesEncodingT, errors: str = ...) -> bytes: ...  # type: ignore
@overload
def decode(obj: str, encoding: Literal["rot13", "rot_13"] = ..., errors: str = ...) -> str: ...
@overload
def decode(obj: bytes, encoding: str = ..., errors: str = ...) -> str: ...
def lookup(__encoding: str) -> CodecInfo: ...
def utf_16_be_decode(__data: bytes, __errors: str | None = ..., __final: bool = ...) -> Tuple[str, int]: ...  # undocumented
def utf_16_be_encode(__str: str, __errors: str | None = ...) -> Tuple[bytes, int]: ...  # undocumented

class CodecInfo(Tuple[_Encoder, _Decoder, _StreamReader, _StreamWriter]):
    @property
    def encode(self) -> _Encoder: ...
    @property
    def decode(self) -> _Decoder: ...
    @property
    def streamreader(self) -> _StreamReader: ...
    @property
    def streamwriter(self) -> _StreamWriter: ...
    @property
    def incrementalencoder(self) -> _IncrementalEncoder: ...
    @property
    def incrementaldecoder(self) -> _IncrementalDecoder: ...
    name: str
    def __new__(
        cls,
        encode: _Encoder,
        decode: _Decoder,
        streamreader: _StreamReader | None = ...,
        streamwriter: _StreamWriter | None = ...,
        incrementalencoder: _IncrementalEncoder | None = ...,
        incrementaldecoder: _IncrementalDecoder | None = ...,
        name: str | None = ...,
        *,
        _is_text_encoding: bool | None = ...,
    ) -> CodecInfo: ...

def getencoder(encoding: str) -> _Encoder: ...
def getdecoder(encoding: str) -> _Decoder: ...
def getincrementalencoder(encoding: str) -> _IncrementalEncoder: ...
def getincrementaldecoder(encoding: str) -> _IncrementalDecoder: ...
def getreader(encoding: str) -> _StreamReader: ...
def getwriter(encoding: str) -> _StreamWriter: ...
def register(__search_function: Callable[[str], CodecInfo | None]) -> None: ...
def open(
    filename: str, mode: str = ..., encoding: str | None = ..., errors: str = ..., buffering: int = ...
) -> StreamReaderWriter: ...
def EncodedFile(file: IO[bytes], data_encoding: str, file_encoding: str | None = ..., errors: str = ...) -> StreamRecoder: ...
def iterencode(iterator: Iterable[str], encoding: str, errors: str = ...) -> Generator[bytes, None, None]: ...
def iterdecode(iterator: Iterable[bytes], encoding: str, errors: str = ...) -> Generator[str, None, None]: ...

if sys.version_info >= (3, 10):
    def unregister(__search_function: Callable[[str], CodecInfo | None]) -> None: ...

BOM: bytes
BOM_BE: bytes
BOM_LE: bytes
BOM_UTF8: bytes
BOM_UTF16: bytes
BOM_UTF16_BE: bytes
BOM_UTF16_LE: bytes
BOM_UTF32: bytes
BOM_UTF32_BE: bytes
BOM_UTF32_LE: bytes

# It is expected that different actions be taken depending on which of the
# three subclasses of `UnicodeError` is actually ...ed. However, the Union
# is still needed for at least one of the cases.
def register_error(__errors: str, __handler: Callable[[UnicodeError], Tuple[str | bytes, int]]) -> None: ...
def lookup_error(__name: str) -> Callable[[UnicodeError], Tuple[str | bytes, int]]: ...
def strict_errors(exception: UnicodeError) -> Tuple[str | bytes, int]: ...
def replace_errors(exception: UnicodeError) -> Tuple[str | bytes, int]: ...
def ignore_errors(exception: UnicodeError) -> Tuple[str | bytes, int]: ...
def xmlcharrefreplace_errors(exception: UnicodeError) -> Tuple[str | bytes, int]: ...
def backslashreplace_errors(exception: UnicodeError) -> Tuple[str | bytes, int]: ...

class Codec:
    # These are sort of @abstractmethod but sort of not.
    # The StreamReader and StreamWriter subclasses only implement one.
    def encode(self, input: str, errors: str = ...) -> Tuple[bytes, int]: ...
    def decode(self, input: bytes, errors: str = ...) -> Tuple[str, int]: ...

class IncrementalEncoder:
    errors: str
    def __init__(self, errors: str = ...) -> None: ...
    @abstractmethod
    def encode(self, input: str, final: bool = ...) -> bytes: ...
    def reset(self) -> None: ...
    # documentation says int but str is needed for the subclass.
    def getstate(self) -> int | str: ...
    def setstate(self, state: int | str) -> None: ...

class IncrementalDecoder:
    errors: str
    def __init__(self, errors: str = ...) -> None: ...
    @abstractmethod
    def decode(self, input: bytes, final: bool = ...) -> str: ...
    def reset(self) -> None: ...
    def getstate(self) -> Tuple[bytes, int]: ...
    def setstate(self, state: Tuple[bytes, int]) -> None: ...

# These are not documented but used in encodings/*.py implementations.
class BufferedIncrementalEncoder(IncrementalEncoder):
    buffer: str
    def __init__(self, errors: str = ...) -> None: ...
    @abstractmethod
    def _buffer_encode(self, input: str, errors: str, final: bool) -> bytes: ...
    def encode(self, input: str, final: bool = ...) -> bytes: ...

class BufferedIncrementalDecoder(IncrementalDecoder):
    buffer: bytes
    def __init__(self, errors: str = ...) -> None: ...
    @abstractmethod
    def _buffer_decode(self, input: bytes, errors: str, final: bool) -> Tuple[str, int]: ...
    def decode(self, input: bytes, final: bool = ...) -> str: ...

# TODO: it is not possible to specify the requirement that all other
# attributes and methods are passed-through from the stream.
class StreamWriter(Codec):
    errors: str
    def __init__(self, stream: IO[bytes], errors: str = ...) -> None: ...
    def write(self, object: str) -> None: ...
    def writelines(self, list: Iterable[str]) -> None: ...
    def reset(self) -> None: ...
    def __enter__(self: Self) -> Self: ...
    def __exit__(self, typ: Type[BaseException] | None, exc: BaseException | None, tb: types.TracebackType | None) -> None: ...
    def __getattr__(self, name: str, getattr: Callable[[str], Any] = ...) -> Any: ...

class StreamReader(Codec):
    errors: str
    def __init__(self, stream: IO[bytes], errors: str = ...) -> None: ...
    def read(self, size: int = ..., chars: int = ..., firstline: bool = ...) -> str: ...
    def readline(self, size: int | None = ..., keepends: bool = ...) -> str: ...
    def readlines(self, sizehint: int | None = ..., keepends: bool = ...) -> list[str]: ...
    def reset(self) -> None: ...
    def __enter__(self: Self) -> Self: ...
    def __exit__(self, typ: Type[BaseException] | None, exc: BaseException | None, tb: types.TracebackType | None) -> None: ...
    def __iter__(self) -> Iterator[str]: ...
    def __getattr__(self, name: str, getattr: Callable[[str], Any] = ...) -> Any: ...

_T = TypeVar("_T", bound=StreamReaderWriter)

# Doesn't actually inherit from TextIO, but wraps a BinaryIO to provide text reading and writing
# and delegates attributes to the underlying binary stream with __getattr__.
class StreamReaderWriter(TextIO):
    def __init__(self, stream: IO[bytes], Reader: _StreamReader, Writer: _StreamWriter, errors: str = ...) -> None: ...
    def read(self, size: int = ...) -> str: ...
    def readline(self, size: int | None = ...) -> str: ...
    def readlines(self, sizehint: int | None = ...) -> list[str]: ...
    def __next__(self) -> str: ...
    def __iter__(self: _T) -> _T: ...
    # This actually returns None, but that's incompatible with the supertype
    def write(self, data: str) -> int: ...
    def writelines(self, list: Iterable[str]) -> None: ...
    def reset(self) -> None: ...
    # Same as write()
    def seek(self, offset: int, whence: int = ...) -> int: ...
    def __enter__(self: Self) -> Self: ...
    def __exit__(self, typ: Type[BaseException] | None, exc: BaseException | None, tb: types.TracebackType | None) -> None: ...
    def __getattr__(self, name: str) -> Any: ...
    # These methods don't actually exist directly, but they are needed to satisfy the TextIO
    # interface. At runtime, they are delegated through __getattr__.
    def close(self) -> None: ...
    def fileno(self) -> int: ...
    def flush(self) -> None: ...
    def isatty(self) -> bool: ...
    def readable(self) -> bool: ...
    def truncate(self, size: int | None = ...) -> int: ...
    def seekable(self) -> bool: ...
    def tell(self) -> int: ...
    def writable(self) -> bool: ...

_SRT = TypeVar("_SRT", bound=StreamRecoder)

class StreamRecoder(BinaryIO):
    def __init__(
        self,
        stream: IO[bytes],
        encode: _Encoder,
        decode: _Decoder,
        Reader: _StreamReader,
        Writer: _StreamWriter,
        errors: str = ...,
    ) -> None: ...
    def read(self, size: int = ...) -> bytes: ...
    def readline(self, size: int | None = ...) -> bytes: ...
    def readlines(self, sizehint: int | None = ...) -> list[bytes]: ...
    def __next__(self) -> bytes: ...
    def __iter__(self: _SRT) -> _SRT: ...
    def write(self, data: bytes) -> int: ...
    def writelines(self, list: Iterable[bytes]) -> int: ...  # type: ignore  # it's supposed to return None
    def reset(self) -> None: ...
    def __getattr__(self, name: str) -> Any: ...
    def __enter__(self: Self) -> Self: ...
    def __exit__(self, type: Type[BaseException] | None, value: BaseException | None, tb: types.TracebackType | None) -> None: ...
    # These methods don't actually exist directly, but they are needed to satisfy the BinaryIO
    # interface. At runtime, they are delegated through __getattr__.
    def seek(self, offset: int, whence: int = ...) -> int: ...
    def close(self) -> None: ...
    def fileno(self) -> int: ...
    def flush(self) -> None: ...
    def isatty(self) -> bool: ...
    def readable(self) -> bool: ...
    def truncate(self, size: int | None = ...) -> int: ...
    def seekable(self) -> bool: ...
    def tell(self) -> int: ...
    def writable(self) -> bool: ...
