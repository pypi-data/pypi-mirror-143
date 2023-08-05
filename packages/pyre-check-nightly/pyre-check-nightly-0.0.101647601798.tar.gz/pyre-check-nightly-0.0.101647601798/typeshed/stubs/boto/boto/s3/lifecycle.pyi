from typing import Any, List

class Rule:
    id: Any
    prefix: Any
    status: Any
    expiration: Any
    transition: Any
    def __init__(
        self,
        id: Any | None = ...,
        prefix: Any | None = ...,
        status: Any | None = ...,
        expiration: Any | None = ...,
        transition: Any | None = ...,
    ) -> None: ...
    def startElement(self, name, attrs, connection): ...
    def endElement(self, name, value, connection): ...
    def to_xml(self): ...

class Expiration:
    days: Any
    date: Any
    def __init__(self, days: Any | None = ..., date: Any | None = ...) -> None: ...
    def startElement(self, name, attrs, connection): ...
    def endElement(self, name, value, connection): ...
    def to_xml(self): ...

class Transition:
    days: Any
    date: Any
    storage_class: Any
    def __init__(self, days: Any | None = ..., date: Any | None = ..., storage_class: Any | None = ...) -> None: ...
    def to_xml(self): ...

class Transitions(List[Transition]):
    transition_properties: int
    current_transition_property: int
    temp_days: Any
    temp_date: Any
    temp_storage_class: Any
    def __init__(self) -> None: ...
    def startElement(self, name, attrs, connection): ...
    def endElement(self, name, value, connection): ...
    def to_xml(self): ...
    def add_transition(self, days: Any | None = ..., date: Any | None = ..., storage_class: Any | None = ...): ...
    @property
    def days(self): ...
    @property
    def date(self): ...
    @property
    def storage_class(self): ...

class Lifecycle(List[Rule]):
    def startElement(self, name, attrs, connection): ...
    def endElement(self, name, value, connection): ...
    def to_xml(self): ...
    def add_rule(
        self,
        id: Any | None = ...,
        prefix: str = ...,
        status: str = ...,
        expiration: Any | None = ...,
        transition: Any | None = ...,
    ): ...
