from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Odd:
    id: str
    market: str
    player_name: Optional[str]
    decimal_odds: float

@dataclass
class Match:
    id: str
    home_team: str
    away_team: str
    start_time: datetime
    league: str
    odds: List[Odd]
