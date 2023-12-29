import requests
from fastapi import APIRouter
import html
import json
from bs4 import BeautifulSoup as html


tags_metadata = ["AnimeSaga"]
search= APIRouter(tags=tags_metadata)
        
@search.get("/animesaga/search")
async def get_search(query:str):
    query=query.replace(" ","+")
    headers={
        "referer":"https://www.animesaga.in/",
        "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36 Edg/120.0.0.0"
    }
    res=requests.get(f"https://www.animesaga.in/?s={query}",headers=headers)
    soup=html(res.content,features="html.parser")
    items = soup.find_all('div',class_='result-item' )
    data = []
    for item in items:
        title=item.find('div',class_='title').find('a').text
        link=item.find('a')['href']
        img=item.find('img')['src'].replace('w92','w450')
        data.append({
            "title": title,
            "link": link,
            "img": img
        })

    return {"items": data}
