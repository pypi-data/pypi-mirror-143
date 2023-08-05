from typing import Any, ContextManager, TextIO

from .ansitowin32 import StreamWrapper

orig_stdout: TextIO | None
orig_stderr: TextIO | None
wrapped_stdout: TextIO | StreamWrapper
wrapped_stderr: TextIO | StreamWrapper
atexit_done: bool

def reset_all() -> None: ...
def init(autoreset: bool = ..., convert: bool | None = ..., strip: bool | None = ..., wrap: bool = ...) -> None: ...
def deinit() -> None: ...
def colorama_text(*args: Any, **kwargs: Any) -> ContextManager[None]: ...
def reinit() -> None: ...
def wrap_stream(
    stream: TextIO, convert: bool | None, strip: bool | None, autoreset: bool, wrap: bool
) -> TextIO | StreamWrapper: ...
