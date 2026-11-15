import random
from events import load_days

DAYS = list(load_days().values())[:5]          # 8-12 May 2024, real DONKI

ACTIONS = {
    "oxygen":  {"label": "Make oxygen",        "fx": {"oxygen": 20, "power": -20}, "from": 1},
    "solar":   {"label": "Clean solar panels", "fx": {"power": 25, "oxygen": -8},  "from": 1},
    "shield":  {"label": "Reinforce shield",   "fx": {"shield": 20, "power": -15}, "from": 2},
    "garden":  {"label": "Tend the garden",    "fx": {"food": 20, "power": -10, "oxygen": -5}, "from": 3},
    "science": {"label": "Do science",         "fx": {"science": 10, "power": -10, "oxygen": -10}, "from": 1},
}
DRAIN = {"power": -5, "oxygen": -6, "shield": -3}

DIFFICULTY = {
    "junior":    {"events": 2, "storm": 0.8, "drain": 0.8, "sun": 18, "timer": None},
    "commander": {"events": 3, "storm": 1.0, "drain": 1.0, "sun": 0, "timer": 10},
    "expert":    {"events": 4, "storm": 1.3, "drain": 1.2, "sun": 0, "timer": 8},
}

MAIN = {1: "dust", 2: "flare", 3: "garden", 4: "advice", 5: "air"}
UNLOCK = {1: {"power", "life"}, 2: {"power", "life", "shield"},
          3: {"power", "life", "shield", "food"},
          4: {"power", "life", "shield", "food", "comms"},
          5: {"power", "life", "shield", "food", "comms"}}

EVENTS = {
 "dust": {"factor": "power", "title": "Dust storm at dusk",
   "text": "Moon dust is about to bury your solar panels.",
   "options": {
     "retract": {"label": "Retract the panels", "now": {"power": -15},
                 "note": "Switching things off protects them, but you make no power."},
     "stay": {"label": "Stay exposed", "now": {"power": 10},
              "risk": (0.5, {"panel": -30}),
              "note": "You kept making power, but dust can scratch panels for good."}}},
 "night": {"factor": "power", "title": "Lunar night is coming",
   "text": "Soon there will be no sunlight for two weeks. Batteries must last.",
   "options": {
     "save": {"label": "Switch off the lab", "now": {"power": 15},
              "note": "Batteries are fuller, but you gave up research."},
     "work": {"label": "Keep the lab on", "now": {"power": -10, "science": 10},
              "note": "Science points earned, but the batteries took the hit."}}},
 "air": {"factor": "life", "title": "The air machine is struggling",
   "text": "Dust and stress made your oxygen machine run poorly.",
   "options": {
     "repair": {"label": "Repair it now", "now": {"oxygen": 25, "power": -25},
                "note": "Life support is fixed, but repairs cost a lot of energy."},
     "limp": {"label": "Keep it running as is", "now": {"oxygen": -12, "power": 5},
              "note": "You saved power, but air is running out. Astronauts never gamble with air."}}},
 "co2": {"factor": "life", "title": "The air filter is full",
   "text": "Your breath adds carbon dioxide. The filter must be swapped.",
   "options": {
     "swap": {"label": "Swap the filter", "now": {"oxygen": 10, "power": -10, "food": -5},
              "note": "Clean air, but it took power and crew time."},
     "ignore": {"label": "Do it later", "now": {"oxygen": -15},
                "note": "Dirty air makes the crew tired and the oxygen drops."}}},
 "flare": {"factor": "shield", "title": "Flare warning",
   "text": "A strong flare just erupted. Radiation is coming.",
   "options": {
     "build": {"label": "Spend power on the shield", "now": {"power": -20, "shield": 25},
               "note": "Shielding is bought with energy."},
     "keep": {"label": "Save power for air", "now": {"oxygen": 10},
              "note": "Air is safe, but the shield stays thin."}}},
 "particles": {"factor": "shield", "title": "Radiation alert",
   "text": "Fast particles from the Sun are reaching the Moon.",
   "options": {
     "shelter": {"label": "Crew shelters in the storm room", "now": {"shield": 10, "science": -5},
                 "note": "The crew is safer, but research stops."},
     "work": {"label": "Keep working", "now": {"science": 10, "shield": -10},
              "note": "Science continues, but the crew gets more radiation."}}},
 "garden": {"factor": "food", "title": "Water the garden?",
   "text": "Radiation stresses your plants. Lights and water cost power.",
   "options": {
     "water": {"label": "Water the plants", "now": {"food": 20, "power": -10},
               "note": "Food costs energy to grow."},
     "skip": {"label": "Save the power", "now": {"food": -10},
              "note": "Power saved today, hungrier tomorrow."}}},
 "harvest": {"factor": "food", "title": "Harvest time",
   "text": "Some plants are almost ready.",
   "options": {
     "early": {"label": "Harvest now", "now": {"food": 10, "power": -5},
               "note": "A smaller harvest, but food is safe."},
     "wait": {"label": "Wait two more days", "now": {"food": -5, "power": 5},
              "note": "A bigger harvest later, but a risky wait."}}},
 "advice": {"factor": "comms", "title": "Earth's advice is late",
   "text": "Earth is sending advice, but messages take time. The storm peaks now.",
   "options": {
     "act": {"label": "Decide on your own", "now": {"power": -15, "shield": 25},
             "note": "Astronauts must act without waiting for orders."},
     "wait": {"label": "Wait for Earth", "after": {"shield": 10},
              "note": "Earth's advice arrived after the storm hit."}}},
 "blackout": {"factor": "comms", "title": "Radio blackout",
   "text": "The storm is jamming the radio. Earth can't hear you.",
   "options": {
     "old": {"label": "Follow the old plan", "now": {"power": -10},
             "note": "The old plan didn't fit the storm."},
     "new": {"label": "Make a new plan yourself", "now": {"oxygen": -8, "shield": 10},
             "note": "You adapted, which costs effort."}}},
}

def clamp(v): return max(0, min(100, round(v)))

def new_game(level="commander", seed=None):
    return {"day": 1, "level": level, "power": 70, "oxygen": 70, "shield": 50,
            "food": 60, "science": 0, "panel": 100, "over": False, "won": False,
            "rng": random.Random(seed), "history": [], "today": []}

def available(state):
    return [k for k, a in ACTIONS.items() if a["from"] <= state["day"]]

def start_day(state):
    d = state["day"]
    pool = [k for k, e in EVENTS.items() if e["factor"] in UNLOCK[d] and k != MAIN[d]]
    n = DIFFICULTY[state["level"]]["events"] - 1
    state["today"] = [MAIN[d]] + state["rng"].sample(pool, min(n, len(pool)))
    return state["today"]

def fx(state, effects):
    for k, v in effects.items():
        if k == "science":
            state["science"] = max(0, state["science"] + v)
        else:
            state[k] = clamp(state[k] + v)

def play_day(state, actions, choices):
    cfg = DIFFICULTY[state["level"]]
    rep, afters, day = [], [], state["day"]
    sun = round(cfg["sun"] * state["panel"] / 100)                    # morning sunshine on the panels
    fx(state, {"power": sun})
    if sun:
        rep.append(f"Sunshine: your panels made {sun} power this morning."
                   + (" Damaged panels make less." if state["panel"] < 100 else ""))
    for a in actions:
        e = dict(ACTIONS[a]["fx"])
        if a == "solar":
            e["power"] = round(e["power"] * state["panel"] / 100)
        fx(state, e)
    for ev_id, ch in zip(state["today"], choices):
        opt = EVENTS[ev_id]["options"][ch]
        fx(state, opt.get("now", {}))
        rep.append(f"{EVENTS[ev_id]['title']}: {opt['note']}")
        if ev_id == "air" and ch == "repair" and state["panel"] < 70:
            fx(state, {"power": -10})
            rep.append("Your damaged panels made the repair cost extra power.")
        if "risk" in opt and state["rng"].random() < opt["risk"][0]:
            fx(state, opt["risk"][1])
            rep.append("Unlucky: dust damaged your panels. They make less power now.")
        afters.append(opt.get("after", {}))
    fx(state, {k: round(v * cfg["drain"]) for k, v in DRAIN.items()})
    if day >= 3:
        fx(state, {"food": -5})
    d = DAYS[day - 1]
    strength = round(d["strength"] * cfg["storm"])
    if state["shield"] < strength:
        hit = strength - state["shield"]
        fx(state, {"power": -(hit // 2)})
        if day >= 3:
            fx(state, {"food": -(hit // 4)})
        rep.append(f"Storm hit! Real flare {d['max_class']}. Weak shield cost {hit // 2} power.")
    else:
        rep.append(f"Storm blocked. Real flare {d['max_class']}. The shield held.")
    for a in afters:
        fx(state, a)
    state["history"].append((day, actions, choices))
    state["day"] += 1
    if min(state["power"], state["oxygen"], state["food"]) <= 0 and day >= 3 or min(state["power"], state["oxygen"]) <= 0:
        state["over"] = True
    elif state["day"] > 5:
        state["over"], state["won"] = True, True
    return rep