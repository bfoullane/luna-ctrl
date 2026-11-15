"""Plays thousands of Junior games with 4 kinds of players and prints win rates.
Run:  python balance_test.py        (needs data/donki_archive.json)
Goal for Junior: careful players win ~90%, random players ~50%, reckless players rarely."""
import random
from collections import Counter
from engine import EVENTS, available, new_game, start_day, play_day


def random_player(g, evs, r):
    return r.sample(available(g), 2), [r.choice(list(EVENTS[e]["options"])) for e in evs]


def careful_player(g, evs, r):
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
    return ["science", "oxygen"], [r.choice(list(EVENTS[e]["options"])) for e in evs]


def run(policy, level="junior", n=2000):
    wins, deaths, sci = 0, Counter(), []
    for seed in range(n):
        g, r = new_game(level, seed=seed), random.Random(seed + 99)
        while not g["over"]:
            evs = start_day(g)
            acts, ch = policy(g, evs, r)
            play_day(g, acts, ch)
        wins += g["won"]
        sci.append(g["science"])
        if not g["won"]: deaths[g["day"] - 1] += 1
    return wins / n, dict(sorted(deaths.items())), sum(sci) / n


if __name__ == "__main__":
    for name, p in (("random", random_player), ("careful", careful_player), ("reckless", reckless_player)):
        w, d, s = run(p)
        print(f"{name:9} wins {w:5.0%}   avg science {s:4.1f}   lost on day: {d}")