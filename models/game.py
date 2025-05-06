from pydantic import BaseModel
from typing import List, Optional

class Game(BaseModel):
    id: Optional[id] = None
    status: Optional[str] = "pending"
    max_players: Optional[int] = 2
    current_round: Optional[int] = 0
    target_text: Optional[str] = ""
    time_limit: Optional[int] = 60
    winner_id: Optional[str] = None