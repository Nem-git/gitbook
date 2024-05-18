import os
import asyncio
import aiohttp
import aiofiles
from bs4 import BeautifulSoup




async def download(path : str, url : str) -> str:
    name = f"{url.split("/")[-1]}.html"
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as resp:
            if resp.ok:
                async with aiofiles.open(file=f"{path}/{name}", mode="wb") as file:
                    async for chunk in resp.content.iter_chunked(n=8192):
                        await file.write(chunk)
                    return name

            else:
                print(f"Server gave back error {resp.status}")


async def rip(dir_path : str, url, url_root : str, url_start : str) -> None:

    os.makedirs(f"{dir_path}{url_root}", exist_ok=True)
    dir_path = f"{dir_path}{url_root}"
    file_name = await download(path=dir_path, url=url)

    async with aiofiles.open(file=f"{dir_path}/{file_name}", mode="rt", newline="\n") as file:
        soup = BeautifulSoup(await file.read(), "html.parser")
        for link in soup.find_all("a"):
            async with asyncio.TaskGroup() as tg:
                tg.create_task(coro=task_management(url_root, dir_path, url_start, link))


async def task_management(url_root : str, dir_path : str, url_start : str, link : str):
    l = link.get("href")
    if url_root in l:
        await download(dir_path, f"{url_start}{l}")
        print(l)


if __name__ == "__main__":
    
    base_url:str = "https://gitbook.io"
    url_start = "https://groupeinfo.gitbook.io"
    dir_path = ".."
    url_root = "/computer-science-data-base"
    url = "".join((url_start, url_root))
    
    
    asyncio.run(main=rip(dir_path=dir_path, url=url, url_root=url_root, url_start=url_start))
    
    
    