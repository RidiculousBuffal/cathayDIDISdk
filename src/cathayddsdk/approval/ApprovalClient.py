import json

import httpx

from .. import limits, timeout
from ..BaseClient import DIDIBaseClient
from ..Consts.HttpConsts import HeaderNames, MimeTypes


class DIDIApprovalClient(DIDIBaseClient):
    # ref https://opendocs.xiaojukeji.com/version2024/10999#%E6%8E%A5%E5%8F%A3%E8%AF%B4%E6%98%8E
    """成功:
    {
      "errno": 0,
      "errmsg": "SUCCESS",
      "data": {
        "approval_id": "1125978361736710"
      },
      "request_id": "+xvHWIzBGl27pvzYkzfSni6QMOY1Anw6ECKDeR/TwiXSKGC2o64BnJxi01pLsA2/"
    }
    失败:
    {
      "errno": 50506,
      "errmsg": "外部审批单号已被使用(对应的滴滴审批单ID为1125978361736710)，请更换外部审批单号或调用审批单修改API",
      "data": null,
      "request_id": "+xvHWIzBGl2SCesEMlL9Cz6Y75nF0SpARZzIeqs2VbaXZBVkoRBki23IrI+MEaJf"
    }

    """

    async def createApprovalTicket(self, approval_json):
        async with httpx.AsyncClient(limits=limits, timeout=timeout) as client:
            payload = await self.getCommonPayload()
            payload.update(approval_json)
            payload['sign'] = self._generate_sign(payload)
            headers = {
                HeaderNames.CONTENT_TYPE: MimeTypes.APPLICATION_JSON
            }
            res = await client.post(f'{self.BASE_URL}/river/Approval/create', json=payload, headers=headers)
            return res.json()
