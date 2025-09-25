import asyncio

from src.cathayddsdk.approval.ApprovalClient import DIDIApprovalClient
import dotenv
dotenv.load_dotenv()
if __name__ == '__main__':
    ticket = [
int("1125978729935578	".replace(' ','')),
int("1125978666970381	".replace(' ','')),
int("1125978662675477	".replace(' ','')),
int("1125978656108265	".replace(' ','')),
int("1125978550462026	".replace(' ','')),
int("1125978501597646	".replace(' ','')),
int("1125978476403757	".replace(' ','')),
int("1125978444452164	".replace(' ','')),
int("1125978444674215	".replace(' ','')),
int("1125978444601151	".replace(' ','')),
int("1125978444689407	".replace(' ','')),
int("1125978377149950	".replace(' ','')),
int("1125978376914582	".replace(' ','')),
int("1125978376575313	".replace(' ','')),
int("1125978376704626	".replace(' ','')),
int("1125978376613986	".replace(' ','')),
int("1125978369424890	".replace(' ','')),
int("1125978369383278	".replace(' ','')),
int("1125978369152008	".replace(' ','')),
int("1125978369186868	".replace(' ','')),
int("1125978369112797	".replace(' ','')),
int("1125978369166227	".replace(' ','')),
int("1125978369091216	".replace(' ','')),
int("1125978369097404	".replace(' ','')),
int("1125978368962209	".replace(' ','')),
int("1125978369065427	".replace(' ','')),
int("1125978369103790	".replace(' ','')),
int("1125978368892713	".replace(' ','')),
int("1125978368953236	".replace(' ','')),
int("1125978369032726	".replace(' ','')),
int("1125978368914100	".replace(' ','')),
int("1125978368877556	".replace(' ','')),
int("1125978368825940	".replace(' ','')),
int("1125978368864383	".replace(' ','')),
int("1125978368861086	".replace(' ','')),
int("1125978368733265	".replace(' ','')),
int("1125978368891698	".replace(' ','')),
int("1125978368731700	".replace(' ','')),
int("1125978368813634	".replace(' ','')),
int("1125978368812002	".replace(' ','')),
int("1125978368601581	".replace(' ','')),
int("1125978368717976	".replace(' ','')),
int("1125978368698332	".replace(' ','')),
int("1125978368678998	".replace(' ','')),
int("1125978368727054	".replace(' ','')),
int("1125978368029312	".replace(' ','')),
int("1125978368094148	".replace(' ','')),
int("1125978368057796	".replace(' ','')),
int("1125978368044799	".replace(' ','')),
int("1125978368012796	".replace(' ','')),
int("1125978367832897	".replace(' ','')),
int("1125978368029450	".replace(' ','')),
int("1125978367913019	".replace(' ','')),
int("1125978367854175	".replace(' ','')),
int("1125978367931426	".replace(' ','')),
int("1125978367797419	".replace(' ','')),
int("1125978367856778	".replace(' ','')),
int("1125978367845254	".replace(' ','')),
int("1125978361736710	".replace(' ','')),
]
    cli = DIDIApprovalClient()
    async def main():
        for t in ticket:
            res = await cli.cancelApprovalTicket(t)
            print(res)
    asyncio.run(main())
