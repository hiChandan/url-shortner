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
import random, string


app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("static/index.html")

import secrets
import string

def generate_short_code(length=7):
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))


@app.post("/shorten")
def shorten_url(long_url: str):
    code = generate_short_code()
    collection.insert_one({"code": code, "url": long_url})
    return {"short_url": f"http://localhost:8000/{code}"}

@app.get("/{code}")
def redirect_url(code: str):
    data = collection.find_one({"code": code})
    if not data:
        return {"error": "URL not found"}
    return {"original_url": data["url"]}
