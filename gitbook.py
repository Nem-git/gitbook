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
                async with asyncio.TaskGroup() as tg:
                    tg.create_task(coro=self.rip(tag, dir_path, url))

    async def rip(self, tag, dir_path, url):
        repo = "computer-science-data-base"
        link = tag["href"]
        
        last = link.split("/")[-1]
        if repo in link:
            file_path = f"{dir_path}/{link}"
            os.makedirs(file_path, exist_ok=True)
            if os.path.exists(file_path):
                try:
                    os.rmdir(file_path)
                except OSError:
                    pass
        
        if repo in link:
            if not link.startswith(url):
                link = "https://groupeinfo.gitbook.io" + link
            
            print(link)
            await self.download(f"{file_path}.html", link)
            
            await self.changes(file_path)


    async def changes(self, file_path):
        async with aiofiles.open(file=f"{file_path}.html", mode="rt", encoding="utf-8") as file:
            soup = BeautifulSoup(await file.read(), "html.parser")
            
            # Il va falloir que je fix les # un jour
            #for l in soup.find_all("a", href=True):
            #    if "#" in l["href"]:
            #        if l["href"].split("#")[0] != "":
            #            l["href"] = link + ".html#" + l["href"].split("#")[-1]
            #            
            #        print(l["href"])
            #    else:
            #        l["href"] = l["href"] + ".html"
            #    
            
            # J'essaie de fix les directories
            #for l in soup.find_all("a", href=True):
            #    for tags in l.children:
            #        if tags.name == "span":
            #            print(link)
            
            # C'est un essai pour enlever le code de search bar mais ca fait rien
            #for c in soup.find_all("div", {"class" : "flex md:w-56 grow-0 shrink-0 justify-self-end"}):
            #    print(c)
            #    c = c.button.decompose()
            #    print(c)
            
            
            
            async with aiofiles.open(file=f"{file_path}.html", mode="wt", encoding="utf-8") as filer:
                await filer.write(str(soup.prettify()))







if __name__ == "__main__":
    
    dir_path = "../computer-science-data-base"
    file_path = "/computer-science-data-base"
    url_root = "/computer-science-data-base"
    url = "https://groupeinfo.gitbook.io/computer-science-data-base"
    
    
    
    os.makedirs(dir_path, exist_ok=True)
    
    time = Time()
    
    #asyncio.run(main=time.rip(dir_path, url))
    
    link = Link()
    asyncio.run(main=link.management(f"{dir_path}{file_path}.html", url, dir_path))
