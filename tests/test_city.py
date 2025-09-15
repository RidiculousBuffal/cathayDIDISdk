import asyncio
import json

import dotenv

from src.cathayddsdk.city.CityClient import DIDICityClient

dotenv.load_dotenv()

if __name__ == '__main__':
    async def main():
        cli = DIDICityClient()
        res = await cli.getRiverCity()
        print(json.dumps(res, indent=2,ensure_ascii=False))


    asyncio.run(main())
