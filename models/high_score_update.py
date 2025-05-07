from pydantic import BaseModel

class HighScoreUpdate(BaseModel):
    username: str
    highest_wpm: int
    games_played: int = 1
    tug_entries: int = 0
    tug_wins: int = 0