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
