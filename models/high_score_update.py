from pydantic import BaseModel

class HighScoreUpdate(BaseModel):
    username: str
    highest_wpm: int
    games_played: int
    tug_entries: int
    tug_wins: int