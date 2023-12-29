from fastapi import FastAPI
from fastapi.responses import RedirectResponse


from routes import *

__version__ = "1.0.0"

app = FastAPI(
	title="AnimeSaga-API",
	description="A  API made by  [LiReNa](https://github.com/LiReNa00)"
)



@app.get("/")
async def main():
	return RedirectResponse("/docs")


app.include_router(router=stream)
app.include_router(router=info)
app.include_router(router=search)
app.include_router(router=crunchyroll)
app.include_router(router=recent)
app.include_router(router=shows)
app.include_router(router=movies)
#uvicorn main:app --host 0.0.0.0 --port 8080 --reload

