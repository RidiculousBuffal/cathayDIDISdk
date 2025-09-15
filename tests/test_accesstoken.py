import asyncio
import dotenv
dotenv.load_dotenv()
from src.cathayddsdk.BaseClient import DIDIBaseClient

if __name__ == '__main__':
    async def main():
        cli = DIDIBaseClient()
        res = await cli.get_access_token()
        print(res)
    asyncio.run(main())