import requests
from fastapi import APIRouter
import html
import json
from bs4 import BeautifulSoup as html


tags_metadata = ["AnimeSaga"]
crunchyroll= APIRouter(tags=tags_metadata)
        
@crunchyroll.get("/animesaga/crunchyroll")
async def get_crunchy():

    headers={
        "referer":"https://www.animesaga.in/",
        "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36 Edg/120.0.0.0"
    }
    res=requests.get("https://www.animesaga.in/genre/crunchyroll/",headers=headers)
    soup=html(res.content,features="html.parser")
    crunchyroll=[]
    anime=soup.find('div',class_='items full').find_all('article')
    for item in anime:
        gr=item.find('img')
        title=gr['alt']
        img=gr['src']
        link=item.find('a')['href']
        crunchyroll.append({
            "img": img,
            "title":title,
            "link": link,
        })
    res=requests.get("https://www.animesaga.in/genre/crunchyroll/page/2/",headers=headers)
    soup=html(res.content,features="html.parser")
    anime=soup.find('div',class_='items full').find_all('article')
    for item in anime:
        gr=item.find('img')
        title=gr['alt']
        img=gr['src']
        link=item.find('a')['href']
        crunchyroll.append({
            "img": img,
            "title":title,
            "link": link,
        })
    return {"crunchyroll":crunchyroll}
