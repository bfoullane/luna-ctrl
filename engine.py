import random
from events import load_days

DAYS = list(load_days().values())[:5]          # 8-12 May 2024, real DONKI

ACTIONS = {
    "oxygen":  {"label": "Make oxygen",        "icon": "💨", "fx": {"oxygen": 20, "power": -20}, "from": 1,
                "desc": "Run the water-splitter to pump fresh breathable air into the habitat."},
    "solar":   {"label": "Clean solar panels", "icon": "☀️", "fx": {"power": 25, "oxygen": -8},  "from": 1,
                "desc": "Brush sharp Moon dust off the panels so they catch maximum sunlight."},
    "shield":  {"label": "Reinforce shield",   "icon": "🛡️", "fx": {"shield": 20, "power": -15}, "from": 2,
                "desc": "Charge the magnetic deflector field before solar radiation arrives."},
    "garden":  {"label": "Tend the garden",    "icon": "🌱", "fx": {"food": 20, "power": -10, "oxygen": -5}, "from": 3,
                "desc": "Feed and water the greenhouse crops growing under LED grow-lights."},
    "science": {"label": "Do science",         "icon": "🔬", "fx": {"science": 10, "power": -10, "oxygen": -10}, "from": 1,
                "desc": "Study Moon rocks and solar weather data to earn mission points."},
}
DRAIN = {"power": -5, "oxygen": -6, "shield": -3}

DIFFICULTY = {
    "junior":    {"events": 2, "storm": 0.8, "drain": 0.8, "sun": 18, "timer": 20},
    "commander": {"events": 3, "storm": 1.0, "drain": 1.0, "sun": 0,  "timer": 12},
    "expert":    {"events": 4, "storm": 1.3, "drain": 1.2, "sun": 0,  "timer": 8},
}

MAIN = {1: "dust", 2: "flare", 3: "garden", 4: "advice", 5: "air"}
UNLOCK = {1: {"power", "life"}, 2: {"power", "life", "shield"},
          3: {"power", "life", "shield", "food"},
          4: {"power", "life", "shield", "food", "comms"},
          5: {"power", "life", "shield", "food", "comms"}}

DAY_FACTS = {
    1: {
        "unlock": "⚡ Power & 💨 Air Systems Online",
        "fact": "On the Moon there is no air to breathe and no wind. Solar panels make electricity from sunlight, and machines use that electricity to make oxygen!"
    },
    2: {
        "unlock": "🛡️ Radiation Shield Unlocked",
        "fact": "Earth has a thick atmosphere and magnetic bubble that block solar storms. The Moon has neither—so Moon bases need special shields to keep astronauts safe."
    },
    3: {
        "unlock": "🌱 Space Garden Unlocked",
        "fact": "Shipping food from Earth costs thousands of dollars per apple! Astronauts grow leafy greens and veggies in space gardens using LED lights and recycled water."
    },
    4: {
        "unlock": "📡 Earth-Moon Comms Unlocked",
        "fact": "On 11 May 2024, the Sun fired a giant X5.8 flare—one of the strongest in years! Radio signals between Earth and the Moon travel at light speed, taking about 1.3 seconds each way."
    },
    5: {
        "unlock": "🚀 Final Day: All Systems Active",
        "fact": "Real NASA flight controllers have to balance power, air, shielding, food, and communications all at once—just like you are doing today!"
    },
}

EVENTS = {
 "dust": {
   "factor": "power", "title": "Dust storm at dusk",
   "text": "Swirling Moon dust is about to cover your solar panels.",
   "did_you_know": "Moon dust isn't soft like beach sand! Because there is no wind or water on the Moon to smooth it down, every grain is sharp like tiny glass.",
   "options": {
     "retract": {
       "label": "Retract the panels", "now": {"power": -15}, "safe": True,
       "note": "Closing the panels kept them safe from scratches, but they couldn't make power.",
       "explain": "Just like closing your eyes in a sandstorm, folding the panels protects the glass—even though you lose electricity while they are closed."
     },
     "stay": {
       "label": "Stay exposed", "now": {"power": 10},
       "risk": (0.5, {"panel": -30}),
       "note": "You kept making power, but sharp dust can scratch panels for good.",
       "explain": "Leaving panels open keeps electricity flowing right now, but gritty lunar dust can permanently scratch the surface so they make less power later."
     }
   }
 },
 "night": {
   "factor": "power", "title": "Lunar night is coming",
   "text": "Soon there will be no sunlight for two weeks. Batteries must last.",
   "did_you_know": "One day-and-night cycle on the Moon lasts almost an entire Earth month—14 days of bright sunshine followed by 14 days of freezing darkness!",
   "options": {
     "save": {
       "label": "Switch off the lab", "now": {"power": 15}, "safe": True,
       "note": "Batteries are fuller, though science experiments paused.",
       "explain": "Turning off non-essential lab machines saves battery energy for life support when the sun goes down."
     },
     "work": {
       "label": "Keep the lab on", "now": {"power": -10, "science": 10},
       "note": "Science points earned, but the batteries took a hit.",
       "explain": "Running science instruments uses extra battery power, leaving a smaller energy cushion for the dark lunar night."
     }
   }
 },
 "air": {
   "factor": "life", "title": "The air machine is struggling",
   "text": "Dust and heavy use made your oxygen generator run poorly.",
   "did_you_know": "On the International Space Station and future Moon bases, astronauts make oxygen from water using electricity—a process called electrolysis!",
   "options": {
     "repair": {
       "label": "Repair it now", "now": {"oxygen": 25, "power": -25}, "safe": True,
       "note": "Life support is fixed and pumping fresh air, though repairs took lots of power.",
       "explain": "Fixing the oxygen generator right away uses heavy power tools, but guarantees the crew always has plenty of air to breathe."
     },
     "limp": {
       "label": "Keep it running as is", "now": {"oxygen": -12, "power": 5},
       "note": "You saved power, but air levels dropped. Astronauts never gamble with air!",
       "explain": "Putting off repairs saves electricity today, but a struggling machine leaks air faster than it replaces it."
     }
   }
 },
 "co2": {
   "factor": "life", "title": "The air filter is full",
   "text": "Every breath adds carbon dioxide to the cabin. The filter needs swapping.",
   "did_you_know": "When you breathe out, you release carbon dioxide (CO2). In a sealed spacecraft, special scrubbers trap CO2 so the air stays fresh and safe.",
   "options": {
     "swap": {
       "label": "Swap the filter", "now": {"oxygen": 10, "power": -10, "food": -5}, "safe": True,
       "note": "Clean, fresh air restored—though the crew spent time and power doing it.",
       "explain": "Installing a clean filter immediately clears out stale air, costing a bit of power and crew energy."
     },
     "ignore": {
       "label": "Do it later", "now": {"oxygen": -15},
       "note": "Stale air made the crew sluggish and breathable oxygen dropped.",
       "explain": "When a filter is clogged, carbon dioxide builds up inside the dome and lowers the quality of breathable air."
     }
   }
 },
 "flare": {
   "factor": "shield", "title": "Flare warning",
   "text": "A bright solar flare just erupted on the Sun! Radiation is heading toward the Moon.",
   "did_you_know": "Solar flares are giant explosions on the Sun that travel at the speed of light—reaching the Moon in just 8 minutes!",
   "options": {
     "build": {
       "label": "Spend power on the shield", "now": {"power": -20, "shield": 25}, "safe": True,
       "note": "Shielding boosted using base electricity.",
       "explain": "Active radiation shields work like an invisible magnetic umbrella—the more power you feed them, the stronger they block solar particles."
     },
     "keep": {
       "label": "Save power for air", "now": {"oxygen": 10},
       "note": "Air reserves are topped up, but the radiation shield stayed thin.",
       "explain": "Keeping power in life support protects your oxygen supply, but leaves the base less protected when the flare hits."
     }
   }
 },
 "particles": {
   "factor": "shield", "title": "Radiation alert",
   "text": "Fast-moving particles from the Sun are sweeping across the lunar surface.",
   "did_you_know": "Real Moon habitats will use thick layers of lunar soil (called regolith) and water tanks around the walls to block space radiation!",
   "options": {
     "shelter": {
       "label": "Crew shelters in storm room", "now": {"shield": 10, "science": -5}, "safe": True,
       "note": "The crew is safely tucked inside the storm shelter, pausing experiments.",
       "explain": "Moving inside the heavily shielded inner room protects the astronauts, even if outside science work has to wait."
     },
     "work": {
       "label": "Keep working", "now": {"science": 10, "shield": -10},
       "note": "Science continued, but the crew took extra radiation exposure.",
       "explain": "Staying at exposed workstations earns research data, but weakens your overall radiation protection."
     }
   }
 },
 "garden": {
   "factor": "food", "title": "Water the garden?",
   "text": "Solar heat and radiation are stressing your plants. Lights and pumps need power.",
   "did_you_know": "NASA astronauts have already grown zinnia flowers, radishes, and red romaine lettuce in space aboard the space station!",
   "options": {
     "water": {
       "label": "Water the plants", "now": {"food": 20, "power": -10}, "safe": True,
       "note": "Healthy crops boosted your food supply using greenhouse power.",
       "explain": "Water pumps and pink LED grow-lights need electricity, but healthy plants reward the crew with fresh food."
     },
     "skip": {
       "label": "Save the power", "now": {"food": -10},
       "note": "Electricity saved today, but thirsty plants produced less food.",
       "explain": "Turning off greenhouse pumps saves battery power right away, but crops wilt quickly without steady water."
     }
   }
 },
 "harvest": {
   "factor": "food", "title": "Harvest time",
   "text": "Your space veggies are almost ripe, while a solar storm approaches.",
   "did_you_know": "Plants in space don't just make food—their leaves also absorb carbon dioxide and release fresh oxygen!",
   "options": {
     "early": {
       "label": "Harvest now", "now": {"food": 10, "power": -5}, "safe": True,
       "note": "A smaller harvest, safely stored in the pantry before the storm.",
       "explain": "Picking crops early gives slightly smaller veggies, but locks the food safely inside storage."
     },
     "wait": {
       "label": "Wait two more days", "now": {"food": -5, "power": 5},
       "note": "Waiting saved power now, though hungry crew dipped into rations.",
       "explain": "Leaving crops to grow longer saves harvest energy today, but reduces ready-to-eat food right now."
     }
   }
 },
 "advice": {
   "factor": "comms", "title": "Earth's advice is late",
   "text": "Mission Control is sending instructions, but the storm is peaking right now.",
   "did_you_know": "The Moon is about 384,400 km (238,855 miles) from Earth—far enough to fit 30 Earths in between!",
   "options": {
     "act": {
       "label": "Decide on your own", "now": {"power": -15, "shield": 25}, "safe": True,
       "note": "You acted fast and powered up the shield before the peak hit!",
       "explain": "Astronaut commanders are trained to make smart decisions independently when Mission Control messages are delayed."
     },
     "wait": {
       "label": "Wait for Earth", "after": {"shield": 10},
       "note": "Earth's message arrived after the storm had already hit.",
       "explain": "Waiting for instructions saved power during the storm, so the shield boost arrived too late to block the peak."
     }
   }
 },
 "blackout": {
   "factor": "comms", "title": "Radio blackout",
   "text": "Solar static is jamming the radio dish. Earth can't hear your call.",
   "did_you_know": "Strong solar flares ionize the upper atmosphere and fill space with radio noise, causing real radio blackouts on Earth and the Moon!",
   "options": {
     "new": {
       "label": "Make a new plan yourself", "now": {"oxygen": -8, "shield": 10}, "safe": True,
       "note": "You adapted quickly to the storm, though the crew worked extra hard.",
       "explain": "Rewriting the schedule on the fly takes extra crew breathing effort, but points the shield right where it's needed."
     },
     "old": {
       "label": "Follow the old plan", "now": {"power": -10},
       "note": "Yesterday's schedule didn't match today's storm and wasted power.",
       "explain": "Sticking to an outdated plan when space weather changes wastes energy on the wrong systems."
     }
   }
 },
}


def clamp(v):
    return max(0, min(100, round(v)))


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


def resolve_morning(state):
    cfg = DIFFICULTY[state["level"]]
    sun = round(cfg["sun"] * state["panel"] / 100)
    fx(state, {"power": sun})
    if sun:
        msg = f"Sunshine: your solar panels made +{sun} Power this morning."
        if state["panel"] < 100:
            msg += " (Scratched panels make a bit less.)"
        return sun, msg
    return 0, "No bonus morning sunshine at this difficulty—manage your batteries carefully!"


def resolve_event(state, ev_id, ch):
    opt = EVENTS[ev_id]["options"][ch]
    before = {k: state[k] for k in ("power", "oxygen", "shield", "food", "science", "panel")}
    fx(state, opt.get("now", {}))
    extra = []
    if ev_id == "air" and ch == "repair" and state["panel"] < 70:
        fx(state, {"power": -10})
        extra.append("Your scratched solar panels made the repair cost 10 extra Power.")
    if "risk" in opt and state["rng"].random() < opt["risk"][0]:
        fx(state, opt["risk"][1])
        extra.append("Oh no! Sharp Moon dust scratched your solar panels (-30% panel health).")
    after = {k: state[k] for k in ("power", "oxygen", "shield", "food", "science", "panel")}
    deltas = {k: after[k] - before[k] for k in after if after[k] != before[k]}
    return {
        "ev_id": ev_id,
        "choice": ch,
        "note": opt["note"],
        "explain": opt["explain"],
        "did_you_know": EVENTS[ev_id]["did_you_know"],
        "deltas": deltas,
        "extra": extra,
        "after_fx": opt.get("after", {}),
    }


def resolve_end_of_day(state, actions, event_records):
    cfg = DIFFICULTY[state["level"]]
    day = state["day"]
    rep = []
    for a in actions:
        e = dict(ACTIONS[a]["fx"])
        if a == "solar":
            e["power"] = round(e["power"] * state["panel"] / 100)
        fx(state, e)
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
        rep.append(f"Storm hit! Real flare {d['max_class']}. Weak shield cost {hit // 2} Power.")
    else:
        rep.append(f"Storm blocked! Real flare {d['max_class']}. Your shield held strong.")
    for rec in event_records:
        if rec["after_fx"]:
            fx(state, rec["after_fx"])
            rep.append(f"{EVENTS[rec['ev_id']]['title']}: delayed Earth advice arrived (+10 Shield).")
    state["history"].append((day, actions, [r["choice"] for r in event_records]))
    state["day"] += 1
    if (min(state["power"], state["oxygen"], state["food"]) <= 0 and day >= 3) or min(state["power"], state["oxygen"]) <= 0:
        state["over"] = True
    elif state["day"] > 5:
        state["over"], state["won"] = True, True
    return rep
def play_day(state, actions, choices):
    """Shortcut for tests: runs one day with the SAME rules as the real game screen."""
    rep = [resolve_morning(state)[1]]
    records = []
    for ev_id, ch in zip(state["today"], choices):
        rec = resolve_event(state, ev_id, ch)
        rep.append(f"{EVENTS[ev_id]['title']}: {rec['note']}")
        rep += rec["extra"]
        records.append(rec)
    return rep + resolve_end_of_day(state, actions, records)