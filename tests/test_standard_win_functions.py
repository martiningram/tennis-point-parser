import point_parser.standard_win_functions as swf


def test_set_win_condition_tb_set():

    test_cases = [
        [(6, 4), True],
        [(7, 6), True],
        [(6, 7), True],
        [(7, 5), True],
        [(3, 6), True],
        [(4, 2), False],
        [(4, 4), False]
    ]

    for cur_args, cur_outcome in test_cases:

        assert(swf.set_win_condition_tb_set(*cur_args) == cur_outcome)


def test_set_win_condition_ad_set():

    test_cases = [
        [(6, 4), True],
        [(7, 6), False],
        [(8, 6), True],
        [(6, 8), True]
    ]

    for cur_args, cur_outcome in test_cases:

        assert(swf.set_win_condition_ad_set(*cur_args) == cur_outcome)


def test_match_over_best_of():

    assert(swf.match_over_best_of(3, 1, 5))


def test_standard_service_game_over():

    # Hold to 30
    assert(swf.standard_service_game_over(4, 2, True))

    # This is AD - 40
    assert(not swf.standard_service_game_over(4, 3, True))

    # This is game if no ad
    assert(swf.standard_service_game_over(4, 3, False))

    # This is a break
    assert(swf.standard_service_game_over(2, 4, True))


def test_roles_at_game_start():

    # First server has served, then first returner has served.
    games_played = 2

    assert(swf.roles_at_game_start(games_played, 'p1', 'p2') == ('p1', 'p2'))


def test_tiebreak_over_standard():

    assert(swf.tiebreak_over_standard(7, 2))

    assert(not swf.tiebreak_over_standard(4, 2))

    assert(not swf.tiebreak_over_standard(7, 7))
