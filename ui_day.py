"""Daily gameplay screens for LUNA-CTRL (logic only; art lives in art.py, CSS in styles.py)."""
import math
import random
import time
from datetime import date

import streamlit as st

from art import EVENT_ART, itiri
from engine import (ACTIONS, DAYS, DAY_FACTS, DIFFICULTY, EVENTS, UNLOCK,
                    available, new_game, resolve_end_of_day, resolve_event,
                    resolve_morning, start_day)
from events import rank as rank_key
from sound_fx import play_sound_engine
from styles import CSS, ENDING_CSS

# =====================================================================
# CONSTANTS
# =====================================================================
NAMES = {"power": ("⚡", "Power"), "oxygen": ("💨", "Air"), "shield": ("🛡️", "Shield"),
         "food": ("🌱", "Food"), "science": ("⭐", "Science"), "panel": ("🔆", "Panels")}
FACTOR = {"power": "power", "oxygen": "life", "shield": "shield", "food": "food"}
RESOURCES = ("power", "oxygen", "shield", "food")

LEVEL_ORDER = ["junior", "commander", "expert"]
STAR2_SCIENCE = 30          # 2nd star: at least this much science
STAR3_SCIENCE = 40          # 3rd star: this much science ...
STAR3_MIN_RESOURCE = 15     # ... AND power, air and food all at least this high at the end

RANKS = {
    1: ("Moon Cadet", "You kept your crew alive through a real solar superstorm!"),
    2: ("Lunar Commander", "A safe base AND great science. Mission Control is impressed!"),
    3: ("Solar Storm Hero", "A near-perfect mission. Mission Control is cheering!"),
}

LOSS_TIPS = {
    "oxygen": ("💨", "The air ran out",
               "The oxygen machine uses power, but a crew cannot live without air. "
               "Next time, pick “Make oxygen” before the air bar gets low."),
    "power": ("⚡", "The power ran out",
              "Everything on the base runs on power. Keep an eye on the power bar, "
              "and remember that the shield and the oxygen machine both use it."),
    "food": ("🌱", "The food ran out",
             "From Day 3 your crew gets hungry every day. Pick “Tend the garden” "
             "before the food bar gets low."),
}


# =====================================================================
# SMALL HELPERS
# =====================================================================
def pretty_date(day_info, day_number):
    """'8 May 2024' from the real data (falls back to the old hardcoded date)."""
    iso = day_info.get("date")
    if iso:
        d = date.fromisoformat(iso)
        return f"{d.day} {d.strftime('%B')} {d.year}"
    return f"{7 + day_number} May 2024"


def visible(k, day):
    return k in ("science", "panel") or FACTOR[k] in UNLOCK[day]


def chips(fx, day, show_after=False):
    parts = []
    for k, v in fx.items():
        if visible(k, day) and v != 0:
            cls = "up" if v > 0 else "dn"
            suffix = " (later)" if show_after else ""
            parts.append(f'<span class="lc-chip {cls}">{NAMES[k][0]} {v:+d} {NAMES[k][1]}{suffix}</span>')
    return "".join(parts)


def storm_was_hit(ui):
    return any("Storm hit" in line for line in ui["storm_lines"])


# =====================================================================
# STATE TRANSITIONS (no drawing here)
# =====================================================================
def init_day_ui(g):
    start_day(g)
    g["_started"] = g["day"]
    sun, sun_msg = resolve_morning(g)
    g["ui"] = {
        "phase": "briefing_sun",
        "ev_idx": 0,
        "turn_start": time.time(),
        "records": [],
        "last_rec": None,
        "acts": [],
        "sun": sun,
        "sun_msg": sun_msg,
        "storm_lines": [],
        "report_day": g["day"],
        "cue": "briefing",
        "cue_id": f"d{g['day']}_brief1",
    }


def set_phase(ui, phase, cue, cue_tag):
    ui["phase"] = phase
    ui["cue"] = cue
    ui["cue_id"] = cue_tag


def choose_event_option(g, ev_id, opt_id, timed_out=False):
    ui = g["ui"]
    rec = resolve_event(g, ev_id, opt_id)
    rec["timed_out"] = timed_out
    ui["records"].append(rec)
    ui["last_rec"] = rec
    has_bad = any(v < 0 for k, v in rec["deltas"].items() if k in RESOURCES + ("panel",))
    cue = "warn" if (has_bad or rec["extra"] or timed_out) else "good"
    set_phase(ui, "result_consequence", cue, f"d{g['day']}_e{ui['ev_idx']}_res")


def toggle_action(ui, a):
    if a in ui["acts"]:
        ui["acts"].remove(a)
    elif len(ui["acts"]) < 2:
        ui["acts"].append(a)
        ui["cue"] = "action"
        ui["cue_id"] = f"act_{a}_{time.time()}"
    else:
        st.toast("Pick 2 actions! Tap a selected one to swap it.", icon="👆")


def finish_day_actions(g):
    ui = g["ui"]
    ui["storm_lines"] = resolve_end_of_day(g, list(ui["acts"]), ui["records"])
    cue = ("win" if g["won"] else "warn" if g["over"]
           else "storm_hit" if storm_was_hit(ui) else "storm_ok")
    set_phase(ui, "storm_result", cue, f"d{ui['report_day']}_storm")


def restart(level):
    st.session_state.game = new_game(level=level)


# =====================================================================
# TOP BAR AND HUD
# =====================================================================
def header_and_audio_bar(g):
    if "muted" not in st.session_state:
        st.session_state.muted = False
    dots = "".join(
        f'<i class="{"done" if i < g["day"] else "now" if i == g["day"] else ""}"></i>'
        for i in range(1, 6))
    c_main, c_snd = st.columns([5, 1])
    c_main.markdown(
        f'<div class="lc-top"><div>🌙 Moon Day {min(g["day"], 5)} of 5</div>'
        f'<div class="lc-dots">{dots}</div><div class="lc-lvl">{g["level"].title()}</div></div>',
        unsafe_allow_html=True,
    )
    snd_label = "🔇 Muted" if st.session_state.muted else "🔊 Sound"
    if c_snd.button(snd_label, key="toggle_sound", use_container_width=True):
        st.session_state.muted = not st.session_state.muted
        st.rerun()


def hud(g, day):
    keys = [k for k in RESOURCES if visible(k, day)]
    cols = st.columns(len(keys) + 1)
    for col, k in zip(cols[:-1], keys):
        val = g[k]
        color = "#4cd97b" if val >= 60 else "#ffc93c" if val >= 30 else "#ff6b6b"
        low = "⚠️ Low!" if val < 30 else " "
        col.markdown(
            f'<div class="lc-m"><div class="lc-mh"><span>{NAMES[k][0]} {NAMES[k][1]}</span><b>{val}</b></div>'
            f'<div class="lc-bar"><i style="width:{val}%;background:{color}"></i></div>'
            f'<div class="lc-low">{low}</div></div>',
            unsafe_allow_html=True,
        )
    cols[-1].markdown(
        f'<div class="lc-sci">⭐ Science: {g["science"]}<br>'
        f'<span style="color:#CECBF6;font-size:.85rem">🔆 Panels: {g["panel"]}%</span></div>',
        unsafe_allow_html=True,
    )


def render_timer_block(g, ev_id):
    limit = DIFFICULTY[g["level"]]["timer"]
    if not limit:
        return
    ui = g["ui"]
    elapsed = time.time() - ui["turn_start"]
    rem = max(0, round(limit - elapsed))
    pct = max(0, min(100, int((limit - elapsed) / limit * 100)))
    bar_color = "#4cd97b" if pct > 50 else "#ffc93c" if pct > 25 else "#ff6b6b"
    st.markdown(
        f'<div class="lc-timer-wrap"><div class="lc-timer-top"><span>⏱️ Decision Timer</span>'
        f'<span>{rem}s left</span></div>'
        f'<div class="lc-timer-bar"><i style="width:{pct}%;background:{bar_color}"></i></div></div>',
        unsafe_allow_html=True,
    )
    if rem <= 0:
        opts = EVENTS[ev_id]["options"]
        fallback = next((k for k, v in opts.items() if v.get("safe")), list(opts)[0])
        choose_event_option(g, ev_id, fallback, timed_out=True)
        st.rerun()


# =====================================================================
# DAY SCREENS, IN THE ORDER THE PLAYER SEES THEM
# =====================================================================
# --- 1a. Morning solar report ---
def render_briefing_sun(g, ui):
    day = g["day"]
    d = DAYS[day - 1]
    fact = DAY_FACTS[day]
    st.markdown(
        f'<div class="lc-stage"><span class="lc-badge">Morning Report • 1 of 2</span>'
        f'<div class="lc-title">☀️ Real NASA Solar Report — {pretty_date(d, day)}</div>'
        f'<div class="lc-sub">NASA satellites recorded <b>{d["flares"]} solar flares</b> on this date. '
        f'The strongest flare was class <b>{d["max_class"]}</b>.</div>'
        f'<div class="lc-sub" style="color:#7fe7ff;font-weight:700">{fact["unlock"]} — {ui["sun_msg"]}</div>'
        f'<div class="lc-tip">{itiri("happy")}<div class="lc-say">Good morning, Commander! '
        f'Let\'s check today\'s space science tip before the events start.</div></div></div>',
        unsafe_allow_html=True,
    )
    if st.button("Next: Did You Know? 🔭 ➔", key="brief_next_1", type="primary", use_container_width=True):
        set_phase(ui, "briefing_dyk", "dyk", f"d{day}_brief2")
        st.rerun()


# --- 1b. Morning "did you know" ---
def render_briefing_dyk(g, ui):
    day = g["day"]
    fact = DAY_FACTS[day]
    st.markdown(
        f'<div class="lc-box-dyk"><span class="lc-badge">🔭 Did You Know? • 2 of 2</span>'
        f'<div class="lc-title" style="color:#ffc93c">{fact["unlock"]}</div>'
        f'<div class="lc-sub">{fact["fact"]}</div>'
        f'<div class="lc-tip">{itiri("joy")}<div class="lc-say">Ready for today\'s mission events? '
        f'Stay sharp!</div></div></div>',
        unsafe_allow_html=True,
    )
    if st.button(f"Start Day {day} Events 🚀", key="start_events", type="primary", use_container_width=True):
        ui["turn_start"] = time.time()
        set_phase(ui, "event_choice", "event", f"d{day}_e0_choice")
        st.rerun()


# --- 2. Event picture + two choice cards ---
def render_event_choice(g, ui):
    day = g["day"]
    idx = ui["ev_idx"]
    total = len(g["today"])
    ev_id = g["today"][idx]
    ev = EVENTS[ev_id]

    frag = getattr(st, "fragment", None)
    if frag:
        @frag(run_every=1)
        def _live_timer():
            render_timer_block(g, ev_id)
        _live_timer()
    else:
        render_timer_block(g, ev_id)

    st.markdown(
        f'<div class="lc-stage"><span class="lc-badge">Event {idx + 1} of {total}</span>'
        f'<div class="lc-title">{ev["title"]}</div>'
        f'<div class="lc-sub">{ev["text"]}</div>'
        f'<div class="lc-art">{EVENT_ART[ev_id]}</div></div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(len(ev["options"]))
    for col, (oid, opt) in zip(cols, ev["options"].items()):
        with col:
            now_chips = chips(opt.get("now", {}), day)
            after_chips = chips(opt.get("after", {}), day, show_after=True)
            risk_badge = ""
            if "risk" in opt:       # chance comes from the engine, not hardcoded
                pct = round(opt["risk"][0] * 100)
                risk_badge = f'<span class="lc-chip wait">🎲 {pct}% Dust Scratch Risk</span>'
            st.markdown(
                f'<div class="lc-choice-card"><b>{opt["label"]}</b>{now_chips}{after_chips}{risk_badge}</div>',
                unsafe_allow_html=True,
            )
            st.button(
                f"Choose: {opt['label']} ➔",
                key=f"pick_{day}_{idx}_{oid}",
                type="primary",
                use_container_width=True,
                on_click=choose_event_option,
                args=(g, ev_id, oid, False),
            )


# --- 3a. Consequence card (1 of 3) ---
def render_result_consequence(g, ui):
    day = g["day"]
    rec = ui["last_rec"]
    opt = EVENTS[rec["ev_id"]]["options"][rec["choice"]]
    has_bad = any(v < 0 for k, v in rec["deltas"].items() if k in RESOURCES + ("panel",))

    if rec.get("timed_out"):
        mood = "worry"
        reaction = "Time zipped by! I hit the safety switch so the crew stayed protected."
    elif rec["extra"]:
        mood = "worry"
        reaction = "Whoa! That sharp Moon dust scratched the solar panels! Let's see what changed."
    elif has_bad:
        mood = "worry"
        reaction = "Ooh, a classic space trade-off! Protecting one system meant spending another."
    else:
        mood = "joy"
        reaction = "Awesome decision, Commander! Look at how your base responded."

    delta_html = chips(rec["deltas"], day) or '<span class="lc-chip wait">⏳ Effect arrives after the storm!</span>'
    extra_html = "".join(
        f"<p style='color:#ffb347;font-weight:700;margin:8px 0 0'>⚠️ {x}</p>" for x in rec["extra"])
    warn = "warn" if (rec["extra"] or has_bad) else ""

    st.markdown(
        f'<div class="lc-box-res {warn}">'
        f'<span class="lc-badge">Consequence</span><span class="lc-step-pills">Card 1 of 3</span>'
        f'<div class="lc-title">You chose: {opt["label"]}</div>'
        f'<div class="lc-sub">{rec["note"]}</div>'
        f'<div>{delta_html}</div>{extra_html}'
        f'<div class="lc-tip">{itiri(mood)}<div class="lc-say">{reaction}</div></div></div>',
        unsafe_allow_html=True,
    )
    if st.button("Next: Why Did That Happen? 🧠 ➔", key=f"to_why_{day}_{ui['ev_idx']}",
                 type="primary", use_container_width=True):
        set_phase(ui, "result_why", "why", f"d{day}_e{ui['ev_idx']}_why")
        st.rerun()


# --- 3b. Why did that happen? (2 of 3) ---
def render_result_why(g, ui):
    day = g["day"]
    rec = ui["last_rec"]
    ev = EVENTS[rec["ev_id"]]
    st.markdown(
        f'<div class="lc-box-why">'
        f'<span class="lc-badge" style="background:#7fe7ff">🧠 Why Did That Happen?</span>'
        f'<span class="lc-step-pills">Card 2 of 3</span>'
        f'<div class="lc-title" style="color:#7fe7ff">{ev["title"]}</div>'
        f'<div class="lc-sub">{rec["explain"]}</div>'
        f'<div class="lc-tip">{itiri("happy")}<div class="lc-say">Real NASA engineers weigh '
        f'trade-offs just like this on every mission!</div></div></div>',
        unsafe_allow_html=True,
    )
    if st.button("Next: Did You Know? 🔭 ➔", key=f"to_dyk_{day}_{ui['ev_idx']}",
                 type="primary", use_container_width=True):
        set_phase(ui, "result_dyk", "dyk", f"d{day}_e{ui['ev_idx']}_dyk")
        st.rerun()


# --- 3c. Did you know? (3 of 3) ---
def render_result_dyk(g, ui):
    day = g["day"]
    rec = ui["last_rec"]
    st.markdown(
        f'<div class="lc-box-dyk">'
        f'<span class="lc-badge">🔭 Did You Know?</span><span class="lc-step-pills">Card 3 of 3</span>'
        f'<div class="lc-title" style="color:#ffc93c">Real Moon & Space Science</div>'
        f'<div class="lc-sub">{rec["did_you_know"]}</div>'
        f'<div class="lc-tip">{itiri("joy")}<div class="lc-say">Space fact unlocked! '
        f'Ready for the next step, Commander?</div></div></div>',
        unsafe_allow_html=True,
    )
    total = len(g["today"])
    is_last = (ui["ev_idx"] + 1) >= total
    label = ("Pick Today's 2 Base Actions 🛠️ ➔" if is_last
             else f"Next Event ({ui['ev_idx'] + 2} of {total}) ➔")
    if st.button(label, key=f"done_ev_{day}_{ui['ev_idx']}", type="primary", use_container_width=True):
        ui["ev_idx"] += 1
        if ui["ev_idx"] < total:
            ui["turn_start"] = time.time()
            set_phase(ui, "event_choice", "event", f"d{day}_e{ui['ev_idx']}_choice")
        else:
            set_phase(ui, "actions", "briefing", f"d{day}_actions")
        st.rerun()


# --- 4. Pick 2 crew actions ---
def render_actions(g, ui):
    day = g["day"]
    acts = available(g)
    st.markdown(
        f'<div class="lc-stage"><span class="lc-badge">Base Operations</span>'
        f'<div class="lc-title">🛠️ Pick 2 Crew Actions ({len(ui["acts"])}/2 selected)</div>'
        f'<div class="lc-sub">Spend your remaining energy to prepare the Moon base '
        f'before the solar storm hits!</div></div>',
        unsafe_allow_html=True,
    )
    cols = st.columns(len(acts))
    for col, a in zip(cols, acts):
        info = ACTIONS[a]
        sel = a in ui["acts"]
        with col:
            st.markdown(
                f'<div class="lc-choice-card" style="border-color:{"#ffc93c" if sel else "#7fe7ff"}">'
                f'<b>{info["icon"]} {info["label"]}</b>'
                f'<p style="color:#CECBF6;font-size:.92rem;margin:4px 0 8px">{info["desc"]}</p>'
                f'{chips(info["fx"], day)}</div>',
                unsafe_allow_html=True,
            )
            st.button(
                ("✓ Selected: " if sel else "Select ") + info["label"],
                key=f"act_{day}_{a}",
                type="primary" if sel else "secondary",
                use_container_width=True,
                on_click=toggle_action,
                args=(ui, a),
            )
    st.button(
        "End Day & Face the Solar Storm ☀️🛡️",
        key=f"endday_{day}",
        disabled=len(ui["acts"]) != 2,
        type="primary",
        use_container_width=True,
        on_click=finish_day_actions,
        args=(g,),
    )


# --- 5. End-of-day storm report ---
def render_storm_result(g, ui, go_home):
    if g["over"]:                      # win or loss: show the special ending screen
        render_ending(g, ui, go_home)
        return
    day = ui["report_day"]
    if storm_was_hit(ui):
        mood = "worry"
        headline = "☀️ The Solar Storm Pierced the Shield!"
        msg = "The real flare was stronger than your shield today, so extra power was lost protecting the crew."
    else:
        mood = "joy"
        headline = "🛡️ Shield Held Strong!"
        msg = "Your shield blocked the solar radiation and kept the Moon base safe!"

    lines_html = "".join(
        f"<p style='margin:6px 0;font-size:1.05rem'>• {line}</p>" for line in ui["storm_lines"])
    warn = "warn" if mood == "worry" else ""
    st.markdown(
        f'<div class="lc-box-res {warn}">'
        f'<span class="lc-badge">End of Moon Day {day}</span>'
        f'<div class="lc-title">{headline}</div>'
        f'<div class="lc-sub">{msg}</div>{lines_html}'
        f'<div class="lc-tip">{itiri(mood)}<div class="lc-say">{msg}</div></div></div>',
        unsafe_allow_html=True,
    )
    if st.button(f"Continue to Moon Day {g['day']} 🚀", key=f"next_day_{day}",
                 type="primary", use_container_width=True):
        g["ui"] = None
        st.rerun()


# =====================================================================
# ENDING SCREENS (win / lose)
# =====================================================================
def ending_summary(g, ui):
    """Works out how the game ended. Pure logic, no Streamlit."""
    last_day = ui["report_day"]
    s = {"won": g["won"], "last_day": last_day, "level": g["level"], "science": g["science"]}
    if g["won"]:
        lowest = min(g["power"], g["oxygen"], g["food"])
        s["stars"] = (1 + (g["science"] >= STAR2_SCIENCE)
                      + (g["science"] >= STAR3_SCIENCE and lowest >= STAR3_MIN_RESOURCE))
    else:
        empty = [k for k in ("oxygen", "power", "food")
                 if g[k] <= 0 and (k != "food" or last_day >= 3)]
        s["cause"] = empty[0] if empty else "power"
        s["storm_hit"] = storm_was_hit(ui)
    return s


def _star(cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append(f"{cx + rad * math.cos(ang):.1f},{cy + rad * math.sin(ang):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}"/>'


def patch_svg(stars, level):
    """A round mission patch that shows the stars you earned."""
    star_row = "".join(_star(70 + 30 * i, 142, 13, "#ffc93c" if i < stars else "#534ab7") for i in range(3))
    return ('<svg viewBox="0 0 200 200" class="lc-patch" aria-label="Mission patch">'
            '<circle cx="100" cy="100" r="95" fill="#ffc93c"/>'
            '<circle cx="100" cy="100" r="86" fill="#26215C" stroke="#7fe7ff" stroke-width="3"/>'
            '<text x="100" y="42" text-anchor="middle" font-size="15" font-weight="800" fill="#7fe7ff" font-family="sans-serif">LUNA-CTRL</text>'
            '<circle cx="100" cy="86" r="30" fill="#EEEDFE"/><circle cx="90" cy="78" r="6" fill="#CECBF6"/>'
            '<circle cx="112" cy="92" r="8" fill="#CECBF6"/><circle cx="96" cy="100" r="4" fill="#CECBF6"/>'
            + star_row +
            f'<text x="100" y="172" text-anchor="middle" font-size="13" font-weight="800" fill="#ffd966" font-family="sans-serif">{level.upper()}</text>'
            '</svg>')


def confetti_html(n=45):
    r = random.Random(7)
    colors = ["#ffc93c", "#7fe7ff", "#ff66d9", "#4cd97b", "#ff8a3d"]
    bits = "".join(
        f'<i style="left:{r.randint(0, 100)}%;background:{r.choice(colors)};'
        f'animation-delay:{r.random() * 2:.2f}s;animation-duration:{2.5 + r.random() * 2:.2f}s"></i>'
        for _ in range(n))
    return f'<div class="lc-confetti">{bits}</div>'


def journey_html(last_day, won):
    cells = []
    for d in range(1, 6):
        if won or d < last_day:
            cells.append('<span class="ok">✓</span>')
        elif d == last_day:
            cells.append('<span class="bad">✗</span>')
        else:
            cells.append(f'<span class="na">{d}</span>')
    return '<div class="lc-journey">' + "".join(cells) + '</div>'


def _render_win(g, e):
    stars = e["stars"]
    rank, rank_msg = RANKS[stars]
    total_flares = sum(d["flares"] for d in DAYS)
    top_class = max((d["max_class"] for d in DAYS), key=rank_key)
    chips_html = "".join(f'<span class="lc-chip neu">{NAMES[k][0]} {NAMES[k][1]} {g[k]}</span>'
                         for k in RESOURCES)
    best_html = '<div class="lc-newbest">🏆 New personal best!</div>' if e.get("new_best") else ""
    hint = ("" if stars == 3 else
            f'<div class="lc-sub" style="color:#7fe7ff;font-weight:700">Want 3 stars? '
            f'Collect {STAR3_SCIENCE}+ science and finish with power, air and food '
            f'all above {STAR3_MIN_RESOURCE - 1}.</div>')
    st.markdown(
        confetti_html()
        + '<div class="lc-end win"><span class="lc-badge">Mission Complete</span>'
        + patch_svg(stars, e["level"])
        + f'<div class="lc-rank">{rank}</div>'
        + f'<div class="lc-sub">{rank_msg}</div>'
        + f'<div class="lc-bigsci">⭐ {g["science"]} Science Points</div>{best_html}'
        + journey_html(e["last_day"], True)
        + f'<div>{chips_html}</div>'
        + f'<div class="lc-sub" style="margin-top:.8rem">The real Sun fired <b>{total_flares} solar flares</b> '
          f'during these 5 days in May 2024. The strongest was class <b>{top_class}</b>, '
          f'and you kept the crew safe through all of them.</div>'
        + hint
        + f'<div class="lc-tip">{itiri("joy")}<div class="lc-say">Fantastic work, Commander! '
          f'You are a real space hero!</div></div></div>',
        unsafe_allow_html=True,
    )
    nxt = LEVEL_ORDER[LEVEL_ORDER.index(e["level"]) + 1] if e["level"] != LEVEL_ORDER[-1] else None
    if nxt:
        cols = st.columns(2)
        cols[0].button(f"Play {e['level'].title()} again 🔁", key="end_again", on_click=restart,
                       args=(e["level"],), use_container_width=True)
        cols[1].button(f"Try {nxt.title()} level 🚀", key="end_next", type="primary", on_click=restart,
                       args=(nxt,), use_container_width=True)
    else:
        st.button(f"Play {e['level'].title()} again 🔁", key="end_again", type="primary",
                  on_click=restart, args=(e["level"],), use_container_width=True)


def _render_loss(g, e):
    icon, title, tip = LOSS_TIPS[e["cause"]]
    survived = e["last_day"] - 1
    day_info = DAYS[e["last_day"] - 1]
    extras = []
    if e["cause"] == "power" and g["panel"] < 70:
        extras.append("Moon dust scratched your solar panels, so they made less power.")
    if e["storm_hit"]:
        extras.append("The solar storm got through a weak shield today and cost you extra "
                      + ("food." if e["cause"] == "food" else "power."))
    extras_html = "".join(f"<div>• {x}</div>" for x in extras)
    progress = (f"You kept the base running for {survived} of 5 days." if survived > 0
                else "Day 1 is a tough one, and almost every astronaut has a hard first try.")
    st.markdown(
        '<div class="lc-end lose"><span class="lc-badge">Mission Debrief</span>'
        + f'<div class="lc-title">Mission paused on Moon Day {e["last_day"]}</div>'
        + f'<div class="lc-sub">{progress}</div>'
        + journey_html(e["last_day"], False)
        + f'<div class="lc-cause"><b>{icon} What happened: {title}</b>'
          f'<div style="margin:.4rem 0">{tip}</div>{extras_html}</div>'
        + f'<div class="lc-sub">On {pretty_date(day_info, e["last_day"])} the real Sun produced '
          f'<b>{day_info["flares"]} solar flares</b>, the strongest was class <b>{day_info["max_class"]}</b>. '
          f'Real NASA teams practice missions again and again until they get it right.</div>'
        + f'<div class="lc-tip">{itiri("worry")}<div class="lc-say">Do not worry, Commander! '
          f'Every astronaut learns from a tough mission. Let us try again!</div></div></div>',
        unsafe_allow_html=True,
    )
    st.button(f"Try {e['level'].title()} again 🔁", key="end_again", type="primary",
              on_click=restart, args=(e["level"],), use_container_width=True)


def render_ending(g, ui, go_home):
    # work out the ending once, so "new personal best" does not flicker on reruns
    if "ending" not in ui:
        ui["ending"] = ending_summary(g, ui)
        if g["won"]:
            best = st.session_state.setdefault("best_science", {})
            prev = best.get(g["level"], 0)
            ui["ending"]["new_best"] = prev > 0 and g["science"] > prev
            best[g["level"]] = max(prev, g["science"])
    e = ui["ending"]
    st.markdown(ENDING_CSS, unsafe_allow_html=True)
    if e["won"]:
        _render_win(g, e)
    else:
        _render_loss(g, e)
    st.button("Back to Mission Control Home 🏠", key="go_home_btn", on_click=go_home,
              use_container_width=True)


# =====================================================================
# ENTRY POINT (called from app.py)
# =====================================================================
PHASES = {
    "briefing_sun": render_briefing_sun,
    "briefing_dyk": render_briefing_dyk,
    "event_choice": render_event_choice,
    "result_consequence": render_result_consequence,
    "result_why": render_result_why,
    "result_dyk": render_result_dyk,
    "actions": render_actions,
}


def render_day(g, go_home):
    st.markdown(CSS, unsafe_allow_html=True)
    if g.get("ui") is None or (g.get("_started") != g["day"] and g["ui"].get("phase") != "storm_result"):
        init_day_ui(g)
    ui = g["ui"]
    display_day = ui["report_day"] if ui["phase"] == "storm_result" else g["day"]

    header_and_audio_bar(g)
    hud(g, display_day)
    play_sound_engine(ui.get("cue", ""), st.session_state.get("muted", False), ui.get("cue_id", ""))

    if ui["phase"] == "storm_result":
        render_storm_result(g, ui, go_home)
    else:
        PHASES[ui["phase"]](g, ui)