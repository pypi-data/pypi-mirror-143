from typing import Any, List

class Tag:
    key: Any
    value: Any
    def __init__(self, key: Any | None = ..., value: Any | None = ...) -> None: ...
    def startElement(self, name, attrs, connection): ...
    def endElement(self, name, value, connection): ...
    def to_xml(self): ...
    def __eq__(self, other): ...

class TagSet(List[Tag]):
    def startElement(self, name, attrs, connection): ...
    def endElement(self, name, value, connection): ...
    def add_tag(self, key, value): ...
    def to_xml(self): ...

class Tags(List[TagSet]):
    def startElement(self, name, attrs, connection): ...
    def endElement(self, name, value, connection): ...
    def to_xml(self): ...
    def add_tag_set(self, tag_set): ...
