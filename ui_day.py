import time
import streamlit as st
from engine import (
    ACTIONS, DIFFICULTY, EVENTS, UNLOCK, DAYS, DAY_FACTS,
    available, start_day, resolve_morning, resolve_event, resolve_end_of_day,
)

NAMES = {"power": ("⚡", "Power"), "oxygen": ("💨", "Air"), "shield": ("🛡️", "Shield"),
         "food": ("🌱", "Food"), "science": ("⭐", "Science"), "panel": ("🔆", "Panels")}
FACTOR = {"power": "power", "oxygen": "life", "shield": "shield", "food": "food"}

CSS = """<style>
@keyframes cardPullUp {
  0% { opacity: 0; transform: translateY(26px) scale(0.97); }
  100% { opacity: 1; transform: translateY(0) scale(1); }
}
@keyframes floatSlow {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-7px); }
}
@keyframes pulseGlow {
  0%, 100% { box-shadow: 0 0 0 0 rgba(255, 201, 60, 0.35); }
  50% { box-shadow: 0 0 22px 4px rgba(255, 201, 60, 0.55); }
}
.lc-top{display:flex;align-items:center;justify-content:space-between;gap:12px;color:#fff;font-weight:700;font-size:1.25rem;margin-bottom:.7rem}
.lc-dots{display:flex;gap:8px}.lc-dots i{width:16px;height:16px;border-radius:50%;background:#3C3489;border:2px solid #7fe7ff;display:inline-block}
.lc-dots i.done{background:#7fe7ff}.lc-dots i.now{background:#ffc93c;border-color:#ffc93c;transform:scale(1.25)}
.lc-lvl{background:#7fe7ff;color:#26215C;border-radius:999px;padding:4px 16px;font-size:.95rem}
.lc-hud{background:#1d1849;border:1px solid #534ab7;border-radius:18px;padding:12px 16px;margin-bottom:1rem}
.lc-m{margin-bottom:.35rem}.lc-mh{display:flex;justify-content:space-between;color:#fff;font-weight:700;font-size:1rem}
.lc-bar{height:14px;background:#3C3489;border-radius:999px;overflow:hidden}.lc-bar i{display:block;height:100%;border-radius:999px;transition:width .5s}
.lc-low{color:#ffb347;font-size:.8rem;font-weight:700;min-height:1rem}
.lc-sci{color:#ffd966;font-weight:800;font-size:1.05rem;text-align:right}
.lc-stage{animation:cardPullUp .45s cubic-bezier(.22,1,.36,1) both;background:#3C3489;border:2px solid #7F77DD;border-radius:22px;padding:20px 22px;margin-bottom:1rem;color:#fff}
.lc-badge{display:inline-block;background:#ffc93c;color:#1b1340;font-weight:800;font-size:.85rem;padding:4px 12px;border-radius:999px;text-transform:uppercase;letter-spacing:.5px;margin-bottom:.5rem}
.lc-title{font-size:1.65rem;font-weight:800;color:#fff;margin:.2rem 0 .4rem}
.lc-sub{font-size:1.1rem;color:#EEEDFE;line-height:1.45;margin-bottom:.8rem}
.lc-art{background:#191442;border:1px solid #534ab7;border-radius:18px;padding:10px;text-align:center;margin-bottom:.8rem}
.lc-art svg{width:100%;max-height:190px;display:block;margin:0 auto}
.lc-choice-card{animation:cardPullUp .5s cubic-bezier(.22,1,.36,1) both;background:#26215C;border:2px solid #7fe7ff;border-radius:18px;padding:14px 16px;margin-bottom:.5rem;min-height:108px}
.lc-choice-card b{color:#fff;font-size:1.12rem;display:block;margin-bottom:6px}
.lc-chip{display:inline-block;border-radius:999px;padding:3px 10px;margin:2px 4px 2px 0;font-size:.85rem;font-weight:700}
.lc-chip.up{background:#1d6b3f;color:#d6ffe6}.lc-chip.dn{background:#7a2b3a;color:#ffe0e0}.lc-chip.wait{background:#5a4d19;color:#ffe999}
.lc-timer-wrap{background:#191442;border:1px solid #534ab7;border-radius:14px;padding:8px 14px;margin-bottom:.9rem}
.lc-timer-top{display:flex;justify-content:space-between;color:#EEEDFE;font-weight:700;font-size:.95rem;margin-bottom:5px}
.lc-timer-bar{height:10px;background:#3C3489;border-radius:999px;overflow:hidden}
.lc-timer-bar i{display:block;height:100%;border-radius:999px;transition:width .35s linear}
.lc-box-res{animation:cardPullUp .4s ease-out both;background:#1d1849;border:2px solid #4cd97b;border-radius:18px;padding:16px 18px;margin-bottom:.8rem;color:#fff}
.lc-box-res.warn{border-color:#ff9a9a}
.lc-box-why{animation:cardPullUp .55s ease-out both;background:#26215C;border-left:6px solid #7fe7ff;border-radius:16px;padding:14px 18px;margin-bottom:.8rem;color:#EEEDFE}
.lc-box-dyk{animation:cardPullUp .7s ease-out both;background:#382b6e;border:2px dashed #ffc93c;border-radius:16px;padding:14px 18px;margin-bottom:1rem;color:#fff}
.lc-box-why b,.lc-box-dyk b{display:block;font-size:1.05rem;margin-bottom:4px}
.lc-box-why b{color:#7fe7ff}.lc-box-dyk b{color:#ffc93c}
.lc-tip{display:flex;align-items:center;gap:14px;margin:.6rem 0}.lc-tip svg{width:76px;flex:none;overflow:visible;animation:floatSlow 3s ease-in-out infinite}
.lc-say{background:#fff;color:#26215C;border-radius:18px;padding:11px 15px;font-weight:600;font-size:1rem;line-height:1.35}
button[data-testid="stBaseButton-primary"]{background:#FFC93C!important;color:#1b1340!important;box-shadow:0 4px 0 #d9961b;animation:pulseGlow 2.5s infinite}
div.stButton>button{min-height:3.1rem;font-size:1.05rem}
</style>"""

FACES = {
 "happy": '<ellipse cx="50" cy="52" rx="5" ry="7" fill="#7fe7ff"/><ellipse cx="70" cy="52" rx="5" ry="7" fill="#7fe7ff"/><path d="M52 64q8 7 16 0" stroke="#7fe7ff" stroke-width="3" fill="none" stroke-linecap="round"/>',
 "worry": '<circle cx="50" cy="52" r="6.5" fill="#ffb347"/><circle cx="70" cy="52" r="6.5" fill="#ffb347"/><circle cx="50" cy="53" r="2.4" fill="#1e2a78"/><circle cx="70" cy="53" r="2.4" fill="#1e2a78"/><path d="M52 67q4-4 8 0q4 4 8 0" stroke="#ffb347" stroke-width="3" fill="none" stroke-linecap="round"/>',
 "joy": '<path d="M50 44l2.4 5.2 5.6.6-4.2 3.8 1.2 5.6-5-2.8-5 2.8 1.2-5.6-4.2-3.8 5.6-.6z" fill="#ffd966"/><path transform="translate(20 0)" d="M50 44l2.4 5.2 5.6.6-4.2 3.8 1.2 5.6-5-2.8-5 2.8 1.2-5.6-4.2-3.8 5.6-.6z" fill="#ffd966"/><path d="M49 62q11 13 22 0z" fill="#7fe7ff"/>',
}


def itiri(mood="happy"):
    return ('<svg viewBox="0 0 120 150" aria-label="Itiri"><path d="M60 26v-12" stroke="#fff" stroke-width="3"/>'
            '<circle cx="60" cy="9" r="6" fill="#ffc93c"/><rect x="40" y="118" width="14" height="24" rx="7" fill="#fff"/>'
            '<rect x="66" y="118" width="14" height="24" rx="7" fill="#fff"/><rect x="32" y="80" width="56" height="46" rx="22" fill="#ff8a3d"/>'
            '<rect x="84" y="88" width="12" height="30" rx="6" fill="#fff"/><rect x="24" y="88" width="12" height="30" rx="6" fill="#fff"/>'
            '<circle cx="60" cy="102" r="7" fill="#ffc93c"/><circle cx="60" cy="52" r="38" fill="#fff"/>'
            '<ellipse cx="60" cy="54" rx="29" ry="25" fill="#1e2a78"/>' + FACES[mood] + '</svg>')


EVENT_ART = {
 "dust": '<svg viewBox="0 0 420 160"><rect width="420" height="160" fill="#131033"/><ellipse cx="210" cy="155" rx="230" ry="35" fill="#5e5a80"/><g transform="translate(120,65) skewX(-18)"><rect width="140" height="52" rx="6" fill="#2c6bed" stroke="#7fe7ff" stroke-width="3"/><line x1="46" y1="0" x2="46" y2="52" stroke="#7fe7ff" stroke-width="2"/><line x1="93" y1="0" x2="93" y2="52" stroke="#7fe7ff" stroke-width="2"/><line x1="0" y1="26" x2="140" y2="26" stroke="#7fe7ff" stroke-width="2"/></g><circle cx="70" cy="65" r="22" fill="#9c96bd" opacity=".45"><animate attributeName="cx" values="40;370" dur="3.5s" repeatCount="indefinite"/></circle><circle cx="140" cy="95" r="28" fill="#b8b2d8" opacity=".35"><animate attributeName="cx" values="10;390" dur="2.8s" repeatCount="indefinite"/></circle></svg>',
 "night": '<svg viewBox="0 0 420 160"><rect width="420" height="160" fill="#0c0a24"/><circle cx="75" cy="35" r="3" fill="#fff"/><circle cx="150" cy="24" r="2" fill="#7fe7ff"/><circle cx="330" cy="40" r="3" fill="#ffd966"/><circle cx="370" cy="22" r="2" fill="#fff"/><path d="M295 28a26 26 0 1 0 24 36 21 21 0 1 1-24-36z" fill="#ffc93c"/><rect x="165" y="55" width="90" height="52" rx="10" fill="none" stroke="#7fe7ff" stroke-width="4"/><rect x="255" y="71" width="10" height="20" rx="3" fill="#7fe7ff"/><rect x="173" y="63" width="48" height="36" rx="5" fill="#ffc93c"><animate attributeName="width" values="65;25;65" dur="3s" repeatCount="indefinite"/></rect></svg>',
 "air": '<svg viewBox="0 0 420 160"><rect width="420" height="160" fill="#131033"/><rect x="145" y="32" width="130" height="96" rx="18" fill="#2e276b" stroke="#7fe7ff" stroke-width="3"/><circle cx="210" cy="80" r="28" fill="#191442" stroke="#ffb347" stroke-width="4"/><path d="M210 58v44M188 80h44" stroke="#7fe7ff" stroke-width="5" stroke-linecap="round"><animateTransform attributeName="transform" type="rotate" from="0 210 80" to="360 210 80" dur="4s" repeatCount="indefinite"/></path><circle cx="305" cy="95" r="8" fill="#7fe7ff" opacity=".7"><animate attributeName="cy" values="110;35" dur="2.2s" repeatCount="indefinite"/></circle><circle cx="325" cy="70" r="6" fill="#7fe7ff" opacity=".5"><animate attributeName="cy" values="105;30" dur="2.7s" repeatCount="indefinite"/></circle></svg>',
 "co2": '<svg viewBox="0 0 420 160"><rect width="420" height="160" fill="#131033"/><rect x="130" y="30" width="160" height="100" rx="16" fill="#2b2363" stroke="#ff9a9a" stroke-width="3"/><line x1="150" y1="55" x2="270" y2="55" stroke="#ff9a9a" stroke-width="6" stroke-linecap="round"/><line x1="150" y1="80" x2="270" y2="80" stroke="#ffb347" stroke-width="6" stroke-linecap="round"/><line x1="150" y1="105" x2="270" y2="105" stroke="#ff9a9a" stroke-width="6" stroke-linecap="round"/><text x="85" y="75" fill="#ffb347" font-size="18" font-weight="bold">CO₂</text><text x="305" y="100" fill="#ff9a9a" font-size="18" font-weight="bold">CO₂</text></svg>',
 "flare": '<svg viewBox="0 0 420 160"><rect width="420" height="160" fill="#131033"/><circle cx="70" cy="80" r="46" fill="#ff8a3d"/><circle cx="70" cy="80" r="36" fill="#ffc93c"/><path d="M108 55 Q175 15 190 78 Q170 120 112 95" fill="none" stroke="#ff6b6b" stroke-width="6"><animate attributeName="stroke-width" values="4;10;4" dur="1.6s" repeatCount="indefinite"/></path><circle cx="345" cy="85" r="32" fill="#8b85b1"/><path d="M295 45 Q275 85 295 125" fill="none" stroke="#7fe7ff" stroke-width="5" stroke-linecap="round"/></svg>',
 "particles": '<svg viewBox="0 0 420 160"><rect width="420" height="160" fill="#131033"/><path d="M270 135 A60 60 0 0 1 390 135 Z" fill="#4e469c" stroke="#7fe7ff" stroke-width="3"/><line x1="30" y1="45" x2="140" y2="65" stroke="#ffc93c" stroke-width="4" stroke-linecap="round"><animate attributeName="x1" values="10;180" dur="1.2s" repeatCount="indefinite"/><animate attributeName="x2" values="90;260" dur="1.2s" repeatCount="indefinite"/></line><line x1="20" y1="95" x2="130" y2="110" stroke="#ff6b6b" stroke-width="4" stroke-linecap="round"><animate attributeName="x1" values="10;170" dur="1.5s" repeatCount="indefinite"/><animate attributeName="x2" values="90;250" dur="1.5s" repeatCount="indefinite"/></line></svg>',
 "garden": '<svg viewBox="0 0 420 160"><rect width="420" height="160" fill="#131033"/><rect x="125" y="22" width="170" height="12" rx="6" fill="#ff66d9"/><polygon points="145,34 275,34 305,125 115,125" fill="#ff66d9" opacity=".16"/><rect x="120" y="118" width="180" height="22" rx="8" fill="#6b4c3b"/><path d="M165 118 Q165 82 145 78 M165 98 Q182 82 192 88" stroke="#4cd97b" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M245 118 Q245 75 225 72 M245 94 Q264 78 274 85" stroke="#4cd97b" stroke-width="5" fill="none" stroke-linecap="round"/></svg>',
 "harvest": '<svg viewBox="0 0 420 160"><rect width="420" height="160" fill="#131033"/><rect x="115" y="112" width="190" height="24" rx="8" fill="#6b4c3b"/><path d="M160 112 V72 M210 112 V65 M260 112 V74" stroke="#4cd97b" stroke-width="5" stroke-linecap="round"/><circle cx="152" cy="82" r="10" fill="#ff6b6b"/><circle cx="218" cy="75" r="11" fill="#ff6b6b"/><circle cx="253" cy="84" r="10" fill="#ffc93c"/></svg>',
 "advice": '<svg viewBox="0 0 420 160"><rect width="420" height="160" fill="#131033"/><circle cx="80" cy="80" r="34" fill="#2c6bed"/><path d="M62 65 Q80 55 95 72 Q85 95 65 88 Z" fill="#4cd97b"/><circle cx="345" cy="80" r="24" fill="#9c96bd"/><path d="M135 80 H295" stroke="#ffc93c" stroke-width="4" stroke-dasharray="10 10"><animate attributeName="stroke-dashoffset" from="40" to="0" dur="1.4s" repeatCount="indefinite"/></path></svg>',
 "blackout": '<svg viewBox="0 0 420 160"><rect width="420" height="160" fill="#131033"/><path d="M160 125 L195 75 L230 125 Z" fill="#7fe7ff"/><path d="M155 65 Q195 105 235 65" fill="none" stroke="#fff" stroke-width="5"/><polyline points="245,45 225,75 250,75 230,108" fill="none" stroke="#ffc93c" stroke-width="5" stroke-linecap="round"><animate attributeName="opacity" values="1;0.2;1" dur="0.9s" repeatCount="indefinite"/></polyline></svg>',
}


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


def header(g):
    dots = "".join(f'<i class="{"done" if i < g["day"] else "now" if i == g["day"] else ""}"></i>' for i in range(1, 6))
    return f'<div class="lc-top"><div>🌙 Moon Day {min(g["day"], 5)} of 5</div><div class="lc-dots">{dots}</div><div class="lc-lvl">{g["level"].title()}</div></div>'


def hud(g, day):
    keys = [k for k in ("power", "oxygen", "shield", "food") if visible(k, day)]
    cols = st.columns(len(keys) + 1)
    for col, k in zip(cols[:-1], keys):
        val = g[k]
        color = "#4cd97b" if val >= 60 else "#ffc93c" if val >= 30 else "#ff6b6b"
        low = "⚠️ Low!" if val < 30 else " "
        col.markdown(
            f'<div class="lc-m"><div class="lc-mh"><span>{NAMES[k][0]} {NAMES[k][1]}</span><b>{val}</b></div>'
            f'<div class="lc-bar"><i style="width:{val}%;background:{color}"></i></div><div class="lc-low">{low}</div></div>',
            unsafe_allow_html=True,
        )
    cols[-1].markdown(
        f'<div class="lc-sci">⭐ Science: {g["science"]}<br><span style="color:#CECBF6;font-size:.85rem">🔆 Panels: {g["panel"]}%</span></div>',
        unsafe_allow_html=True,
    )


def init_day_ui(g):
    start_day(g)
    g["_started"] = g["day"]
    sun, sun_msg = resolve_morning(g)
    g["ui"] = {
        "phase": "briefing",
        "ev_idx": 0,
        "turn_start": time.time(),
        "records": [],
        "last_rec": None,
        "acts": [],
        "sun": sun,
        "sun_msg": sun_msg,
        "storm_lines": [],
        "report_day": g["day"],
    }


def choose_event_option(g, ev_id, opt_id, timed_out=False):
    ui = g["ui"]
    rec = resolve_event(g, ev_id, opt_id)
    rec["timed_out"] = timed_out
    ui["records"].append(rec)
    ui["last_rec"] = rec
    ui["phase"] = "event_result"


def next_from_event_result(g):
    ui = g["ui"]
    ui["ev_idx"] += 1
    if ui["ev_idx"] < len(g["today"]):
        ui["phase"] = "event_choice"
        ui["turn_start"] = time.time()
    else:
        ui["phase"] = "actions"


def toggle_action(ui, a):
    if a in ui["acts"]:
        ui["acts"].remove(a)
    elif len(ui["acts"]) < 2:
        ui["acts"].append(a)
    else:
        st.toast("Pick 2 actions! Tap a selected one to swap it.", icon="👆")


def finish_day_actions(g):
    ui = g["ui"]
    ui["storm_lines"] = resolve_end_of_day(g, list(ui["acts"]), ui["records"])
    ui["phase"] = "storm_result"


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
        f'<div class="lc-timer-wrap"><div class="lc-timer-top"><span>⏱️ Decision Timer</span><span>{rem}s left</span></div>'
        f'<div class="lc-timer-bar"><i style="width:{pct}%;background:{bar_color}"></i></div></div>',
        unsafe_allow_html=True,
    )
    if rem <= 0:
        opts = EVENTS[ev_id]["options"]
        fallback = next((k for k, v in opts.items() if v.get("safe")), list(opts)[0])
        choose_event_option(g, ev_id, fallback, timed_out=True)
        st.rerun()


def render_briefing(g, ui):
    day = g["day"]
    d = DAYS[day - 1]
    fact = DAY_FACTS[day]
    st.markdown(
        f'<div class="lc-stage"><span class="lc-badge">Morning Mission Briefing</span>'
        f'<div class="lc-title">☀️ Real NASA Solar Report — {7 + day} May 2024</div>'
        f'<div class="lc-sub">NASA satellites detected <b>{d["flares"]} solar flares</b> on this date. '
        f'The strongest flare was class <b>{d["max_class"]}</b>.</div>'
        f'<div class="lc-box-why"><b>{fact["unlock"]}</b>{ui["sun_msg"]}</div>'
        f'<div class="lc-box-dyk"><b>🔭 Did You Know?</b>{fact["fact"]}</div></div>',
        unsafe_allow_html=True,
    )
    if st.button(f"Start Day {day} Events 🚀", key="start_events", type="primary", use_container_width=True):
        ui["phase"] = "event_choice"
        ui["turn_start"] = time.time()
        st.rerun()


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
            risk_badge = '<span class="lc-chip wait">🎲 50% Dust Scratch Risk</span>' if "risk" in opt else ""
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


def render_event_result(g, ui):
    day = g["day"]
    rec = ui["last_rec"]
    ev = EVENTS[rec["ev_id"]]
    opt = ev["options"][rec["choice"]]
    has_bad = any(v < 0 for k, v in rec["deltas"].items() if k in ("power", "oxygen", "shield", "food", "panel"))
    mood = "worry" if (has_bad or rec["extra"]) else "joy"

    delta_html = chips(rec["deltas"], day) or '<span class="lc-chip wait">⏳ Effect arrives after the storm!</span>'
    extra_html = "".join(f"<p style='color:#ffb347;font-weight:700;margin:6px 0 0'>⚠️ {x}</p>" for x in rec["extra"])
    timeout_note = "<p style='color:#ffc93c;font-weight:700;margin:0 0 6px'>⏱️ Time ran out! Itiri quickly picked the safest option for you.</p>" if rec.get("timed_out") else ""

    st.markdown(
        f'<div class="lc-box-res {"warn" if rec["extra"] else ""}">'
        f'<span class="lc-badge">Consequence</span>{timeout_note}'
        f'<div class="lc-title" style="font-size:1.35rem">You chose: {opt["label"]}</div>'
        f'<div class="lc-sub">{rec["note"]}</div>'
        f'<div>{delta_html}</div>{extra_html}</div>'
        f'<div class="lc-box-why"><b>🧠 Why Did That Happen?</b>{rec["explain"]}</div>'
        f'<div class="lc-box-dyk"><b>🔭 Did You Know?</b>{rec["did_you_know"]}</div>'
        f'<div class="lc-tip">{itiri(mood)}<div class="lc-say">Great job thinking like a NASA flight controller, Commander!</div></div>',
        unsafe_allow_html=True,
    )

    is_last = (ui["ev_idx"] + 1) >= len(g["today"])
    btn_label = "Pick Today's 2 Base Actions ➔" if is_last else f"Next Event ({ui['ev_idx'] + 2} of {len(g['today'])}) ➔"
    st.button(btn_label, key=f"cont_{day}_{ui['ev_idx']}", type="primary", use_container_width=True,
              on_click=next_from_event_result, args=(g,))


def render_actions(g, ui):
    day = g["day"]
    acts = available(g)
    st.markdown(
        f'<div class="lc-stage"><span class="lc-badge">Base Operations</span>'
        f'<div class="lc-title">🛠️ Pick 2 Crew Actions ({len(ui["acts"])}/2 selected)</div>'
        f'<div class="lc-sub">Spend your remaining energy to prepare the Moon base before the solar storm hits!</div></div>',
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

    st.markdown(
        '<div class="lc-box-dyk"><b>🔭 Did You Know?</b>On a real Moon base, every system is connected: '
        'solar panels power the water-splitter that makes oxygen, and astronauts recycle almost every drop of water!</div>',
        unsafe_allow_html=True,
    )
    ready = len(ui["acts"]) == 2
    st.button(
        "End Day & Face the Solar Storm ☀️🛡️",
        key=f"endday_{day}",
        disabled=not ready,
        type="primary",
        use_container_width=True,
        on_click=finish_day_actions,
        args=(g,),
    )


def render_storm_result(g, ui, go_home):
    day = ui["report_day"]
    hit = any("Storm hit" in line for line in ui["storm_lines"])
    bad = g["over"] and not g["won"]
    mood = "worry" if (hit or bad) else "joy"

    if bad:
        headline = "Mission Alert: Life Support Ran Low!"
        msg = "Power, air, or food hit zero. Real NASA teams test missions many times—try again with what you learned!"
    elif g["won"]:
        headline = f"🎉 Mission Complete! {g['science']} Science Points!"
        msg = "You guided your crew safely through all 5 days of the May 2024 solar superstorm!"
    elif hit:
        headline = "☀️ The Solar Storm Pierced the Shield!"
        msg = "The real flare was stronger than your shield today, so extra power was lost protecting the crew."
    else:
        headline = "🛡️ Shield Held Strong!"
        msg = "Your shield blocked the solar radiation and kept the Moon base safe!"

    lines_html = "".join(f"<p style='margin:6px 0;font-size:1.05rem'>• {line}</p>" for line in ui["storm_lines"])
    st.markdown(
        f'<div class="lc-box-res {"warn" if (hit or bad) else ""}">'
        f'<span class="lc-badge">End of Moon Day {day}</span>'
        f'<div class="lc-title">{headline}</div>'
        f'<div class="lc-sub">{msg}</div>{lines_html}</div>'
        f'<div class="lc-tip">{itiri(mood)}<div class="lc-say">{msg}</div></div>',
        unsafe_allow_html=True,
    )

    if g["over"]:
        st.button("Back to Mission Control Home 🏠", key="go_home_btn", type="primary", use_container_width=True, on_click=go_home)
    else:
        if st.button(f"Continue to Moon Day {g['day']} 🚀", key=f"next_day_{day}", type="primary", use_container_width=True):
            g["ui"] = None
            st.rerun()


def render_day(g, go_home):
    st.markdown(CSS, unsafe_allow_html=True)
    if g.get("ui") is None or g.get("_started") != g["day"] and g["ui"].get("phase") != "storm_result":
        init_day_ui(g)
    ui = g["ui"]
    display_day = ui["report_day"] if ui["phase"] == "storm_result" else g["day"]
    st.markdown(header({**g, "day": display_day}), unsafe_allow_html=True)
    hud(g, display_day)

    phase = ui["phase"]
    if phase == "briefing":
        render_briefing(g, ui)
    elif phase == "event_choice":
        render_event_choice(g, ui)
    elif phase == "event_result":
        render_event_result(g, ui)
    elif phase == "actions":
        render_actions(g, ui)
    elif phase == "storm_result":
        render_storm_result(g, ui, go_home)