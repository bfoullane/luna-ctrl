import streamlit as st
from engine import ACTIONS, EVENTS, UNLOCK, DAYS, available, start_day, play_day

NAMES = {"power": ("⚡", "Power"), "oxygen": ("💨", "Air"), "shield": ("🛡️", "Shield"),
         "food": ("🌱", "Food"), "science": ("⭐", "Science")}
FACTOR = {"power": "power", "oxygen": "life", "shield": "shield", "food": "food"}

CSS = """<style>
.lc-top{display:flex;align-items:center;justify-content:space-between;gap:12px;color:#fff;font-weight:700;font-size:1.3rem;margin-bottom:.6rem}
.lc-dots{display:flex;gap:8px}.lc-dots i{width:16px;height:16px;border-radius:50%;background:#3C3489;border:2px solid #7fe7ff}
.lc-dots i.done{background:#7fe7ff}.lc-dots i.now{background:#ffc93c;border-color:#ffc93c;transform:scale(1.25)}
.lc-lvl{background:#7fe7ff;color:#26215C;border-radius:999px;padding:4px 16px;font-size:1rem}
.lc-banner{background:#3C3489;border:2px solid #ffc93c;border-radius:16px;padding:12px 16px;color:#fff;font-size:1rem;line-height:1.4;margin-bottom:1rem}
.lc-banner small{color:#CECBF6;display:block;margin-top:4px}
.lc-tip{display:flex;align-items:center;gap:14px}.lc-tip svg{width:96px;flex:none;overflow:visible;animation:lcb 3s ease-in-out infinite}
.lc-say{background:#fff;color:#26215C;border-radius:18px;padding:12px 16px;font-weight:600;font-size:1.05rem;line-height:1.3}
@keyframes lcb{50%{transform:translateY(-8px)}}
.lc-m{margin-bottom:.5rem}.lc-mh{display:flex;justify-content:space-between;color:#fff;font-weight:700;font-size:1.1rem}
.lc-mh small.up{color:#4cd97b}.lc-mh small.dn{color:#ff9a9a}
.lc-bar{height:18px;background:#3C3489;border-radius:999px;overflow:hidden}.lc-bar i{display:block;height:100%;border-radius:999px;transition:width .6s}
.lc-low{color:#ffb347;font-size:.85rem;font-weight:700;min-height:1.1rem}
.lc-sci{color:#ffd966;font-weight:700;font-size:1.1rem}
.lc-step{color:#fff;font-size:1.4rem;font-weight:700;margin:1.2rem 0 .4rem}
.lc-card{background:#3C3489;border-radius:16px;padding:12px 16px;color:#fff;margin-bottom:.5rem}
.lc-card b{font-size:1.15rem;display:block}.lc-card span{color:#CECBF6}
.lc-chip{display:inline-block;border-radius:999px;padding:2px 10px;margin:2px 4px 8px 0;font-size:.85rem;font-weight:700}
.lc-chip.up{background:#1d6b3f;color:#d6ffe6}.lc-chip.dn{background:#7a2b3a;color:#ffe0e0}
.lc-chain{background:#3C3489;border-radius:16px;padding:12px 16px;color:#fff;margin-bottom:.8rem}
.lc-chain .arr{text-align:center;color:#ffc93c;font-size:1.1rem}.lc-chain .res{background:#26215C;border-radius:12px;padding:8px 12px}
.lc-chain.hit{border:2px solid #ff9a9a}.lc-chain.ok{border:2px solid #4cd97b}
button[data-testid="stBaseButton-primary"]{background:#FFC93C!important;color:#1b1340!important;box-shadow:0 4px 0 #d9961b}
div.stButton>button{min-height:3.2rem;font-size:1.1rem}
</style>"""

FACES = {
 "happy": '<ellipse cx="50" cy="52" rx="5" ry="7" fill="#7fe7ff"/><ellipse cx="70" cy="52" rx="5" ry="7" fill="#7fe7ff"/><path d="M52 64q8 7 16 0" stroke="#7fe7ff" stroke-width="3" fill="none" stroke-linecap="round"/>',
 "worry": '<circle cx="50" cy="52" r="6.5" fill="#ffb347"/><circle cx="70" cy="52" r="6.5" fill="#ffb347"/><circle cx="50" cy="53" r="2.4" fill="#1e2a78"/><circle cx="70" cy="53" r="2.4" fill="#1e2a78"/><path d="M52 67q4-4 8 0q4 4 8 0" stroke="#ffb347" stroke-width="3" fill="none" stroke-linecap="round"/><path d="M84 38q5 8 0 12q-5-4 0-12z" fill="#7fe7ff"/>',
 "joy": '<path d="M50 44l2.4 5.2 5.6.6-4.2 3.8 1.2 5.6-5-2.8-5 2.8 1.2-5.6-4.2-3.8 5.6-.6z" fill="#ffd966"/><path transform="translate(20 0)" d="M50 44l2.4 5.2 5.6.6-4.2 3.8 1.2 5.6-5-2.8-5 2.8 1.2-5.6-4.2-3.8 5.6-.6z" fill="#ffd966"/><path d="M49 62q11 13 22 0z" fill="#7fe7ff"/>',
}


def itiri(mood):
    return ('<svg viewBox="0 0 120 150" aria-label="Itiri the mascot"><path d="M60 26v-12" stroke="#fff" stroke-width="3"/>'
            '<circle cx="60" cy="9" r="6" fill="#ffc93c"/><rect x="40" y="118" width="14" height="24" rx="7" fill="#fff"/>'
            '<rect x="66" y="118" width="14" height="24" rx="7" fill="#fff"/><rect x="32" y="80" width="56" height="46" rx="22" fill="#ff8a3d"/>'
            '<rect x="84" y="88" width="12" height="30" rx="6" fill="#fff"/><rect x="24" y="88" width="12" height="30" rx="6" fill="#fff"/>'
            '<circle cx="60" cy="102" r="7" fill="#ffc93c"/><circle cx="60" cy="52" r="38" fill="#fff"/>'
            '<ellipse cx="60" cy="54" rx="29" ry="25" fill="#1e2a78"/>' + FACES[mood] + '</svg>')


def visible(k, day):
    return k == "science" or FACTOR[k] in UNLOCK[day]


def chips(fx, day):
    return "".join(f'<span class="lc-chip {"up" if v > 0 else "dn"}">{v:+d} {NAMES[k][1]}</span>'
                   for k, v in fx.items() if visible(k, day))


def meter(k, val, delta=0):
    color = "#4cd97b" if val >= 60 else "#ffc93c" if val >= 30 else "#ff6b6b"
    dtxt = f' <small class="{"up" if delta > 0 else "dn"}">({delta:+d})</small>' if delta else ""
    low = "Low! Careful!" if val < 30 else "&nbsp;"
    return (f'<div class="lc-m"><div class="lc-mh"><span>{NAMES[k][0]} {NAMES[k][1]}</span><b>{val}{dtxt}</b></div>'
            f'<div class="lc-bar"><i style="width:{val}%;background:{color}"></i></div><div class="lc-low">{low}</div></div>')


def header(g):
    dots = "".join(f'<i class="{"done" if i < g["day"] else "now" if i == g["day"] else ""}"></i>' for i in range(1, 6))
    return f'<div class="lc-top"><div>Moon day {min(g["day"], 5)} of 5</div><div class="lc-dots">{dots}</div><div class="lc-lvl">{g["level"].title()}</div></div>'


def banner(g):
    d = DAYS[g["day"] - 1]
    return (f'<div class="lc-banner">☀️ <b>Real Sun report, {7 + g["day"]} May 2024:</b> the Sun sent out {d["flares"]} flares. '
            f'The strongest was class <b>{d["max_class"]}</b>.<small>Real data from NASA DONKI. The Moon base is a simulation.</small></div>')


def tip(text, mood):
    return f'<div class="lc-tip">{itiri(mood)}<div class="lc-say">{text}</div></div>'


def meters(g, day, before=None):
    keys = [k for k in ("power", "oxygen", "shield", "food") if visible(k, day)]
    return "".join(meter(k, g[k], (g[k] - before[k]) if before else 0) for k in keys)


def pick_event(ui, ev, opt):
    ui["choices"][ev] = opt


def toggle_action(ui, a):
    if a in ui["acts"]:
        ui["acts"].remove(a)
    elif len(ui["acts"]) < 2:
        ui["acts"].append(a)
    else:
        st.toast("Only 2 actions! Tap one to un-pick it.", icon="👆")


def end_day(g):
    ui, day = g["ui"], g["day"]
    before = {k: g[k] for k in NAMES}
    evs = list(g["today"])
    picks = [ui["choices"][e] for e in evs]
    acts = list(ui["acts"])
    rep = play_day(g, acts, picks)
    ui["report"] = {"day": day, "before": before, "after": {k: g[k] for k in NAMES},
                    "evs": list(zip(evs, picks)), "acts": acts, "lines": rep}


def next_day(g):
    g["ui"] = None


def plan(g, ui):
    day, evs = g["day"], g["today"]
    done_ev = len(ui["choices"]) == len(evs)
    ready = done_ev and len(ui["acts"]) == 2
    low = any(g[k] < 30 for k in ("power", "oxygen"))
    if ready:
        text, mood = "Ready? Tap <b>End the day</b>. The Sun's storm is coming!", "happy"
    elif done_ev:
        text, mood = "Now pick <b>2 actions</b> to spend your energy.", "happy"
    else:
        text, mood = "Hi, Commander! Read each event and tap a choice. Every choice has a cost!", "happy"
    if low:
        mood = "worry"
    st.markdown(CSS + header(g) + banner(g), unsafe_allow_html=True)
    c1, c2 = st.columns([3, 2])
    c1.markdown(tip(text, mood), unsafe_allow_html=True)
    c2.markdown(meters(g, day) + f'<div class="lc-sci">⭐ Science: {g["science"]}</div>', unsafe_allow_html=True)

    st.markdown('<div class="lc-step">1. Handle today\'s events</div>', unsafe_allow_html=True)
    for col, ev in zip(st.columns(len(evs)), evs):
        e = EVENTS[ev]
        with col:
            st.markdown(f'<div class="lc-card"><b>{e["title"]}</b><span>{e["text"]}</span></div>', unsafe_allow_html=True)
            for oid, o in e["options"].items():
                sel = ui["choices"].get(ev) == oid
                st.button(("✓ " if sel else "") + o["label"], key=f"ev_{ev}_{oid}", use_container_width=True,
                          type="primary" if sel else "secondary", on_click=pick_event, args=(ui, ev, oid))
                st.markdown(chips({**o.get("now", {}), **o.get("after", {})}, day), unsafe_allow_html=True)

    st.markdown('<div class="lc-step">2. Pick 2 actions</div>', unsafe_allow_html=True)
    acts = available(g)
    for col, a in zip(st.columns(len(acts)), acts):
        with col:
            sel = a in ui["acts"]
            st.button(("✓ " if sel else "") + ACTIONS[a]["label"], key=f"act_{a}", use_container_width=True,
                      type="primary" if sel else "secondary", on_click=toggle_action, args=(ui, a))
            st.markdown(chips(ACTIONS[a]["fx"], day), unsafe_allow_html=True)

    st.markdown('<div class="lc-step">3. Send the day</div>', unsafe_allow_html=True)
    st.button("End the day 🌙", key="endday", disabled=not ready, type="primary", use_container_width=True,
              on_click=end_day, args=(g,))
    if not ready:
        need = (len(evs) - len(ui["choices"])) + (2 - len(ui["acts"]))
        st.caption(f"Almost there: {need} more tap{'s' if need != 1 else ''} to go.")


def report(g, ui, go_home):
    r, day = ui["report"], ui["report"]["day"]
    titles = {EVENTS[e]["title"]: (e, c) for e, c in r["evs"]}
    hit = any(l.startswith("Storm hit") for l in r["lines"])
    bad = g["over"] and not g["won"]
    mood = "worry" if hit or bad else "joy" if g["won"] or min(r["after"]["power"], r["after"]["oxygen"]) >= 30 else "happy"
    if bad:
        text = "Oh no! Power or air ran out. Astronauts learn from every mission. Try again!"
    elif g["won"]:
        text = f"Mission complete! The crew is safe. You collected {g['science']} science points!"
    elif hit:
        text = "The storm got through! A stronger shield would help. Let's see why."
    else:
        text = "The shield held! Let's see what your choices did."
    st.markdown(CSS + header({**g, "day": day}) + tip(text, mood), unsafe_allow_html=True)
    st.markdown(f'<div class="lc-step">Day {day} report</div>', unsafe_allow_html=True)
    b, a = r["before"], r["after"]
    cols = st.columns(2)
    keys = [k for k in ("power", "oxygen", "shield", "food") if visible(k, day)]
    for i, k in enumerate(keys):
        cols[i % 2].markdown(meter(k, a[k], a[k] - b[k]), unsafe_allow_html=True)
    st.markdown(f'<div class="lc-sci">⭐ Science: {a["science"]} ({a["science"] - b["science"]:+d})</div>', unsafe_allow_html=True)
    st.markdown('<div class="lc-step">What caused what</div>', unsafe_allow_html=True)
    labels = ", ".join(ACTIONS[x]["label"] for x in r["acts"])
    st.markdown(f'<div class="lc-chain"><div>You picked: <b>{labels}</b></div></div>', unsafe_allow_html=True)
    for line in r["lines"]:
        head, _, rest = line.partition(": ")
        if head in titles:
            e, c = titles[head]
            html = (f'<div class="lc-chain"><div>{head}. You chose: <b>{EVENTS[e]["options"][c]["label"]}</b></div>'
                    f'<div class="arr">▼</div><div class="res">{rest}</div></div>')
        elif line.startswith("Sunshine"):
            html = f'<div class="lc-chain"><div>🌞 Morning sunshine</div><div class="arr">▼</div><div class="res">{line}</div></div>'
        elif line.startswith("Storm"):
            html = (f'<div class="lc-chain {"hit" if hit else "ok"}"><div>☀️ The Sun\'s storm arrived</div>'
                    f'<div class="arr">▼</div><div class="res">{line}</div></div>')
        else:
            html = f'<div class="lc-chain"><div>Surprise!</div><div class="arr">▼</div><div class="res">{line}</div></div>'
        st.markdown(html, unsafe_allow_html=True)
    if g["over"]:
        st.button("Back to home", key="home", type="primary", use_container_width=True, on_click=go_home)
    else:
        st.button(f"Start Moon day {g['day']} 🚀", key="next", type="primary", use_container_width=True,
                  on_click=next_day, args=(g,))


def render_day(g, go_home):
    if g.get("ui") and g["ui"]["report"]:
        report(g, g["ui"], go_home)
        return
    if g.get("ui") is None or g.get("_started") != g["day"]:
        start_day(g)
        g["_started"] = g["day"]
        g["ui"] = {"choices": {}, "acts": [], "report": None}
    plan(g, g["ui"])