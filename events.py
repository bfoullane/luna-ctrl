import json
from collections import defaultdict
from pathlib import Path

def rank(c):
    return ("ABCMX".index(c[0]), float(c[1:]))

def storm_strength(c):
    letter, num = c[0], float(c[1:])
    if letter == "X":
        return min(70, round(30 + 6 * num))
    if letter == "M":
        return round(15 + num)
    return 5

def load_days(path=Path(__file__).parent / "data" / "donki_archive.json"):
    data = json.load(open(path))
    days = defaultdict(lambda: {"flares": 0, "x_flares": 0, "max_class": "B0"})
    for f in data["FLR"]:
        d = f["beginTime"][:10]
        c = f["classType"]
        days[d]["flares"] += 1
        days[d]["x_flares"] += c.startswith("X")
        if rank(c) > rank(days[d]["max_class"]):
            days[d]["max_class"] = c
    for d in days:
        days[d]["strength"] = storm_strength(days[d]["max_class"])
    return dict(sorted(days.items()))

if __name__ == "__main__":
    for d, v in load_days().items():
        print(d, v)