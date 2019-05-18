import numpy as np


def set_win_condition_ad_set(games_p1: int, games_p2: int) -> bool:

    enough_games = max(games_p1, games_p2) >= 6
    enough_margin = np.abs(games_p1 - games_p2) >= 2

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
