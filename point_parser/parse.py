from typing import List, Dict, Callable, Tuple, Optional
from dataclasses import dataclass


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


@dataclass
class FormatFunctions:

    # TODO: The set win condition might vary by set -- the third bool is the
    # whether it's the final set.
    set_win_condition: Callable[[int, int, bool], bool]
    is_tiebreak_fun: Callable[[int, int, bool], bool]
    tiebreak_over: Callable[[int, int, bool], bool]

    match_over_fun: Callable[[int, int], bool]
    service_game_over: Callable[[int, int], bool]

    # Takes total games & first server and returner
    roles_at_game_start: Callable[[int, str, str], Tuple[str, str]]

    is_final_set: Callable[[int], bool]

    # Takes total points & first server and returner
    tiebreak_roles: Callable[[int, str, str], Tuple[str, str]]


def player_wins_set(
        match_state: MatchState,
        winning_player: str,
        losing_player: str,
        format_functions: FormatFunctions) -> MatchState:

    match_state.sets_won[winning_player] += 1
    match_state.past_sets.append(
        CompletedSet(
            player_scores=match_state.cur_set_score,
            tiebreak_score=(match_state.cur_game_score if
                            match_state.is_tiebreak else None)
        ))

    if not format_functions.match_over_fun(
            match_state.cur_set_score[winning_player],
            match_state.cur_set_score[losing_player]):
        match_state.set_num += 1
        match_state.reset_set_score()

    return match_state


def player_wins_game(match_state: MatchState,
                     winning_player: str,
                     losing_player: str,
                     format_functions: FormatFunctions) \
        -> MatchState:

    games_winner, games_loser = (match_state.cur_game_score[winning_player],
                                 match_state.cur_game_score[losing_player])

    games_winner += 1

    match_state.cur_set_score[winning_player] += 1
    match_state.total_games_played += 1

    # Set server and returner
    match_state.server, match_state.returner = \
        format_functions.roles_at_game_start(match_state.total_games_played,
                                             match_state.first_server,
                                             match_state.first_returner)

    is_final_set = format_functions.is_final_set(match_state.set_num)

    # Check whether player won the set
    if format_functions.set_win_condition(
            match_state.cur_set_score[winning_player],
            match_state.cur_set_score[losing_player], is_final_set):

        match_state = player_wins_set(match_state, winning_player,
                                      losing_player, format_functions)

    match_state.is_tiebreak = format_functions.is_tiebreak_fun(
        match_state.cur_set_score[winning_player],
        match_state.cur_set_score[losing_player],
        is_final_set)

    match_state.reset_game_score()

    return match_state


def advance_tiebreak(server_won: bool,
                     match_state: MatchState,
                     format_functions: FormatFunctions) -> MatchState:

    # Advance the game score
    if server_won:
        match_state.cur_game_score[match_state.server] += 1
    else:
        match_state.cur_game_score[match_state.returner] += 1

    if format_functions.tiebreak_over(
            match_state.cur_game_score[match_state.server],
            match_state.cur_game_score[match_state.returner],
            format_functions.is_final_set(match_state.set_num)):

        winning_player, losing_player = get_point_winner_loser(
            match_state.server, match_state.returner, server_won)

        match_state = player_wins_game(match_state, winning_player,
                                       losing_player, format_functions)

        return match_state

    total_points = sum(match_state.cur_game_score.values())
    start_server, start_returner = format_functions.roles_at_game_start(
        match_state.total_games_played, match_state.first_server,
        match_state.first_returner)

    # Otherwise, adjust who's serving
    match_state.server, match_state.returner = \
        format_functions.tiebreak_roles(total_points, start_server,
                                        start_returner)

    return match_state


def get_point_winner_loser(server, returner, server_won):

    winning_player, losing_player = (
        (server, returner) if server_won else (returner, server))

    return winning_player, losing_player


def advance_service_game(server_won: bool,
                         match_state: MatchState,
                         format_functions: FormatFunctions) \
        -> MatchState:

    # Advance the game score
    if server_won:
        match_state.cur_game_score[match_state.server] += 1
    else:
        match_state.cur_game_score[match_state.returner] += 1

    # See whether the service game is over
    if format_functions.service_game_over(
            match_state.cur_game_score[match_state.server],
            match_state.cur_game_score[match_state.returner]):

        winning_player, losing_player = get_point_winner_loser(
            match_state.server, match_state.returner, server_won)

        match_state = player_wins_game(match_state, winning_player,
                                       losing_player, format_functions)

    return match_state


def process_win_loss_vector(win_loss_vector: List[bool],
                            match_state: MatchState,
                            format_functions: FormatFunctions):

    if len(win_loss_vector) == 0:
        return match_state

    cur_win_loss = win_loss_vector[0]

    # Otherwise, do stuff and recurse.
    if match_state.is_tiebreak:
        match_state = advance_tiebreak(cur_win_loss, match_state,
                                       format_functions)
    else:
        match_state = advance_service_game(cur_win_loss, match_state,
                                           format_functions)

    print(match_summary_string(match_state))

    # Recurse
    return process_win_loss_vector(win_loss_vector[1:], match_state,
                                   format_functions)


def create_start_match_state(first_server: str, first_returner: str,
                             is_tiebreak: bool = False) -> MatchState:

    return MatchState(
        server=first_server,
        returner=first_returner,
        is_tiebreak=is_tiebreak,
        first_server=first_server,
        first_returner=first_returner,
        set_num=0,
        total_games_played=0,
        cur_set_score={first_server: 0, first_returner: 0},
        cur_game_score={first_server: 0, first_returner: 0},
        sets_won={first_server: 0, first_returner: 0},
        past_sets=list()
    )


def transform_to_score_format(points_p1: int, points_p2: int) -> str:

    lookup = {
        0: '0',
        1: '15',
        2: '30',
        3: '40',
        4: 'AD',
    }

    if max(points_p1, points_p2) > 3:

        difference = points_p1 - points_p2
        assert abs(difference) <= 1

        if difference == 1:
            points_p1, points_p2 = 4, 3
        elif difference == 0:
            points_p1, points_p2 = 3, 3
        elif difference == -1:
            points_p1, points_p2 = 3, 4

    return f'{lookup[points_p1]}:{lookup[points_p2]}'


def match_summary_string(match_state: MatchState) -> str:

    cur_server, cur_returner = match_state.server, match_state.returner

    string = f'{cur_server} - {cur_returner}: '

    for cur_set in match_state.past_sets:

        to_add = (f'{cur_set.player_scores[cur_server]}-'
                  f'{cur_set.player_scores[cur_returner]} ')

        if cur_set.tiebreak_score is not None:

            min_score = min(cur_set.tiebreak_score.values())

        to_add += f'({min_score}) '

        string += to_add

    # Add current set:
    string += (f'{match_state.cur_set_score[cur_server]}-'
               f'{match_state.cur_set_score[cur_returner]} ')

    # Add current game score
    if match_state.is_tiebreak:
        string += (f'{match_state.cur_game_score[cur_server]}:'
                   f'{match_state.cur_game_score[cur_returner]}')
    else:
        string += transform_to_score_format(
            match_state.cur_game_score[cur_server],
            match_state.cur_game_score[cur_returner])

    return string
