import point_parser.parse as p
import point_parser.standard_win_functions as swf
from functools import partial

classic_slam_format_men = p.FormatFunctions(
    set_win_condition=swf.set_win_condition_ad_final_set,
    is_tiebreak_fun=swf.is_tiebreak_fun_no_tb_final_set,
    tiebreak_over=lambda points_p1, points_p2, _: swf.tiebreak_over_standard(
        points_p1, points_p2),
    match_over_fun=partial(swf.match_over_best_of, best_of=5),
    service_game_over=partial(swf.standard_service_game_over, has_ad=True),
    roles_at_game_start=swf.roles_at_game_start,
    is_final_set=lambda set_num: set_num + 1 == 5,
    tiebreak_roles=swf.tiebreak_roles_standard
)

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
