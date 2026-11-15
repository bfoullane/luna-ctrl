"""Balance test: plays thousands of games per level with 3 kinds of players and prints win rates.

Run:
    python balance_test.py                 # all levels, 2000 games each, UI rules
    python balance_test.py junior          # one level
    python balance_test.py all 5000        # all levels, 5000 games each
    python balance_test.py all 2000 test   # use play_day() instead of the UI rules

Needs data/donki_archive.json (run nasa_data.py once to create it).
Goal for Junior: careful players win ~90%, random players ~50%, reckless players rarely.
Commander and Expert should show clearly LOWER win rates than Junior for the same players.
"""
import random
import sys
from collections import Counter

from engine import (EVENTS, DIFFICULTY, available, new_game, start_day, play_day,
                    resolve_morning, resolve_event, resolve_end_of_day)


# ---------- the three kinds of players ----------

def random_player(g, evs, r):
    """Picks 2 random actions and a random option for every event."""
    return r.sample(available(g), 2), [r.choice(list(EVENTS[e]["options"])) for e in evs]


def careful_player(g, evs, r):
    """Picks the event option with the best resource effect (80% of the time) and fixes the weakest resource."""
    ch = []
    for e in evs:
        opts = EVENTS[e]["options"]
        score = lambda o: sum(v for k, v in {**opts[o].get("now", {}), **opts[o].get("after", {})}.items()
                              if k in ("power", "oxygen", "shield", "food"))
        ch.append(max(opts, key=score) if r.random() < .8 else r.choice(list(opts)))
    a = []
    if g["oxygen"] < g["power"] or g["oxygen"] < 50: a.append("oxygen")
    if g["power"] < 60: a.append("solar")
    if g["day"] >= 2 and g["shield"] < 50 and len(a) < 2: a.append("shield")
    if g["day"] >= 3 and g["food"] < 40 and len(a) < 2: a.append("garden")
    for x in ("science", "solar", "oxygen"):
        if len(a) < 2 and x not in a: a.append(x)
    return a[:2], ch


def reckless_player(g, evs, r):
    """Always does science and oxygen, and picks random event options."""
    return ["science", "oxygen"], [r.choice(list(EVENTS[e]["options"])) for e in evs]


# ---------- two ways to play one day ----------

def play_one_day_ui(g, policy, r):
    """Same order of steps as the real game screen: morning sun, events, then actions and storm."""
    evs = start_day(g)
    resolve_morning(g)
    acts, ch = policy(g, evs, r)
    records = [resolve_event(g, ev, c) for ev, c in zip(evs, ch)]
    resolve_end_of_day(g, acts, records)


def play_one_day_test(g, policy, r):
    """Uses play_day(), the shortcut used by test_engine.py."""
    evs = start_day(g)
    acts, ch = policy(g, evs, r)
    play_day(g, acts, ch)


# ---------- the simulation ----------

def run(policy, level="junior", n=2000, mode="ui"):
    play = play_one_day_ui if mode == "ui" else play_one_day_test
    wins, deaths, sci = 0, Counter(), []
    for seed in range(n):
        g, r = new_game(level, seed=seed), random.Random(seed + 99)
        while not g["over"]:
            play(g, policy, r)
        wins += g["won"]
        sci.append(g["science"])
        if not g["won"]:
            deaths[g["day"] - 1] += 1
    return wins / n, dict(sorted(deaths.items())), sum(sci) / n


PLAYERS = (("random", random_player), ("careful", careful_player), ("reckless", reckless_player))


def main():
    arg = sys.argv[1].lower() if len(sys.argv) > 1 else "all"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    mode = "test" if len(sys.argv) > 3 and sys.argv[3].lower() == "test" else "ui"
    levels = list(DIFFICULTY) if arg == "all" else [arg]
    for lv in levels:
        if lv not in DIFFICULTY:
            sys.exit(f"Unknown level '{lv}'. Choose from: {', '.join(DIFFICULTY)} or all.")

    print(f"{n} games per player type, rules: {'real game screen' if mode == 'ui' else 'play_day()'}")
    summary = {}
    for lv in levels:
        print(f"\n=== {lv.upper()} ===")
        for name, policy in PLAYERS:
            w, d, s = run(policy, lv, n, mode)
            summary[(lv, name)] = w
            print(f"{name:9} wins {w:5.0%}   avg science {s:4.1f}   lost on day: {d}")

    if len(levels) > 1:
        print("\n=== WIN RATE SUMMARY ===")
        print(f"{'player':9} " + "  ".join(f"{lv:>9}" for lv in levels))
        for name, _ in PLAYERS:
            print(f"{name:9} " + "  ".join(f"{summary[(lv, name)]:9.0%}" for lv in levels))


if __name__ == "__main__":
    main()