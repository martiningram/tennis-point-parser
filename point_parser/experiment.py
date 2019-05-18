import sys
import numpy as np
import point_parser.parse as p
import point_parser.standard_win_functions as swf
from functools import partial


sys.setrecursionlimit(10000)

wimbledon_format_functions = p.FormatFunctions(
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

start_state = p.create_start_match_state('Roger Federer', 'Rafael Nadal')

wl_vector = np.random.choice([True, False], size=300, p=[0.95, 0.05])

print(p.process_win_loss_vector(wl_vector, start_state,
                                wimbledon_format_functions))
