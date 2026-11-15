# LUNA-CTRL

**A 5-day Moon base survival game for kids aged 7 to 12, powered by a real NASA solar storm.**

Built for the NASA Space Apps Challenge 2026: *Build a Junior Astronaut Mission Trainer*.

**Play it online:** [ADD STREAMLIT LINK HERE]
**Demo video:** [ADD VIDEO LINK HERE]

<!-- Add 2 or 3 screenshots here: home screen, a day screen, the consequences screen -->

## The idea

You are the commander of a small Moon base. For five Moon days you keep your crew alive while the Sun throws a real storm at you. Every choice costs something: power spent on the shield is power you can't spend on air. That is the real engineering trade-off NASA mission planners face, and the game lets kids feel it instead of reading about it.

## How it works

Each day:

1. **See the real event.** A banner shows what the Sun actually did on that date.
2. **Handle the day's events.** Each event is a choice between two options, and neither is free.
3. **Pick 2 actions** to spend your limited resources.
4. **End the day.** The storm hits, and you see what your choices caused.
5. **Read the consequences.** A cause-and-effect chain explains what happened and why.

You lose if power or air runs out. You win by surviving all five days, and your score is the science you collected.

### The five factors

| Factor | What it means in the game | The trade-off |
|---|---|---|
| Power | Electricity from solar panels | Everything else runs on it |
| Life support | The air your crew breathes | The oxygen machine costs power |
| Radiation shielding | The base's wall against Sun radiation | Reinforcing it costs power |
| Food production | The garden | Lights and water cost power and air |
| Communication delay | Earth's advice arrives late | Wait for orders, or act on your own |

One new factor unlocks each day, so young players learn one idea at a time. By day 5 all five can hit at once.

### The five days

| Day | Date (real) | New factor | Headline event |
|---|---|---|---|
| 1 | 8 May 2024 | Power and life support | Dust storm at dusk |
| 2 | 9 May 2024 | Shielding | Flare warning |
| 3 | 10 May 2024 | Food | Water the garden? |
| 4 | 11 May 2024 | Communication delay | Earth's advice is late |
| 5 | 12 May 2024 | Everything together | The air machine is struggling |

Extra events are drawn at random each game, so every playthrough is different.

### Difficulty levels
| Level | Audience | Events a day | Storm strength | Daily drain | Morning sunshine | Timer |
|---|---|---|---|---|---|---|
| Junior | Ages 7 to 9 | 2 | ×0.8 | ×0.8 | +18 power | 20 s |
| Commander | Ages 10 to 12 | 3 | ×1.0 | ×1.0 | none | 12 s |
| Expert | Older siblings and parents | 4 | ×1.3 | ×1.2 | none | 8 s |

## Real NASA data and what is simulated

| Real | Simulated |
|---|---|
| Solar flare dates, times and classes (X, M, C, B) for the storm period, which drive the daily storm strength | Dust storms, repairs and garden events |
| | All resource numbers and costs |
| | How strong a flare is *in game points* (our own balancing scale) |
| | The Earth message delay (exaggerated for gameplay; the real Earth-Moon delay is about 1.3 seconds) |

The game uses **archived** DONKI data saved in `data/donki_archive.json`. It is not presented as live data. The archive covers 8 to 13 May 2024 and includes flare (FLR), coronal mass ejection (CME) and geomagnetic storm (GST) records. The game currently uses the flare records; the five game days map to 8 to 12 May.

The shield damage on each day comes from the strongest real flare of that day. X-class flares are the strongest, then M, C and B. The biggest flare of this storm, X5.8 on 11 May, is why day 4 is the hardest.

## Data sources

- **DONKI** (Space Weather Database Of Notifications, Knowledge, Information), NASA Community Coordinated Modeling Center (CCMC), Goddard Space Flight Center: https://ccmc.gsfc.nasa.gov/tools/DONKI/

Data courtesy of NASA CCMC and the DONKI service. The 2024 storm period was chosen because it was one of the strongest geomagnetic storms in decades.

## What kids learn

- Spaceflight is a budget: every resource is limited and linked to the others.
- Radiation from the Sun is a real danger, and shielding is bought with energy.
- Sunlight, dust and storms decide how much power a Moon base has.
- Messages from Earth are not instant, so crews must be able to decide for themselves.
- Safe-looking choices can have hidden costs later.

## Run it locally

```
git clone https://github.com/bfoullane/luna-ctrl.git
cd luna-ctrl
python -m venv venv
```

Activate the virtual environment:

- Windows: `venv\Scripts\activate`
- Mac / Linux: `source venv/bin/activate`

Then install and run:

```
pip install -r requirements.txt
streamlit run app.py
```

To refresh the archived data (optional, needs internet):

```
python nasa_data.py
```

## Balance testing

Difficulty is tuned with data, not guesswork. `balance_test.py` plays 2,000 simulated games per player type (random, careful and reckless) and reports win rates, average science collected, and the day players lose on. The goal for Junior level is that careful players win about 90% of the time, random players about 50%, and reckless players rarely.

```
python balance_test.py
```

There is also a text-only version of the game for quick rule testing: `python test_engine.py`.

## Project structure

| File | Purpose |
|---|---|
| `app.py` | Streamlit entry point, page styling and screen routing |
| `engine.py` | Game rules, events and consequences (no UI) |
| `events.py` | Turns the real flare data into daily storm strength |
| `ui_home.py` | Home screen and level selection |
| `ui_day.py` | Daily gameplay screen |
| `sound_fx.py` | Music and sound effects, synthesized in the browser (no audio files, no copyright issues) |
| `nasa_data.py` | Fetches DONKI data and saves the archive |
| `balance_test.py` | Simulates thousands of games to tune difficulty |
| `test_engine.py` | Text-only version of the game for testing the rules |
| `data/donki_archive.json` | Archived real DONKI data for 8 to 13 May 2024 |

## Tech

Python, Streamlit, the Web Audio API, and NASA's DONKI API. No account, login or download is needed to play.

## Limitations

This is an educational simulation, not a validated spacecraft model. The numbers are simplified so the trade-offs are easy to see.

## About

Built by Basma Foullane, an engineering student at ENSA Oujda, Morocco, as a solo entry for NASA Space Apps Challenge 2026.