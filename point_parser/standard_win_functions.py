from typing import Tuple


def set_win_condition_ad_set(games_p1: int, games_p2: int) -> bool:

    enough_games = max(games_p1, games_p2) >= 6
    enough_margin = abs(games_p1 - games_p2) >= 2

    return enough_games and enough_margin


def set_win_condition_tb_set(games_p1: int, games_p2: int) -> bool:

    ad_set_condition = set_win_condition_ad_set(games_p1, games_p2)
    tb_won = (games_p1 + games_p2) == 13

    return ad_set_condition or tb_won


def set_win_condition_ad_final_set(games_p1: int, games_p2: int,
                                   final_set: bool) -> bool:

    if final_set:
        return set_win_condition_ad_set(games_p1, games_p2)
    else:
        return set_win_condition_tb_set(games_p1, games_p2)


def match_over_best_of(sets_won_p1: int, sets_won_p2: int,
                       best_of: int) -> bool:

    assert best_of in [3, 5]

    max_sets = max(sets_won_p1, sets_won_p2)

    if best_of == 3:
        return max_sets == 2

    else:
        return max_sets == 3


def standard_service_game_over(points_p1: int, points_p2: int,
                               has_ad: bool = True) -> bool:

    diff = abs(points_p1 - points_p2)
    max_pts = max(points_p1, points_p2)

    enough_points = max_pts >= 4
    enough_diff = diff >= 2

    if has_ad:
        return enough_points and enough_diff
    else:
        return enough_points


def roles_at_game_start(total_games_played: int, first_server: str,
                        first_returner: str) -> Tuple[str, str]:

    modulo = total_games_played % 2

    # If 1 game played, returner plays.
    if modulo == 1:
        return first_returner, first_server
    else:
        return first_server, first_returner


def is_tiebreak_fun_uso_style(games_p1: int, games_p2: int,
                              is_final_set: bool) -> bool:

    return games_p1 == 6 and games_p2 == 6


def is_tiebreak_fun_no_tb_final_set(games_p1: int, games_p2: int,
                                    is_final_set: bool) -> bool:

    if is_final_set:
        return False
    else:
        return is_tiebreak_fun_uso_style(games_p1, games_p2, is_final_set)


def tiebreak_over_standard(points_p1: int, points_p2: int) -> bool:

    enough_points = max(points_p1, points_p2) >= 7
    enough_diff = abs(points_p1 - points_p2) >= 2

    return enough_points and enough_diff


def tiebreak_roles_standard(total_points: int, first_server: str,
                            first_returner: str) -> Tuple[str, str]:

    if total_points % 4 in [1, 2]:

        return (first_returner, first_server)

    else:

        return (first_server, first_returner)
