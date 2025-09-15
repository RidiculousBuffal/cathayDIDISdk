import httpx

from .. import limits, timeout
from ..BaseClient import DIDIBaseClient
from ..Consts.HttpConsts import HeaderNames, MimeTypes


class DIDIBudgetCenterClient(DIDIBaseClient):
    async def getBudgetCenterList(self, offset=0, length=100):
        async with httpx.AsyncClient(limits=limits, timeout=timeout) as client:
            payload = await self.getCommonPayload()
            payload['offset'] = offset
            payload['length'] = length
            payload['sign'] = self._generate_sign(payload)
            headers = {
                HeaderNames.CONTENT_TYPE: MimeTypes.APPLICATION_X_WWW_FORM_URLENCODED
            }
            res = await client.get(f'{self.BASE_URL}/river/BudgetCenter/get', params=payload)
            return res.json()

