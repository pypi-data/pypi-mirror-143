from email.message import Message
from typing import Iterator

def body_line_iterator(msg: Message, decode: bool = ...) -> Iterator[str]: ...
def typed_subpart_iterator(msg: Message, maintype: str = ..., subtype: str | None = ...) -> Iterator[str]: ...
