# pyright: reportIgnoreCommentWithoutRule=false, reportUnusedCallResult=false

from fastapi import FastAPI
from sqlite3 import connect, Date
from datetime import datetime, date

from pydantic import BaseModel

from config import settings

app = FastAPI()
con = connect(settings.db_name)


@app.get("/api/leaderboard")
async def leaderboard():
    # Return a 2D array of people mapped to how many days they've held the horse total
    cursor = con.cursor()
    cursor.execute(
        "SELECT username, days_held FROM leaderboard ORDER BY days_held DESC"
    )

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
    exchange_date: date = datetime.now().date()


@app.post("/api/exchange")
async def exchange(body: Exchange):
    cur = con.cursor()

    # Fetch the most recent exchange
    cur.execute("SELECT * FROM ownership ORDER BY date LIMIT 1")
    result = cur.fetchone()
    prev_date: str = result[0]
    prev_user: str = result[1]

    diff_days = (
        body.exchange_date - datetime.strptime(prev_date, "%Y-%m-%d").date()
    ).days

    # Fetch their current days_held
    cur.execute("SELECT days_held FROM leaderboard WHERE username = ?", (prev_user,))
    result = cur.fetchone()
    if result is None:
        # Add user to leaderboard
        cur.execute("INSERT INTO leaderboard VALUES (?, ?)", (prev_user, 0))
    else:
        # Update their current days_held
        days_held: int = result[0]
        cur.execute(
            "UPDATE leaderboard SET days_held = ? WHERE username = ?",
            (days_held + diff_days, prev_user),
        )

    cur.execute("INSERT INTO ownership VALUES (?, ?)", (body.exchange_date, body.user))
    con.commit()
