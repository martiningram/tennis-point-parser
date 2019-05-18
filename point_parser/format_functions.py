from dataclasses import dataclass
from typing import Callable, Tuple


@dataclass
class FormatFunctions:
    """
    This class collects all the logic encoding tennis match rules.

    For examples, see the file "formats.py".
    """

    # FIXME: I wish I could name the input args here. Maybe abstract base
    # classes are the way to go after all?

    # TODO: The set win condition might vary by set -- the third bool is the
    # whether it's the final set.

    # Function taking games_won_p1, games_won_p2, is_final set, and returning
    # whether the set has been won.
    set_win_condition: Callable[[int, int, bool], bool]

    # Function taking games_won_p1, games_won_p2, is_final set, and returning
    # whether we are in a tiebreak.
    is_tiebreak_fun: Callable[[int, int, bool], bool]

    # Function taking games_won_p1, games_won_p2, is_final_set, and returning
    # whether the tiebreak is over.
    tiebreak_over: Callable[[int, int, bool], bool]

    # Function taking sets_won_p1, sets_won_p2, and returning whether the
    # match is over.
    match_over_fun: Callable[[int, int], bool]

    # Function taking points_won_p1, points_won_p2, and returning whether the
    # service game is over.
    service_game_over: Callable[[int, int], bool]

    # Takes total games & first server and returner and returns who is serving
    # at the start of the game.
    roles_at_game_start: Callable[[int, str, str], Tuple[str, str]]

    # Given the current set number, returns whether we are in the final set
    # or not.
    is_final_set: Callable[[int], bool]

    # Takes total points & first server and returner and returns who is serving
    # and receiving in the tiebreak.
    tiebreak_roles: Callable[[int, str, str], Tuple[str, str]]
