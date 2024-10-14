# pyright: reportIgnoreCommentWithoutRule=false, reportUnusedCallResult=false

from fastapi import FastAPI
from sqlite3 import connect
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

    rows: list[list[int | str]] = cursor.fetchall()
    leaderboard = [[row[0], row[1]] for row in rows]

    cursor.execute('SELECT username, date FROM ownership ORDER BY date DESC LIMIT 1')
    recent_holder = cursor.fetchone()

    recent_date = datetime.strptime(recent_holder[1], "%Y-%m-%d")
    extra_days = (datetime.today() - recent_date).days
    for row in leaderboard:
        if row[0] == recent_holder[0]:
            row[1] += extra_days

    return {"leaderboard": leaderboard}


@app.get("/api/history")
async def history():
    # Return a 2D array of the entire history of the horse exchanges
    cursor = con.cursor()
    cursor.execute('SELECT username, date FROM ownership ORDER BY days_held DESC')

    rows = cursor.fetchall()
    leaderboard = [[row[0], row[1]] for row in rows]
    return {"message": "Hello World"}


@app.get("/api/timer")
async def timer():
    cur = con.cursor()

    # Fetch the most recent exchange
    cur.execute("SELECT date FROM ownership ORDER BY date LIMIT 1")
    result: list[str] | None = cur.fetchone()

    time_remaining = result[0] if result is not None else 0
    return {"time_remaining": time_remaining}


class Exchange(BaseModel):
    user: str
    exchange_date: date = datetime.now().date()


@app.post("/api/exchange")
async def exchange(body: Exchange):
    cur = con.cursor()

    # Fetch the most recent exchange
    cur.execute("SELECT date, username FROM ownership ORDER BY date LIMIT 1")
    latest_exchange: list[str] | None = cur.fetchone()

    if latest_exchange is not None:
        prev_date: str = latest_exchange[0]
        prev_user: str = latest_exchange[1]

        diff_days = (
            body.exchange_date - datetime.strptime(prev_date, "%Y-%m-%d").date()
        ).days

        # Fetch their current days_held
        cur.execute(
            "SELECT days_held FROM leaderboard WHERE username = ?", (prev_user,)
        )
        result: list[int] | None = cur.fetchone()
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
