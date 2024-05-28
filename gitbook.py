import os
import asyncio
import aiohttp
import aiofiles
from bs4 import BeautifulSoup
from time import time


class New_time:
    
    async def download(self, path, url) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.ok:
                    async with aiofiles.open(file=path, mode="wb") as file:
                        async for chunk in resp.content.iter_chunked(n=8192):
                            await file.write(chunk)

                else:
                    print(f"Server gave back error {resp.status}")


    def verify(self, new_time, path):
        
        if not os.path.exists(path):
            open(file=path, mode="wt").close()

        with open(file=path, mode="rt", newline="\n") as file:
            old_time = file.read()
            if old_time == new_time:
                return False

            else:
                with open(file=path, mode="wt", newline="\n") as file:
                    file.write(new_time)
                    return True


    async def rip(self, path, url):
        
        file_path = f"{path}/temp.cache.html"
        
        await self.download(file_path, url)
        
        async with aiofiles.open(file=file_path, mode="rt", newline="\n") as file:
            soup = BeautifulSoup(await file.read(), "html.parser")
            os.remove(file_path)
            
            full_time = soup.find("new_time")
            
            new_time = full_time.get("datetime")
            
            time_path = f"{path}/.new_time.temp"
            
            return self.verify(new_time, time_path)



class Link:
    links = []


    async def download(self, path : str, url : str) -> None:
        async with aiohttp.ClientSession() as session:
            #print(path)
            async with session.get(url=url) as resp:
                if resp.ok:
                    async with aiofiles.open(file=path, mode="wb") as file:
                        async for chunk in resp.content.iter_chunked(n=41920):
                            await file.write(chunk)

                else:
                    print(f"Server gave back error {resp.status}")


    async def management(self, path, url, dir_path) -> None:
        await self.download(path, url)
        
        async with aiofiles.open(file=path, mode="rt", encoding="utf-8") as file:
            soup = BeautifulSoup(await file.read(), "html.parser")
        
            for tag in soup.find_all("a", href=True):
                self.links.append(tag)
            
            for tag in self.links:
                async with asyncio.TaskGroup() as tg:
                    tg.create_task(coro=self.rip(tag, dir_path, url))
                #print(tag)


    async def rip(self, tag, dir_path, url):
        link = tag["href"]
        
        if "utm_source" not in link:
            file_path = f"{dir_path}/{link}"
            os.makedirs(file_path, exist_ok=True)
            if os.path.exists(file_path):
                try:
                    os.rmdir(file_path)
                except OSError:
                    pass
                    
            
            if not link.startswith(url):
                link = "https://groupeinfo.gitbook.io" + link
            
            print(link)
            file_path = f"{file_path}.html"
            
            await self.download(file_path, link)
            
            await self.changes(file_path)


    async def changes(self, file_path):
        async with aiofiles.open(file=file_path, mode="rt", encoding="utf-8") as file:
            soup = BeautifulSoup(await file.read(), "html.parser")
            
            
            for link in soup.find_all("a", href=True):
                
                try:
                    url = link["href"]
                    self.links.append(url)
                except:
                    pass
                
                if len(link.contents) >= 2 and "utm_source" not in url:
                    if "group" in link.contents[1]["class"]:
                
                #if url == "/computer-science-data-base":
                #    url = f"{url}.html"

                        for script in soup.find_all("script"):
                            if script.string:
                                if url in script.string:
                                    
                                    script.string = script.string.replace(f"{url}\\", f"{url}.html\\")
                
                if url == "/computer-science-data-base":
                    for script in soup.find_all("script"):
                        if script.string:
                            if url in script.string:
                                script.string = script.string.replace(f'{url}/\\",\\', f'{url}.html\\",\\') #"pathname for only carre, pis pas logo en haut a gauche
            
            link["href"] = url
            
            async with aiofiles.open(file=file_path, mode="wt", encoding="utf-8") as filer:
                await filer.write(str(soup.prettify()))







if __name__ == "__main__":
    
    dir_path = "../computer-science-data-base"
    file_path = "/computer-science-data-base"
    url_root = "/computer-science-data-base"
    url = "https://groupeinfo.gitbook.io/computer-science-data-base/sources"
    
    
    
    os.makedirs(dir_path, exist_ok=True)
    
    new_time = New_time()
    
    #asyncio.run(main=new_time.rip(dir_path, url))
    
    link = Link()
    
    _ = time()
    asyncio.run(main=link.management(f"{dir_path}{file_path}.html", url, dir_path))
    print(time() - _)
