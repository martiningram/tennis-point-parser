import pandas as pd
from typing import List, Dict, Any
from point_parser.parse import (create_start_match_state,
                                process_win_loss_vector, match_summary_string,
                                MatchState, FormatFunctions)
from point_parser.formats import (standard_best_of_three,
                                  classic_slam_format_men, us_open_format_men)

SLAM_FORMATS = {
    "GentlemensWimbledonSingles": classic_slam_format_men,
    "MensFrenchOpen": classic_slam_format_men,
    "MensAustralianOpen": classic_slam_format_men,
    "MensUSOpen": us_open_format_men
}


def convert_to_boolean(score_str: str) -> List[bool]:
    """
    Converts the pbp string in Jeff Sackmann's dataset to a sequence of
    "True" and "False" for input into the parser.
    """

    flat_string = score_str.replace(';', '')
    flat_string = flat_string.replace('.', '')
    flat_string = flat_string.replace('A', 'S')
    flat_string = flat_string.replace('D', 'R')
    flat_string = flat_string.replace('/', '')
    assert(len(set(flat_string)) == 2)

    server_won = [x == 'S' for x in flat_string]

    return server_won


def load_sackmann_data(sackmann_csv_file: str,
                       discard_unusual_events: bool = True) -> pd.DataFrame:
    """
    Loads Jeff's data into a DataFrame.

    Args:
        sackmann_csv_file: Path to the csv with Jeff's data.
        discard_unusual_events: If True, discards Davis Cup, Hopman Cup,
            and Wildcard Playoffs [recommended].

    Returns:
        A DataFrame with the contents of the CSV.
    """

    data = pd.read_csv(sackmann_csv_file)
    data = data.reset_index()

    data['tny_name'] = data['tny_name'].str.replace('.html', '')
    data['tny_name'] = data['tny_name'].str.replace(r'\.$', '')
    data['tny_name'] = data['tny_name'].str.replace("'", '')

    data['date'] = pd.to_datetime(data['date'])

    if discard_unusual_events:
        data = data[~data.tny_name.str.contains(
            'DavisCup|Hopman|WildcardPlayoff|WildCardPlayoff')]

    return data


def process_match(first_server: str,
                  first_returner: str,
                  sackmann_str: str,
                  format_functions: FormatFunctions) \
        -> List[MatchState]:
    """
    Parses one match from Jeff's data.

    Args:
        first_server: The first server in the match.
        first_returner: The first returner in the match.
        sackmann_str: The coded string from Jeff's data.
        format_functions: The format of the match.

    Returns:
        A list of MatchStates, one for each point of the match.
    """

    win_loss = convert_to_boolean(sackmann_str)

    start_state = create_start_match_state(first_server, first_returner)

    result = process_win_loss_vector(win_loss, start_state, format_functions)

    return result


def validate_against_sackmann_score(final_match_state: MatchState,
                                    sackmann_score: str) -> bool:
    """
    Compares the parsed score against the one in Jeff's dataset.

    Args:
        final_match_state: The final parsed state.
        sackmann_score: The string score in Jeff's dataset.

    Returns:
        True if scores match, False if not.
    """

    matches_sack = (
        match_summary_string(final_match_state, score_only=True) ==
        sackmann_score)

    return matches_sack


def validate_all(sackmann_df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Checks all matches in the DataFrame against their parsed results.

    Args:
        sackmann_df: The loaded data.

    Returns:
        A list containing each match which did not parse in the same way as
        Jeff's parser, as a dictionary with fields "final_state", containing
        the final parsed state, and "match_tuple", containing Jeff's row
        in the DataFrame.
    """

    problematic_matches = list()

    for cur_match in sackmann_df.itertuples():

        if cur_match.tny_name in SLAM_FORMATS:
            cur_format = SLAM_FORMATS[cur_match.tny_name]
        else:
            cur_format = standard_best_of_three

        try:
            result = process_match(cur_match.server1, cur_match.server2,
                                   cur_match.pbp, cur_format)
        except AssertionError:

            matches_sack = False

            problematic_matches.append({
                'final_state': None,
                'match_tuple': cur_match
            })

            continue

        final_state = result[-1]

        matches_sack = validate_against_sackmann_score(
            final_state, cur_match.score)

        if not matches_sack:
            problematic_matches.append({
                'final_state': final_state,
                'match_tuple': cur_match
            })

    return problematic_matches
