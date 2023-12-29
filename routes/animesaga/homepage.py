import requests
from fastapi import APIRouter
import html
import json
from bs4 import BeautifulSoup as html


tags_metadata = ["AnimeSaga"]
homepage= APIRouter(tags=tags_metadata)
        
@homepage.get("/animesaga/home")
async def home():

    headers={
        "referer":"https://www.animesaga.in/",
        "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36 Edg/120.0.0.0"
    }
    res=requests.get("https://www.animesaga.in/",headers=headers)
    soup=html(res.content,features="html.parser")
    recent=[]
    return {"eor":"jj"}
