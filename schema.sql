CREATE TABLE ownership (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    date DATE NOT NULL
);

CREATE TABLE leaderboard (
  username TEXT PRIMARY KEY,
  days_held INTEGER NOT NULL
);
