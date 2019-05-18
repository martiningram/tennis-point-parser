import sys
import numpy as np
import point_parser.parse as p
from point_parser.formats import classic_slam_format_men


sys.setrecursionlimit(10000)

start_state = p.create_start_match_state('Roger Federer', 'Rafael Nadal')

wl_vector = np.random.choice([True, False], size=300, p=[0.95, 0.05])

print(p.process_win_loss_vector(
    wl_vector, start_state, classic_slam_format_men))
