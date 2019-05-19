import point_parser.parse as p
import point_parser.standard_win_functions as swf
from functools import partial

"""
This module contains the different match formats. They encode the different
rules, such as best of five sets, best of three sets, tiebreak formats and so
on.

I have annotated the "classic_slam_format_men" so that it is clear what the
functions mean.
"""

# This is the old-style best of five grand slam format with no tiebreak
# in the deciding set.
classic_slam_format_men = p.FormatFunctions(
    # Advantage final set win condition
    set_win_condition=swf.set_win_condition_ad_final_set,
    # Tiebreak at the usual score but not in final set
    is_tiebreak_fun=swf.is_tiebreak_fun_no_tb_final_set,
    # Tiebreak is the usual tiebreak
    tiebreak_over=lambda points_p1, points_p2, _: swf.tiebreak_over_standard(
        points_p1, points_p2),
    # Winner of best of 5 sets wins
    match_over_fun=partial(swf.match_over_best_of, best_of=5),
    # Service game is the usual service game, with ad scoring
    service_game_over=partial(swf.standard_service_game_over, has_ad=True),
    # We can find the roles (server, returner) at each game start the usual way
    roles_at_game_start=swf.roles_at_game_start,
    # Fifth set is final set TODO Maybe rename to "deciding"
    is_final_set=lambda set_num: set_num + 1 == 5,
    # In tiebreak, we can find server and returner the standard way
    tiebreak_roles=swf.tiebreak_roles_standard
)

# This is the standard best of three set format with tiebreaks in every set.
# Most tournaments on the ATP (except for slams) and on the WTA are played in
# this format.
standard_best_of_three = p.FormatFunctions(
    set_win_condition=lambda games_p1, games_p2, _:
        swf.set_win_condition_tb_set(games_p1, games_p2),
    is_tiebreak_fun=swf.is_tiebreak_fun_uso_style,
    tiebreak_over=lambda points_p1, points_p2, _: swf.tiebreak_over_standard(
        points_p1, points_p2),
    match_over_fun=partial(swf.match_over_best_of, best_of=3),
    service_game_over=partial(swf.standard_service_game_over, has_ad=True),
    roles_at_game_start=swf.roles_at_game_start,
    is_final_set=lambda set_num: set_num + 1 == 3,
    tiebreak_roles=swf.tiebreak_roles_standard
)

# This is the best of five grand slam format, but as played by the US Open,
# which has tiebreaks in all five sets.
# TODO: There is lots of duplication with the "classic" format here. But
# maybe that's all right?
us_open_format_men = p.FormatFunctions(
    set_win_condition=lambda games_p1, games_p2, _:
        swf.set_win_condition_tb_set(games_p1, games_p2),
    is_tiebreak_fun=swf.is_tiebreak_fun_uso_style,
    tiebreak_over=lambda points_p1, points_p2, _: swf.tiebreak_over_standard(
        points_p1, points_p2),
    match_over_fun=partial(swf.match_over_best_of, best_of=5),
    service_game_over=partial(swf.standard_service_game_over, has_ad=True),
    roles_at_game_start=swf.roles_at_game_start,
    is_final_set=lambda set_num: set_num + 1 == 5,
    tiebreak_roles=swf.tiebreak_roles_standard
)

classic_slam_format_ladies = p.FormatFunctions(
    # Advantage final set win condition
    set_win_condition=swf.set_win_condition_ad_final_set,
    # Tiebreak at the usual score but not in final set
    is_tiebreak_fun=swf.is_tiebreak_fun_no_tb_final_set,
    # Tiebreak is the usual tiebreak
    tiebreak_over=lambda points_p1, points_p2, _: swf.tiebreak_over_standard(
        points_p1, points_p2),
    # Winner of best of 3 sets wins
    match_over_fun=partial(swf.match_over_best_of, best_of=3),
    # Service game is the usual service game, with ad scoring
    service_game_over=partial(swf.standard_service_game_over, has_ad=True),
    # We can find the roles (server, returner) at each game start the usual way
    roles_at_game_start=swf.roles_at_game_start,
    # Third set is final set TODO Maybe rename to "deciding"
    is_final_set=lambda set_num: set_num + 1 == 3,
    # In tiebreak, we can find server and returner the standard way
    tiebreak_roles=swf.tiebreak_roles_standard
)

us_open_format_ladies = p.FormatFunctions(
    # TB final set
    set_win_condition=lambda games_p1, games_p2, _:
        swf.set_win_condition_tb_set(games_p1, games_p2),
    # Tiebreak at the usual score, regardless of which set
    is_tiebreak_fun=swf.is_tiebreak_fun_uso_style,
    # Tiebreak is the usual tiebreak
    tiebreak_over=lambda points_p1, points_p2, _: swf.tiebreak_over_standard(
        points_p1, points_p2),
    # Winner of best of 3 sets wins
    match_over_fun=partial(swf.match_over_best_of, best_of=3),
    # Service game is the usual service game, with ad scoring
    service_game_over=partial(swf.standard_service_game_over, has_ad=True),
    # We can find the roles (server, returner) at each game start the usual way
    roles_at_game_start=swf.roles_at_game_start,
    # Third set is final set TODO Maybe rename to "deciding"
    is_final_set=lambda set_num: set_num + 1 == 3,
    # In tiebreak, we can find server and returner the standard way
    tiebreak_roles=swf.tiebreak_roles_standard
)
