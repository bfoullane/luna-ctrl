"""Automatic checks for the game rules. Run:  pip install pytest   then   pytest -v"""
import random
import pytest
from engine import DIFFICULTY, EVENTS, available, new_game, start_day, play_day

LEVELS = ["junior", "commander", "expert"]


def random_turn(g, r):
    evs = start_day(g)
    acts = r.sample(available(g), 2)
    choices = [r.choice(list(EVENTS[e]["options"])) for e in evs]
    play_day(g, acts, choices)


def test_levels_really_get_harder():
    d = [DIFFICULTY[lv] for lv in LEVELS]
    assert d[0]["events"] < d[1]["events"] < d[2]["events"]
    assert d[0]["storm"] < d[1]["storm"] < d[2]["storm"]
    assert d[0]["drain"] < d[1]["drain"] < d[2]["drain"]
    assert d[0]["timer"] > d[1]["timer"] > d[2]["timer"]
    assert d[0]["sun"] > 0 and d[1]["sun"] == d[2]["sun"] == 0


@pytest.mark.parametrize("level", LEVELS)
def test_each_day_has_the_promised_number_of_events(level):
    for day in range(1, 6):
        g = new_game(level, seed=1)
        g["day"] = day
        assert len(start_day(g)) == DIFFICULTY[level]["events"]


@pytest.mark.parametrize("level", LEVELS)
def test_every_game_ends_within_5_days_and_resources_stay_0_to_100(level):
    for seed in range(200):
        g, r = new_game(level, seed=seed), random.Random(seed)
        days = 0
        while not g["over"]:
            random_turn(g, r)
            days += 1
            assert all(0 <= g[k] <= 100 for k in ("power", "oxygen", "shield", "food"))
        assert days <= 5
        assert g["won"] == (days == 5 and min(g["power"], g["oxygen"], g["food"]) > 0)


def test_same_seed_gives_same_game():
    def play(seed):
        g, r = new_game("commander", seed=seed), random.Random(seed)
        while not g["over"]:
            random_turn(g, r)
        return g["won"], g["science"], g["day"]
    assert play(42) == play(42)