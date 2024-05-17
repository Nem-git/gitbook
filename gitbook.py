import asyncio
import aiohttp
import aiofiles
from bs4 import BeautifulSoup




async def Download(self, session, path, url) -> None:
    
    async with session:
        async with session.get(url=url) as resp:
            if resp.ok:
                async with aiofiles.open(file=path, mode="wb") as file:
                    async with chunk in resp.content.iter_chunked(n=8192):
                        await file.write(chunk)
            else:
                print(f"Server gave back error {resp.status}")
    

async def Rip(self, path):
    async with aiofiles.open(file=path, mode="r") as file:
        soup = BeautifulSoup(file, "html.parser")
        




if __name__ == "__main__":
    base_url:str = "https://groupeinfo.gitbook.io/computer-science-data-base"
    
    session = aiohttp.ClientSession(base_url=base_url)
    path = "../"
    url = base_url
    
    asyncio.run(main=Download(session=session, path, url))
    
    
    