import streamlit as st
import streamlit.components.v1 as components
from ui_home import HOME_HTML
from engine import new_game
from ui_day import render_day

st.set_page_config(page_title="LUNA-CTRL", page_icon="🌙", layout="wide",
                   initial_sidebar_state="collapsed")

st.markdown("""<style>
header[data-testid="stHeader"], footer {display: none;}
.stApp {background: #26215C;}
.block-container {max-width: 100% !important; padding: 0 0 1rem 0 !important;}
.stApp iframe {width: 100% !important; height: auto !important; aspect-ratio: 16/9;
               max-height: calc(100vh - 10px); display: block; border: none;}
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
</style>""", unsafe_allow_html=True)

LEVELS = {"junior", "commander", "expert"}

if "screen" not in st.session_state:
    st.session_state.screen = "home"


def go(screen):
    st.session_state.screen = screen


def start_game(level_key):
    st.session_state.game = new_game(level=level_key)
    st.session_state.screen = "day"


level = st.query_params.get("level")
if level in LEVELS and st.session_state.screen == "home":
    start_game(level)
    st.query_params.clear()


def home():
    components.html(HOME_HTML, height=600)
    for lv in ("junior", "commander", "expert"):      # hidden buttons: the home page clicks one of them
        st.button(lv, key=f"start_{lv}", on_click=start_game, args=(lv,))
    st.caption("Real storm data: NASA DONKI (archived). Everything else is simulated.")
    

def day():
    g = st.session_state.game
    with st.container(key="page"):
        render_day(g, lambda: go("home"))


{"home": home, "day": day}[st.session_state.screen]()