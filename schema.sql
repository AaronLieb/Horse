CREATE TABLE ownership (
    date DATE PRIMARY KEY,
    username TEXT NOT NULL
);

CREATE TABLE leaderboard (
  username TEXT PRIMARY KEY,
  days_held INTEGER NOT NULL
);
