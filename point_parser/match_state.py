from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class CompletedSet:

    player_scores: Dict[str, int]
    tiebreak_score: Optional[Dict[str, int]]


@dataclass
class MatchState:
    """Keeps track of a match state over time."""
    server: str
    returner: str
    is_tiebreak: bool

    first_server: str
    first_returner: str

    set_num: int
    total_games_played: int

    cur_set_score: Dict[str, int]
    cur_game_score: Dict[str, int]

    sets_won: Dict[str, int]
    past_sets: List[CompletedSet]

    def reset_game_score(self):

        self.cur_game_score = {self.server: 0, self.returner: 0}

    def switch_server_and_returner(self):

        self.server, self.returner = self.returner, self.server

    def reset_set_score(self):

        self.cur_set_score = {self.server: 0, self.returner: 0}

    is_over: bool
