import os
import asyncio
import aiohttp
import aiofiles
from bs4 import BeautifulSoup


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



class Link:

    async def download(self, path : str, url : str) -> str:
        name = url.split("/")[-1] + ".html"
        async with aiohttp.ClientSession() as session:
            print(url)

            async with session.get(url=url) as resp:
                if resp.ok:
                    async with aiofiles.open(file=f"{path}/{name}", mode="wb") as file:
                        async for chunk in resp.content.iter_chunked(n=8192):
                            await file.write(chunk)
                        return name

                else:
                    print(f"Server gave back error {resp.status}")


    async def rip(self, dir_path : str, url, url_root : str, url_start : str, link : str) -> None:
        
        file_name = await self.management(url_root, dir_path, url_start, link)
        dir_path = f"{dir_path}{url_root}"

        async with aiofiles.open(file=f"{dir_path}/{file_name}", mode="rt", newline="\n", encoding="utf-8") as file:
            soup = BeautifulSoup(await file.read(), "html.parser")
            for link in soup.find_all("a"):
                
                async with asyncio.TaskGroup() as tg:
                    tg.create_task(coro=self.management(url_root, dir_path, url_start, link))


    async def management(self, url_root : str, dir_path : str, url_start : str, link : str):
        not_allowed = ["https:", "www.gitbook.com", "groupeinfo.gitbook.io", "", "?utm_source=content&utm_medium=trademark&utm_campaign=SoR8NHCZ4ZjclRjRssSc"]
        l = link.get("href")

        for directory in l.split("/"):
            if directory != l.split("/")[-1] and directory not in not_allowed or directory == "computer-science-data-base":
                #print(directory)
                dir_path = f"{dir_path}/{directory}"
                os.makedirs(dir_path, exist_ok=True)

        if url_root in l:
            if l == "https://groupeinfo.gitbook.io/computer-science-data-base":
                new_url = l

            else:
                new_url = ".".join(f"{url_start}{l}".split(".")[:-1])
            
            dreturn = f"{dir_path}/{await self.download(dir_path, new_url)}"
            
            async with aiofiles.open(file=dreturn, mode="rt", encoding="utf-8") as file:
                soup = BeautifulSoup(await file.read(), "html.parser")
                for link in soup.find_all("a", href=True):
                    
                    if not "#" in link.get("href"):
                        link["href"] = link["href"] + ".html"
                        for script in soup.find_all("script"):
                            script["src"] = ""
                        
                        async with aiofiles.open(file=dreturn, mode="wt", encoding="utf-8") as filer:
                            await filer.write(str(soup.prettify()))
                        
                


            
            return dreturn





if __name__ == "__main__":
    
    base_url = "https://gitbook.io"
    url_start = "https://groupeinfo.gitbook.io"
    dir_path = ".."
    url_root = "/computer-science-data-base"
    url = "".join((url_start, url_root))
    
    links = {"href" : url}
    
    time = Time()
    
    #asyncio.run(main=time.rip(dir_path, url))
    
    link = Link()
    asyncio.run(main=link.rip(dir_path=dir_path, url=url, url_root=url_root, url_start=url_start, link=links))
