import asyncio
import aiohttp
import aiofiles
from bs4 import BeautifulSoup




async def Download(path, url) -> None:
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as resp:
            if resp.ok:
                async with aiofiles.open(file=path, mode="wb") as file:
                    async with chunk in resp.content.iter_chunked(n=8192):
                        await file.write(chunk)
            else:
                print(f"Server gave back error {resp.status}")


async def Rip(path) -> None:
    async with aiofiles.open(file=path, mode="r") as file:
        soup = BeautifulSoup(file, "html.parser")



if __name__ == "__main__":
    base_url:str = "https://gitbook.io/"
    
    path = "../stuff.html"
    url = "https://groupeinfo.gitbook.io/computer-science-data-base"
    
    asyncio.run(main=Download(path=path, url=url))
    
    
    