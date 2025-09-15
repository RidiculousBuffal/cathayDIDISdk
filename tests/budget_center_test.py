import asyncio
import json

import dotenv

from src.cathayddsdk.budgetCenter.BudgetCenterClient import DIDIBudgetCenterClient
from src.cathayddsdk.city.CityClient import DIDICityClient

dotenv.load_dotenv()

if __name__ == '__main__':
    async def main():
        cli = DIDIBudgetCenterClient()
        res = await cli.getBudgetCenterList()
        print(json.dumps(res, indent=2,ensure_ascii=False))


    asyncio.run(main())
