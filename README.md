# LUNA-CTRL 🌙

**A 5-day Moon base survival game for kids aged 7 to 12, powered by real NASA solar flare data.**

Built for the NASA Space Apps Challenge 2026: *Build a Junior Astronaut Mission Trainer*.

| | |
|---|---|
| 🎮 **Play online** |  |
| 📑 **Demo slides** |  |

## The idea

You are the commander of a small Moon base. For five Moon days you keep your crew alive while the Sun throws a real storm at you. Every choice has a price: power spent on the shield is power you can't spend on air. That is the engineering trade-off mission planners face, and the game lets kids *feel* it instead of reading about it.

The five game days match **8 to 12 May 2024**, the days of one of the strongest solar storms in decades. Each morning the game shows what the Sun really did that day, using archived data from NASA's DONKI database.

## How a day works

1. **Morning report.** The real flare count and strongest flare class for that date, plus one space fact.
2. **Events.** Each event gives two options, and each option has a cost. A timer runs (see levels below).
3. **Consequences.** Three short cards: what changed, *why* it happened, and a "Did you know?" fact.
4. **Pick 2 actions.** Spend your limited effort: make oxygen, clean solar panels, reinforce the shield, tend the garden, or do science.
5. **Storm.** The day's real flare strength is compared with your shield, and you see the result.

### Winning and losing

- **You lose** if **power** or **air** reaches zero at the end of a day. From day 3 you also lose if **food** reaches zero.
- **You win** by surviving all five days. Your score is the **science** you collected.
- **Stars:** ⭐ survive · ⭐⭐ also collect 30+ science · ⭐⭐⭐ collect 40+ science *and* finish with power, air and food all at 15 or more.

### The five factors

| Factor | What it means | The trade-off |
|---|---|---|
| Power | Electricity from solar panels | Everything else runs on it |
| Life support | The air your crew breathes | The oxygen machine costs power |
| Radiation shielding | The base's protection from the Sun | Reinforcing it costs power |
| Food production | The garden | Lights and water cost power and air |
| Communication delay | Earth's advice arrives late | Wait for orders, or decide on your own |

One new factor unlocks each day, so young players learn one idea at a time. By day 5 all five matter at once.

### The five days

| Day | Real date | New factor | Headline event |
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

When the timer runs out on an event, the crew automatically takes the safe option.

## Real NASA data and what is simulated

| Real | Simulated |
|---|---|
| Solar flare dates, times and classes (X, M, C, B) from DONKI | Dust storms, repairs, garden and air events |
| The flare count and strongest class shown each morning | All resource numbers and costs |
| The strongest flare of each day, which sets that day's storm strength | How strong a flare is *in game points* (our own balancing scale) |
| | The Earth message delay (see below) |

The game uses **archived** data saved in `data/donki_archive.json`. It is never presented as live data. The archive covers 8 to 13 May 2024 and holds flare (FLR), coronal mass ejection (CME) and geomagnetic storm (GST) records. **Gameplay currently uses the flare records only.** CME and GST records are archived for future versions.

### Simplifications we want to be honest about

- **Flares stand in for the whole storm.** In reality the 10 to 11 May 2024 event was a severe *geomagnetic* storm driven by CMEs, and the radiation risk to a Moon base comes mainly from energetic particles, not from flare class itself. We use flare class as one clear, measurable number that kids can follow day by day.
- **The shield is a game concept.** The Moon has no global magnetic field. Real Moon habitats are planned to use thick layers of lunar soil and water around the walls. The game's "active shield" is a simplified stand-in.
- **Earth delay is exaggerated.** The real Earth-Moon radio delay is about 1.3 seconds each way. In the game, "Wait for Earth" means the shield boost arrives *after* the storm, to show why a crew must be able to decide on its own.
- **Numbers are for gameplay.** Resource values and costs are balanced for fun and clarity, not taken from a spacecraft model.

## What kids learn

- Spaceflight is a budget: every resource is limited and linked to the others.
- Radiation from the Sun is a real danger, and protection costs energy.
- Sunlight, dust and storms decide how much power a Moon base has.
- Messages from Earth are not instant, so crews must be able to decide for themselves.
- A choice that looks safe can have a hidden cost later.

## Accessibility and kid-friendly design

- Resource bars always show a number and a "Low!" text warning, never colour alone.
- Large buttons and short sentences, with a friendly mascot (Itiri) explaining each result.
- Sound is optional: music and effects are synthesized in the browser and can be muted at any time. No audio files are used.
- No account, login, ads or personal data.

## Run it locally

```
git clone https://github.com/bfoullane/luna-ctrl.git
cd luna-ctrl
python -m venv venv
```

Activate the virtual environment:

- Windows (PowerShell): `venv\Scripts\activate`
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

> **Note:** the app is tested with Streamlit 1.67.0 (pinned in `requirements.txt`). You may see a log message that `st.components.v1.html` is deprecated. It is harmless and does not affect play.

## Testing and balance

The game rules live in `engine.py` with no UI code, so they can be tested directly.

```
pip install pytest
python -m pytest -v          # rule checks
python balance_test.py       # simulates 2,000 games per player type and level
python play_cli.py           # play the rules in the terminal
```

Difficulty is tuned with simulations, not guesswork. `balance_test.py` plays three kinds of simulated players (**random**, **careful** and **reckless**) through the same step order as the real game screen, and reports win rate, average science and the day players lose on. The design goals:

- Junior: careful players win about 90% of the time, random players about half, and reckless players rarely.
- Commander and Expert must show clearly lower win rates than Junior for the same players.

## Project structure

| File | Purpose |
|---|---|
| `app.py` | Streamlit entry point, page styling and screen routing |
| `engine.py` | Game rules, events and consequences (no UI) |
| `events.py` | Turns the real flare data into daily storm strength |
| `ui_home.py` | Home screen and level selection |
| `ui_day.py` | Daily gameplay screens and ending screens |
| `art.py` | SVG artwork: the mascot and one picture per event |
| `styles.py` | CSS for the game screens |
| `sound_fx.py` | Music and sound effects, synthesized in the browser |
| `nasa_data.py` | Fetches DONKI data and saves the archive |
| `balance_test.py` | Simulates thousands of games to tune difficulty |
| `test_rules.py` | Automatic rule checks (pytest) |
| `play_cli.py` | Text-only version of the game for quick rule testing |
| `data/donki_archive.json` | Archived DONKI data for 8 to 13 May 2024 |

## Tech

Python, Streamlit, the Web Audio API, and NASA's DONKI API. Nothing to install or download for players.

## Data sources

- **DONKI** (Space Weather Database Of Notifications, Knowledge, Information), NASA Community Coordinated Modeling Center (CCMC), Goddard Space Flight Center: https://ccmc.gsfc.nasa.gov/tools/DONKI/

Data courtesy of NASA CCMC and the DONKI service. This project is not endorsed by NASA.

## Limitations

This is an educational simulation, not a validated spacecraft model. Storm strength comes from flare class only, resource numbers are simplified, and progress (such as personal best science) is kept only for the current browser session.

## AI use disclosure

AI assistance (Claude by Anthropic) was used for code review,and the slide deck. Game design, scenarios, balancing decisions and final testing were done by the author.

## About

Built by Basma Foullane, an engineering student at ENSA Oujda, Morocco, as a solo entry for NASA Space Apps Challenge 2026.