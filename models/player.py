from pydantic import BaseModel

class Player(BaseModel):
    username: str
    total_games: int
    games_won: int
    highest_wpm: int
    average_wpm: int