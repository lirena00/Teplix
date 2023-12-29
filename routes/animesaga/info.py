import requests
from fastapi import APIRouter
import html
import json
import re
from bs4 import BeautifulSoup as html
import lxml

tags_metadata = ["AnimeSaga"]
info= APIRouter(tags=tags_metadata)

@info.get("/animesaga/info")
async def get_info(url:str="https://www.animesaga.in/tvshows/the-reincarnation-of-the-strongest-exorcist-in-another-world/"):

    headers={
        "referer":"https://www.animesaga.in/",
        "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36 Edg/120.0.0.0"
    }
    res=requests.get(url,headers=headers)
    soup=html(res.content,features="lxml")
    tags=[]
    title=soup.find('h1').text
    div_with_class_sgeneros = soup.find('div', class_='sgeneros')
    if div_with_class_sgeneros:
        tags_links = div_with_class_sgeneros.find_all('a')
        for link in tags_links:
            tags.append(link.text)

    seasons_data = []
    seasons= soup.find_all('div',class_='se-a')
    for season in seasons: 
        episodes_data=[]
        episodes=season.find('ul').find_all('li')
        for episode in episodes:
            image= episode.find('img')['src']
            gr= episode.find('a')
            episode_title=gr.text
            link=gr['href']
            episodes_data.append({
                "image": image,
                "title": episode_title,
                "link": link
            })
        seasons_data.append({
            "episodes": episodes_data
        })



    return {
        "title": title,
        "tags": tags,
        "seasons": seasons_data
    }