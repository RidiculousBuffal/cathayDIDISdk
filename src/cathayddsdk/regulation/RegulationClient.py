from typing import List, Optional

import httpx
from pydantic import BaseModel

from .. import timeout, limits
from ..BaseClient import DIDIBaseClient
from ..Consts.HttpConsts import HeaderNames, MimeTypes
from ..Model.Response import DIDIResponse


class RegulationListModel(BaseModel):
    regulation_id: str
    regulation_name: str
    regulation_employee_name: str
    regulation_employee_description: str
    regulation_status: str
    is_approve: int
    scene_type: str
    is_use_quota: int
    source: int
    city_type: int
    approval_type: int


class RegulationListResponse(DIDIResponse):
    data: Optional[list[RegulationListModel]]=[]


class DIDIRegulationClient(DIDIBaseClient):
    async def getRiverRegulationList(self):
        async with httpx.AsyncClient(timeout=timeout, limits=limits) as client:
            payload = await self.getCommonPayload()
            payload['sign'] = self._generate_sign(payload)
            headers = {
                HeaderNames.CONTENT_TYPE: MimeTypes.APPLICATION_X_WWW_FORM_URLENCODED
            }
            res = await client.get(f'{self.BASE_URL}/river/Regulation/get', params=payload, headers=headers)
            return RegulationListResponse.model_validate(res.json())
