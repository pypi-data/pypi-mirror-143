from typing import Any

from werkzeug.exceptions import HTTPException
from werkzeug.routing import Rule
from werkzeug.wrappers import Request as RequestBase, Response as ResponseBase

class JSONMixin:
    @property
    def is_json(self) -> bool: ...
    @property
    def json(self): ...
    def get_json(self, force: bool = ..., silent: bool = ..., cache: bool = ...): ...
    def on_json_loading_failed(self, e: Any) -> None: ...

class Request(RequestBase, JSONMixin):
    url_rule: Rule | None = ...
    view_args: dict[str, Any] = ...
    routing_exception: HTTPException | None = ...
    # Request is making the max_content_length readonly, where it was not the
    # case in its supertype.
    # We would require something like https://github.com/python/typing/issues/241
    @property
    def max_content_length(self) -> int | None: ...  # type: ignore
    @property
    def endpoint(self) -> str | None: ...
    @property
    def blueprint(self) -> str | None: ...

class Response(ResponseBase, JSONMixin):
    default_mimetype: str | None = ...
    @property
    def max_cookie_size(self) -> int: ...
