from typing import Any

from pydantic import BaseModel


class DIDIResponse(BaseModel):
    errno: int
    errmsg: str
    data: Any
    request_id: str
