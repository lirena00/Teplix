import requests
from fastapi import APIRouter
import html
import json
from bs4 import BeautifulSoup as html

tags_metadata = ["AnimeSaga"]
shows= APIRouter(tags=tags_metadata)
        
@shows.get("/animesaga/shows")
async def tvshows():

    headers={
        "referer":"https://www.animesaga.in/",
        "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36 Edg/120.0.0.0"
    }
    res=requests.get("https://www.animesaga.in/tvshows/",headers=headers)
    soup=html(res.content,features="html.parser")
    shows=[]
    tv=soup.find('div',id='archive-content').find_all('article')
    for item in tv:
        gr=item.find('img')
        title=gr['alt']
        img=gr['src']
        link=item.find('a')['href']
        shows.append({
            "img": img,
            "title":title,
            "link": link,
        })
        
    return {"shows":shows}
