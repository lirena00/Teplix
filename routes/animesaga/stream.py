from fastapi import FastAPI
from bs4 import BeautifulSoup as html
import json
from fastapi import APIRouter
import re
import requests
import binascii
import hashlib
from base64 import b64decode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def decrypt(json_string):
    json_data = json.loads(json_string)
    try:
        salt = binascii.unhexlify(json_data["s"])
        iv = binascii.unhexlify(json_data["iv"])
    except Exception as e:
        return e
    ct = b64decode(json_data["ct"])
    concated_passphrase = "4MmH9EsZrq0WEekn".encode() + salt
    md5 = [hashlib.md5(concated_passphrase).digest()]
    for i in range(1, 3):
        md5.append(hashlib.md5(md5[i - 1] + concated_passphrase).digest())
    key = md5[0] + md5[1]
    key = key[:32]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    data = decryptor.update(ct) + decryptor.finalize()
    return data.decode('utf-8')

def scrape_data(url):
    response = requests.get(url)
    page_content = html(response.content, features="lxml")
    pattern = r"JScripts = '([^']*)'"
    match = re.search(pattern, str(page_content))
    if match:
        extracted_content = match.group(1)
        return extracted_content
    else:
        return {"error": "Pattern not found."}

tags_metadata = ["AnimeSaga"]
stream= APIRouter(tags=tags_metadata)

@stream.get("/animesaga/stream")
async def stream_content(url:str="https://www.animesaga.in/episodes/my-love-story-with-yamada-kun-at-lv999-season-1-episode-1/"):
    headers = {
        "referer": "https://www.animesaga.in/",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36 Edg/120.0.0.0"
    }
    res = requests.get(url, headers=headers)
    soup = html(res.content, features="lxml")
    items = soup.find('a', class_='pinterest dt_social')
    post = items['data-id']
    type_ = "tv"
    url = "https://animesaga.in/wp-admin/admin-ajax.php"
    data = {
        'post': post,
        'nume': '1',
        'type': type_,
        'action': 'doo_player_ajax'
    }
    resp = requests.post(url, data=data)
    respj = json.loads(resp.text)
    main_url = respj['embed_url']
    print(main_url)
    result = scrape_data(main_url)
    data = decrypt(result)
    soup = html(data, "lxml")
    x = str(soup).replace("\\t", "\t").replace("\\n", "\n").replace('\\"', '"')
    pattern = r'token = "([^"]+)"'
    result = {}
    match = re.search(pattern, x)
    if match:
        result['token'] = match.group(1)
    pattern = r'file: "([^"]+)"'
    match = re.search(pattern, x)
    if match:
        result['file'] = match.group(1).replace("\\/", "/").replace("&amp;", "&")
    pattern = r'subtitle: "([^"]+)"'
    match = re.search(pattern, x)
    if match:
        result['subtitle'] = f"[{match.group(1)}]".replace("\\/", "/").replace("&amp;", "&")
    return result