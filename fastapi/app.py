import os
import requests
import uvicorn
from fastapi import FastAPI

BASE_URL = os.getenv("BASE_URL")
app = FastAPI()


@app.get("/{url_path:path}")
async def proxy(url_path: str):
    res = requests.get(f'{BASE_URL}/{url_path}')
    if res.ok:
        return res.content

    return {"success": False}


if __name__ == '__main__':
    uvicorn.run(app)
