import streamlit as st
import streamlit.components.v1 as components
from ui_home import HOME_HTML
from engine import new_game
from ui_day import render_day
from sound_fx import play_sound_engine

st.set_page_config(page_title="LUNA-CTRL", page_icon="🌙", layout="wide",
                   initial_sidebar_state="collapsed")

st.markdown("""<style>
header[data-testid="stHeader"], footer {display: none;}
.stApp {background: #26215C;}
.block-container {max-width: 100% !important; padding: 0 0 1rem 0 !important;}
.stApp iframe {width: 100% !important; height: auto !important; aspect-ratio: 16/9;
               max-height: calc(100vh - 10px); display: block; border: none;}
/* Keep the invisible audio synthesizer iframe hidden on both Home and Day screens */
.stApp iframe[height="0"] {display: none !important; height: 0 !important;
                          width: 0 !important; aspect-ratio: auto !important;}
[data-testid="stCaptionContainer"] p {color: #CECBF6; text-align: center;}
[data-testid="stExpander"] {background: #3C3489; border: 1px solid #7F77DD;
                            border-radius: 12px; margin: 0.5rem 2rem;}
[data-testid="stExpander"] * {color: #ffffff;}
.st-key-page {max-width: 900px; margin: 0 auto; padding: 2rem 1.5rem;}
.st-key-page h1, .st-key-page h2, .st-key-page h3, .st-key-page p {color: #ffffff;}
div.stButton > button {border-radius: 999px; font-weight: 700; border: none;
                       background: #EEEDFE; color: #26215C;}
div.stButton > button p {color: inherit !important;}
.st-key-start_junior, .st-key-start_commander, .st-key-start_expert {display: none;}
/* Floating top-right music toggle on the home screen */
.st-key-home_sound {
    position: fixed;
    top: 14px;
    right: 18px;
    z-index: 9999;
    width: auto !important;
}
.st-key-home_sound button {
    background: rgba(38, 33, 92, 0.88) !important;
    color: #EEEDFE !important;
    border: 2px solid #7fe7ff !important;
    padding: 0.35rem 1rem !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
}
</style>""", unsafe_allow_html=True)

LEVELS = {"junior", "commander", "expert"}

if "screen" not in st.session_state:
    st.session_state.screen = "home"

if "muted" not in st.session_state:
    st.session_state.muted = False


def go(screen):
    st.session_state.screen = screen


def start_game(level_key):
    st.session_state.game = new_game(level=level_key)
    st.session_state.screen = "day"


def toggle_home_sound():
    st.session_state.muted = not st.session_state.muted


level = st.query_params.get("level")
if level in LEVELS and st.session_state.screen == "home":
    start_game(level)
    st.query_params.clear()


def home():
    snd_label = "🔇 Muted" if st.session_state.muted else "🔊 Music ON"
    st.button(snd_label, key="home_sound", on_click=toggle_home_sound)
    components.html(HOME_HTML, height=600)
    play_sound_engine("home", st.session_state.muted, "home_screen")
    for lv in ("junior", "commander", "expert"):      # hidden buttons: the home page clicks one of them
        st.button(lv, key=f"start_{lv}", on_click=start_game, args=(lv,))
    st.caption("Real storm data: NASA DONKI (archived). Everything else is simulated.")


def day():
    g = st.session_state.game
    with st.container(key="page"):
        render_day(g, lambda: go("home"))


{"home": home, "day": day}[st.session_state.screen]()