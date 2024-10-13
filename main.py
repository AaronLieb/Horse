# pyright: reportIgnoreCommentWithoutRule=false, reportUnusedCallResult=false

from fastapi import FastAPI
from sqlite3 import connect, Date
from datetime import datetime

from pydantic import BaseModel

from config import settings

app = FastAPI()
con = connect(settings.db_name)


@app.get("/api/leaderboard")
async def leaderboard():
    # Return a 2D array of people mapped to how many days they've held the horse total
    cursor = con.cursor()
    cursor.execute('SELECT username, days_held FROM ownership ORDER BY days_held DESC')

    rows = cursor.fetchall()
    leaderboard = [[row[0], row[1]] for row in rows]
    return {"message": leaderboard}


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
    date: Date | None = datetime.now().date()


@app.post("/api/exchange")
async def exchange(body: Exchange):
    cur = con.cursor()
    cur.execute("INSERT INTO ownership VALUES (?, ?)", (body.date, body.user))
    con.commit()
