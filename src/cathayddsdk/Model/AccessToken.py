from typing import Optional

from pydantic import BaseModel


class AccessToken(BaseModel):
    access_token: str
    expires_in: int
    token_type: Optional[str]='Bearer'
    scope: Optional[str]=None
    from_cache:Optional[bool]=False
