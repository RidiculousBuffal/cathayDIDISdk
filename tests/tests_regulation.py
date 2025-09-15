import asyncio
import json

import dotenv

from src.cathayddsdk.regulation.RegulationClient import DIDIRegulationClient

dotenv.load_dotenv()

if __name__ == '__main__':
    async def main():
        cli = DIDIRegulationClient()
        res = await cli.getRiverRegulationList()
        print(res.model_dump_json())


    asyncio.run(main())

    # {
    #     "regulation_id": "1125977651872720",
    #     "regulation_name": "出差申请用车",
    #     "regulation_employee_name": "申请出差",
    #     "regulation_employee_description": "",
    #     "regulation_status": "1",
    #     "is_approve": 2,
    #     "scene_type": "2",
    #     "is_use_quota": 0,
    #     "source": 1,
    #     "city_type": 3,
    #     "approval_type": 1
    # },