import asyncio
import json

import dotenv

from src.cathayddsdk.approval.ApprovalClient import DIDIApprovalClient

dotenv.load_dotenv()

if __name__ == '__main__':
    with open('./test_approval.json', 'r', encoding='utf-8') as f:
        data = json.load(f)


    async def main():
        cli = DIDIApprovalClient()
        res = await cli.createApprovalTicket(data)
        print(json.dumps(res, indent=2, ensure_ascii=False))


    asyncio.run(main())
