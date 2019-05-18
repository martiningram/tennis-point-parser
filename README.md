# Format parser for tennis

### Requirements

* python 3.7+
* pandas

### Motivation

A compact way to store the point-by-point data of a tennis match is to store a
Boolean vector of "True" and "False", listing whether the server won each point,
or lost it. While compact, this form isn't particularly useful for analysis.

This repository's main purpose is to provide code to easily take such a sequence
of True and False and turn it into a list of match states.

For example, the 2017 match at the Miami Open between Federer and Nadal can be
represented as:

```python
sequence = [True, False, False, True, False, True, False, True, True, True,
True, False, True, True, False, True, False, True, True, True, True, False,
False, True, True, False, True, False, True, True, True, True, True, False,
True, False, False, False, True, True, True, False, True, True, False, False,
True, True, True, True, True, False, False, False, True, True, True, True,
False, False, True, False, True, False, True, False, False, True, False, True,
True, True, True, True, False, True, True, True, True, True, True, True, False,
True, True, False, True, True, True, True, True, True, True, True, True, True,
True, True, True, True, False, True, False, False, True, False, True, True,
True, False, True, True, False, True, True, False, True, True, False, False,
False, False, True, True, False, True, True]
```

Together with the knowledge that Federer served first, and that this is a
best-of-three match, we can recover the score sequence, for example:

```
Roger Federer - Rafael Nadal: 0-0 15:0
Roger Federer - Rafael Nadal: 0-0 15:15
Roger Federer - Rafael Nadal: 0-0 15:30
...
Roger Federer - Rafael Nadal: 6-3 6-4
```

We can use this package to do this job. Here's how it works:

```python
import point_parser.formats as fmts
import point_parser.parse as p
import point_parser.utils as utils

states = process_win_loss_vector(
    sequence,
    utils.create_start_match_state('Roger Federer', 'Rafael Nadal'),
    fmts.standard_best_of_three
)
```

The function takes three arguments:

* `sequence`, the boolean vector defined above
* `match_state`, which is the starting match state. More on match states below.
* `format_functions`, which encode the rules of the format, such as whether it
  is best of three, best of five, has a tiebreak, and so on.

It will return a list of MatchStates. To get the score sequence printouts above,
we can run:

```python
for cur_state in states:
  print(utils.match_summary_string(cur_state))
```

Each MatchState contains information about the current score of the match. For
example, after the first point, it reads:

```
MatchState(server='Roger Federer', returner='Rafael Nadal', is_tiebreak=False,
first_server='Roger Federer', first_returner='Rafael Nadal', set_num=0,
total_games_played=0, cur_set_score={'Roger Federer': 0, 'Rafael Nadal': 0},
cur_game_score={'Roger Federer': 1, 'Rafael Nadal': 0}, sets_won={'Roger
Federer': 0, 'Rafael Nadal': 0}, past_sets=[], is_over=False)
```

The list of match states could then be used to extract more information about
the match, such as the number of break points.

### Installation

Please run `python setup.py develop` to install the package.
