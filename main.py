# pyright: reportIgnoreCommentWithoutRule=false

from fastapi import FastAPI
import sqlite3
import datetime

from pydantic import BaseModel

from config import settings

app = FastAPI()
con = sqlite3.connect(settings.db_name)


@app.get("/api/leaderboard")
async def leaderboard():
    # Return a 2D array of people mapped to how many days they've held the horse total
    return {"message": "Hello World"}


@app.get("/api/history")
async def history():
    # Return a 2D array of the entire history of the horse exchanges
    return {"message": "Hello World"}


@app.get("/api/timer")
async def timer():
    # This will return the number of days until someone can challenge for the horse again
    return {"message": "Hello World"}


class Exchange(BaseModel):
    user: str
    date: datetime.date | None = datetime.now().date()  # pyright: ignore


@app.post("/api/exchange")
async def exchange(body: Exchange):
    print(body)
    return {"message": "Hello World"}
