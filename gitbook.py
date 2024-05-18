import os
import asyncio
import aiohttp
import aiofiles
from bs4 import BeautifulSoup


class Link:

    async def download(self, path : str, url : str) -> str:
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


    async def rip(self, dir_path : str, url, url_root : str, url_start : str) -> None:

        os.makedirs(f"{dir_path}{url_root}", exist_ok=True)
        dir_path = f"{dir_path}{url_root}"
        file_name = await self.download(path=dir_path, url=url)

        async with aiofiles.open(file=f"{dir_path}/{file_name}", mode="rt", newline="\n") as file:
            soup = BeautifulSoup(await file.read(), "html.parser")
            for link in soup.find_all("a"):
                async with asyncio.TaskGroup() as tg:
                    tg.create_task(coro=self.management(url_root, dir_path, url_start, link))


    async def management(self, url_root : str, dir_path : str, url_start : str, link : str):
        l = link.get("href")
        if url_root in l:
            await self.download(dir_path, f"{url_start}{l}")
            print(l)


class Time:
    
    async def download(self, path, url) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.ok:
                    async with aiofiles.open(file=path, mode="wb") as file:
                        async for chunk in resp.content.iter_chunked(n=8192):
                            await file.write(chunk)

                else:
                    print(f"Server gave back error {resp.status}")


    def verify(self, time, path):
        
        if not os.path.exists(path):
            open(file=path, mode="wt").close()

        with open(file=path, mode="rt", newline="\n") as file:
            old_time = file.read()
            if old_time == time:
                return False

            else:
                with open(file=path, mode="wt", newline="\n") as file:
                    file.write(time)
                    return True


    async def rip(self, path, url):
        
        file_path = f"{path}/temp.cache.html"
        
        await self.download(file_path, url)
        
        async with aiofiles.open(file=file_path, mode="rt", newline="\n") as file:
            soup = BeautifulSoup(await file.read(), "html.parser")
            os.remove(file_path)
            
            full_time = soup.find("time")
            
            time = full_time.get("datetime")
            
            time_path = f"{path}/.time.temp"
            
            return self.verify(time, time_path)




if __name__ == "__main__":
    
    base_url = "https://gitbook.io"
    url_start = "https://groupeinfo.gitbook.io"
    dir_path = ".."
    url_root = "/computer-science-data-base"
    url = "".join((url_start, url_root))
    
    time = Time()
    
    #asyncio.run(main=time.rip(dir_path, url))
    
    link = Link()
    asyncio.run(main=link.rip(dir_path=dir_path, url=url, url_root=url_root, url_start=url_start))