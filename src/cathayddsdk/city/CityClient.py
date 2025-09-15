import httpx

from .. import limits, timeout
from ..BaseClient import DIDIBaseClient
from ..Consts.HttpConsts import HeaderNames, MimeTypes


class DIDICityClient(DIDIBaseClient):
    async def getRiverCity(self):
        async with httpx.AsyncClient(limits=limits, timeout=timeout) as client:
            payload = await self.getCommonPayload(True,True,True,False)
            payload['sign'] = self._generate_sign(payload)
            headers = {
                HeaderNames.CONTENT_TYPE: MimeTypes.APPLICATION_X_WWW_FORM_URLENCODED
            }
            res = await client.get(f'{self.BASE_URL}/river/City/get', params=payload, headers=headers)
            return res.json()
