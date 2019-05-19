from typing import Tuple
from copy import deepcopy
from .match_state import MatchState, CompletedSet
from .format_functions import FormatFunctions


def player_wins_set(
        match_state: MatchState,
        winning_player: str,
        losing_player: str,
        format_functions: FormatFunctions) -> MatchState:
    """
    Advances the match state, taking into account that a player has just won
    a set.

    Args:
        match_state: The current state of the match.
        winning_player: Player who won the set.
        losing_player: Player who lost the set.
        format_functions: The functions encoding the match format.

    Returns:
        The updated MatchState.
    """

    match_state = deepcopy(match_state)

    match_state.sets_won[winning_player] += 1
    match_state.past_sets.append(
        CompletedSet(
            player_scores=match_state.cur_set_score,
            tiebreak_score=(match_state.cur_game_score if
                            match_state.is_tiebreak else None)
        ))

    if not format_functions.match_over_fun(
            match_state.sets_won[winning_player],
            match_state.sets_won[losing_player]):
        match_state.set_num += 1
        match_state.reset_set_score()
    else:
        match_state.is_over = True

    return match_state


def player_wins_game(match_state: MatchState,
                     winning_player: str,
                     losing_player: str,
                     format_functions: FormatFunctions) \
        -> MatchState:
    """
    Advances the match state, taking into account that a player has just won
    a game.

    Args:
        match_state: The current state of the match.
        winning_player: Player who won the game.
        losing_player: Player who lost the game.
        format_functions: The functions encoding the match format.

    Returns:
        The updated MatchState.
    """

    match_state = deepcopy(match_state)

    match_state.cur_set_score[winning_player] += 1
    match_state.total_games_played += 1

    # Set server and returner
    match_state.server, match_state.returner = \
        format_functions.roles_at_game_start(match_state.total_games_played,
                                             match_state.first_server,
                                             match_state.first_returner)

    is_final_set = format_functions.is_final_set(match_state.set_num)

    # Check whether player won the set
    if format_functions.set_win_condition(
            match_state.cur_set_score[winning_player],
            match_state.cur_set_score[losing_player], is_final_set):

        match_state = player_wins_set(match_state, winning_player,
                                      losing_player, format_functions)

    match_state.is_tiebreak = format_functions.is_tiebreak_fun(
        match_state.cur_set_score[winning_player],
        match_state.cur_set_score[losing_player],
        is_final_set)

    match_state.reset_game_score()

    return match_state


def advance_tiebreak(server_won: bool,
                     match_state: MatchState,
                     format_functions: FormatFunctions) -> MatchState:
    """
    Advances the tiebreak score, taking into account that the server has
    either just won or lost the point.

    Args:
        server_won: Whether or not the server won the point.
        match_state: The current state of the match.
        format_functions: The functions encoding the match format.

    Returns:
        The updated MatchState.
    """

    match_state = deepcopy(match_state)

    # Advance the game score
    if server_won:
        match_state.cur_game_score[match_state.server] += 1
    else:
        match_state.cur_game_score[match_state.returner] += 1

    if format_functions.tiebreak_over(
            match_state.cur_game_score[match_state.server],
            match_state.cur_game_score[match_state.returner],
            format_functions.is_final_set(match_state.set_num)):

        winning_player, losing_player = get_point_winner_loser(
            match_state.server, match_state.returner, server_won)

        match_state = player_wins_game(match_state, winning_player,
                                       losing_player, format_functions)

        return match_state

    total_points = sum(match_state.cur_game_score.values())
    start_server, start_returner = format_functions.roles_at_game_start(
        match_state.total_games_played, match_state.first_server,
        match_state.first_returner)

    # Otherwise, adjust who's serving
    match_state.server, match_state.returner = \
        format_functions.tiebreak_roles(total_points, start_server,
                                        start_returner)

    return match_state


def get_point_winner_loser(server: str, returner: str, server_won: bool) \
        -> Tuple[str, str]:
    """
    A simple utility function returning point winner and loser given whether
    the server or returner won.
    """

    winning_player, losing_player = (
        (server, returner) if server_won else (returner, server))

    return winning_player, losing_player


def advance_service_game(server_won: bool,
                         match_state: MatchState,
                         format_functions: FormatFunctions) \
        -> MatchState:
    """
    Advances the service game score, taking into account that the server has
    either just won or lost the point.

    Args:
        server_won: Whether or not the server won the point.
        match_state: The current state of the match.
        format_functions: The functions encoding the match format.

    Returns:
        The updated MatchState.
    """

    match_state = deepcopy(match_state)

    # Advance the game score
    if server_won:
        match_state.cur_game_score[match_state.server] += 1
    else:
        match_state.cur_game_score[match_state.returner] += 1

    # See whether the service game is over
    if format_functions.service_game_over(
            match_state.cur_game_score[match_state.server],
            match_state.cur_game_score[match_state.returner]):

        winning_player, losing_player = get_point_winner_loser(
            match_state.server, match_state.returner, server_won)

        match_state = player_wins_game(match_state, winning_player,
                                       losing_player, format_functions)

    return match_state
