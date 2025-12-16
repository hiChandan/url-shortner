import secrets
from fastapi import FastAPI
from app.database import collection
import random
import string
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from app.database import collection
from datetime import datetime
import random
import string
from datetime import datetime, timedelta
from app.database import collection, redis_client

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    return FileResponse("static/index.html")


def generate_short_code(length=7):
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))


@app.post("/shorten")
def shorten_url(long_url: str, days_valid: int = 7):
    expires_at = datetime.utcnow() + timedelta(days=days_valid)

    while True:
        try:
            code = generate_short_code()
            collection.insert_one({
                "short_code": code,
                "long_url": long_url,
                "created_at": datetime.utcnow(),
                "expires_at": expires_at
            })
            return {
                "short_code": code,
                "expires_at": expires_at
            }
        except Exception:
            continue


@app.get("/{short_code}")
def redirect(short_code: str):
    cached_url = redis_client.get(short_code)
    if cached_url:
        return RedirectResponse(cached_url, status_code=307)

    data = collection.find_one({"short_code": short_code})
    if not data:
        raise HTTPException(
            status_code=404, detail="Link expired or not found")

    redis_client.setex(short_code, 3600, data["long_url"])

    return RedirectResponse(data["long_url"], status_code=307)
