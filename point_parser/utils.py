from .match_state import MatchState


def transform_to_score_format(points_p1: int, points_p2: int) -> str:
    """
    Converts the integer representation of points in a service game to the
    format usual in tennis [e.g. 1-0 to 15:0].

    Args:
        points_p1: How many points p1 has won in the game.
        points_p2: How many points p2 has won in the game.

    Returns:
        A string in the format x:y; for example, "15:0" for points_p1=1 and
        points_p2=0.
    """

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


def match_summary_string(match_state: MatchState,
                         score_only: bool = False) -> str:
    """
    Summarises the match state in the usual scoring format.

    Args:
        match_state: The current state of the match.
        score_only: If True, only returns the score, not the names of the
            server & returner.

    Returns:
        A summary string, such as "Roger Federer - Rafael Nadal: 0-0 15:30".
    """

    if match_state.is_over:
        # TODO: This isn't great -- they're not server and returner!
        # We need to do p1 and p2 instead.
        winner = max(match_state.sets_won.items(), key=lambda x: x[1])[0]
        loser = min(match_state.sets_won.items(), key=lambda x: x[1])[0]
        cur_server, cur_returner = winner, loser
    else:
        cur_server, cur_returner = match_state.server, match_state.returner

    if not score_only:
        string = f'{cur_server} - {cur_returner}:'
    else:
        string = ''

    for cur_set in match_state.past_sets:

        to_add = (f' {cur_set.player_scores[cur_server]}-'
                  f'{cur_set.player_scores[cur_returner]}')

        if cur_set.tiebreak_score is not None:

            min_score = min(cur_set.tiebreak_score.values())
            to_add += f'({min_score})'

        string += to_add

    if match_state.is_over:
        return string.strip()

    # Add current set:
    string += (f' {match_state.cur_set_score[cur_server]}-'
               f'{match_state.cur_set_score[cur_returner]}')

    # Add current game score
    if match_state.is_tiebreak:
        string += (f' {match_state.cur_game_score[cur_server]}:'
                   f'{match_state.cur_game_score[cur_returner]}')
    else:
        string += ' ' + transform_to_score_format(
            match_state.cur_game_score[cur_server],
            match_state.cur_game_score[cur_returner])

    return string.strip()


def create_start_match_state(first_server: str, first_returner: str,
                             is_tiebreak: bool = False) -> MatchState:
    """
    Initialises the starting match state.

    Args:
        first_server: Player to serve first in the match.
        first_returner: Player to return first in the match.
        is_tiebreak: Whether or not the match starts in a tiebreak.

    Returns:
        The starting MatchState.
    """

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
        past_sets=list(),
        is_over=False
    )
