import requests
from fastapi import APIRouter
import re
import html
import json
from bs4 import BeautifulSoup as html


tags_metadata = ["AnimeSaga"]
recent= APIRouter(tags=tags_metadata)
        
@recent.get("/animesaga/recent")
async def get_recent():

    headers={
        "referer":"https://www.animesaga.in/",
        "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36 Edg/120.0.0.0"
    }
    res=requests.get("https://www.animesaga.in/episodes/",headers=headers)
    recent=[]
    soup=html(res.content,features="html.parser")
    episodes=soup.find('div',id='archive-content').find_all('article')
    for episode in episodes:
        img=episode.find('img')['src'].replace('w300','w500')
        gr=episode.find('h3').find('a')
        episode_title=gr.text
        link=gr['href']
        episode_n=episode.find_all('span')[-2].text
        title=episode.find_all('span')[-1].text
        episode_no= re.search(r'E(\d+)', episode_n).group(1) if re.search(r'E(\d+)', episode_n) else None
        recent.append({
            "img": img,
            "title":title,
            "episode-title": episode_title,
            "link": link,
            "episode_no": int(episode_no)
        })
    return {"recent":recent}
