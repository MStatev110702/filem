from typing import TypedDict, Any, NotRequired

class QueryResponse(TypedDict):
    success: bool
    data: Any
    error: NotRequired[str]