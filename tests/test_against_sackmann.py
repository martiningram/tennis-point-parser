import os
import pytest
import point_parser.compare_with_sackmann as cws


def test_against_sackmann():

    if 'SACK_POINT_PATH' not in os.environ:
        pytest.skip("Environment variable SACK_POINT_PATH is unset."
                    " To compare against Sackmann scores, please set it to"
                    " the base path of Jeff Sackmann's tennis_pointbypoint"
                    " repo.")

    sack_files = ['pbp_matches_atp_main_current.csv',
                  'pbp_matches_atp_main_archive.csv',
                  'pbp_matches_wta_main_archive.csv',
                  'pbp_matches_wta_main_current.csv']

    # TODO: 36 seems high. Check them in detail!
    expected_wrong = [4, 36, 2, 0]

    for cur_sack_file, cur_expected in zip(sack_files, expected_wrong):

        sack_file = os.path.join(
            os.environ['SACK_POINT_PATH'],
            cur_sack_file
        )

        sack_data = cws.load_sackmann_data(sack_file)
        problematic = cws.validate_all(sack_data)

        # There should be four of these, all caused by Jeff mistakenly
        # including retirements.
        assert(len(problematic) == cur_expected)
