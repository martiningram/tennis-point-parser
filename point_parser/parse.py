from copy import deepcopy
from typing import List
from .match_state import MatchState
from .format_functions import FormatFunctions
from .manipulate_match_state import advance_tiebreak, advance_service_game
from .utils import match_summary_string, create_start_match_state


def process_win_loss_vector(win_loss_vector: List[bool],
                            match_state: MatchState,
                            format_functions: FormatFunctions,
                            debug_print_each_point: bool = False) \
        -> List[MatchState]:
    """
    Parses a boolean sequence of wins and losses and returns the sequence of
    MatchStates implied.

    Args:
        win_loss_vector: A list of True and False indicating whether the server
            won or lost the point.
        match_state: The state of the match before the updates in the vector.
        format_functions: The functions encoding the rules of the match [see
            formats.py for examples].
        debug_print_each_point: Optionally print the result of each update for
            debugging purposes.

    Returns:
        A list of MatchStates, each representing the result of each update
        to the match state.

    Example::

        import point_parser.utils as utils
        import point_parser.formats as fmts

        states = process_win_loss_vector(
            [True],
            utils.create_start_match_state('Roger Federer', 'Rafael Nadal'),
            fmts.classic_slam_format_men,
        )

        # This should return:
        [MatchState(server='Roger Federer', returner='Rafael Nadal',
        is_tiebreak=False, first_server='Roger Federer', first_returner='Rafael
        Nadal', set_num=0, total_games_played=0, cur_set_score={'Roger
        Federer': 0, 'Rafael Nadal': 0}, cur_game_score={'Roger Federer': 1,
        'Rafael Nadal': 0}, sets_won={'Roger Federer': 0, 'Rafael Nadal': 0},
        past_sets=[], is_over=False)]

    """

    # TODO: Check whether base case etc. really make sense.

    # We're done if there are no more points to advance.
    if len(win_loss_vector) == 0:
        return []

    # Otherwise, the match better not be over!
    assert not match_state.is_over

    cur_win_loss = win_loss_vector[0]

    if match_state.is_tiebreak:
        match_state = advance_tiebreak(cur_win_loss, match_state,
                                       format_functions)
    else:
        match_state = advance_service_game(cur_win_loss, match_state,
                                           format_functions)

    if debug_print_each_point:
        print(cur_win_loss)
        print(match_summary_string(match_state))

    # Recurse
    return [match_state] + process_win_loss_vector(
        win_loss_vector[1:], deepcopy(match_state), format_functions,
        debug_print_each_point)
