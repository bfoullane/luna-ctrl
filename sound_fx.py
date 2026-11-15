import streamlit.components.v1 as components


def play_sound_engine(cue: str, muted: bool, play_id: str):
    """Renders an invisible Web Audio synthesizer for cheerful, copyright-free space music & SFX."""
    muted_js = "true" if muted else "false"
    html = f"""
    <script>
    (function() {{
      const MUTED = {muted_js};
      const CUE = "{cue}";
      const PLAY_ID = "{play_id}";

      // Persist AudioContext and music loop on parent window across Streamlit reruns
      const win = window.parent || window;
      const AudioCtx = win.AudioContext || win.webkitAudioContext;
      if (!AudioCtx) return;

      if (!win._lunaAudio) {{
        win._lunaAudio = {{
          ctx: new AudioCtx(),
          musicGain: null,
          musicStarted: false,
          muted: MUTED,
          step: 0,
          nextNoteTime: 0,
          lastPlayId: "",
          pendingCue: ""
        }};
      }}

      const state = win._lunaAudio;
      state.muted = MUTED;
      const ctx = state.ctx;

      // Play a single cheerful marimba/celesta note routed to destination or music bus
      function playPluck(freq, when, duration, vol = 0.14, dest = null, bright = true) {{
        if (state.muted || !freq) return;
        const target = dest || ctx.destination;

        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = "triangle";
        osc.frequency.setValueAtTime(freq, when);

        gain.gain.setValueAtTime(0.0001, when);
        gain.gain.exponentialRampToValueAtTime(vol, when + 0.012);
        gain.gain.exponentialRampToValueAtTime(0.0001, when + duration);

        osc.connect(gain);
        gain.connect(target);
        osc.start(when);
        osc.stop(when + duration + 0.03);

        // Add a soft octave bell overtone for extra sparkle
        if (bright) {{
          const bell = ctx.createOscillator();
          const bellGain = ctx.createGain();
          bell.type = "sine";
          bell.frequency.setValueAtTime(freq * 2, when);

          bellGain.gain.setValueAtTime(0.0001, when);
          bellGain.gain.exponentialRampToValueAtTime(vol * 0.28, when + 0.01);
          bellGain.gain.exponentialRampToValueAtTime(0.0001, when + duration * 0.65);

          bell.connect(bellGain);
          bellGain.connect(target);
          bell.start(when);
          bell.stop(when + duration + 0.03);
        }}
      }}

      // Upbeat 32-step (4-bar) cheerful space-adventure melody loop
      function startCheerfulMusic() {{
        if (state.musicStarted) return;
        state.musicStarted = true;

        const master = ctx.createGain();
        master.gain.value = state.muted ? 0.0 : 0.55;
        master.connect(ctx.destination);
        state.musicGain = master;

        // Note frequencies (Hz)
        const N = {{
          G2: 98.00, B2: 123.47, C3: 130.81, D3: 146.83, F3: 174.61, G3: 196.00,
          G4: 392.00, C5: 523.25, D5: 587.33, E5: 659.25, G5: 783.99, A5: 880.00,
          B5: 987.77, C6: 1046.50
        }};

        // 32 eighth-note steps (bouncy C -> G -> F -> G progression)
        const melody = [
          N.E5, 0,    N.G5, N.A5, N.G5, N.E5, N.C5, N.D5,
          N.E5, 0,    N.G5, N.B5, N.A5, N.G5, N.E5, 0,
          N.A5, 0,    N.C6, N.A5, N.G5, N.E5, N.D5, N.E5,
          N.G5, N.E5, N.D5, N.E5, N.C5, 0,    N.G4, 0
        ];

        const bass = [
          N.C3, 0,    N.G3, 0,    N.C3, 0,    N.G3, 0,
          N.G2, 0,    N.D3, 0,    N.G2, 0,    N.D3, 0,
          N.F3, 0,    N.C3, 0,    N.F3, 0,    N.C3, 0,
          N.G2, 0,    N.B2, 0,    N.C3, 0,    0,    0
        ];

        const stepLen = 0.24; // ~125 BPM eighth notes
        state.nextNoteTime = ctx.currentTime + 0.05;

        win.setInterval(() => {{
          if (ctx.state !== "running" || state.muted) {{
            state.nextNoteTime = ctx.currentTime + 0.05;
            return;
          }}
          while (state.nextNoteTime < ctx.currentTime + 0.25) {{
            const i = state.step % melody.length;
            const mNote = melody[i];
            const bNote = bass[i];

            if (mNote) {{
              playPluck(mNote, state.nextNoteTime, 0.26, 0.11, state.musicGain, true);
            }}
            if (bNote) {{
              playPluck(bNote, state.nextNoteTime, 0.22, 0.09, state.musicGain, false);
            }}

            state.nextNoteTime += stepLen;
            state.step++;
          }}
        }}, 80);
      }}

      function triggerCue(name) {{
        if (state.muted || !name) return;
        const t = ctx.currentTime;

        if (name === "home") {{
          // Playful, upbeat space-cadet welcome fanfare!
          playPluck(392.00, t + 0.00, 0.16, 0.16); // G4
          playPluck(523.25, t + 0.10, 0.16, 0.16); // C5
          playPluck(659.25, t + 0.20, 0.16, 0.17); // E5
          playPluck(783.99, t + 0.30, 0.22, 0.18); // G5
          playPluck(659.25, t + 0.44, 0.14, 0.16); // E5
          playPluck(1046.5, t + 0.56, 0.45, 0.20); // C6!
        }} else if (name === "briefing") {{
          playPluck(523.25, t + 0.00, 0.20, 0.14);
          playPluck(659.25, t + 0.11, 0.20, 0.14);
          playPluck(783.99, t + 0.22, 0.32, 0.16);
        }} else if (name === "event") {{
          playPluck(440.00, t + 0.00, 0.16, 0.13);
          playPluck(659.25, t + 0.12, 0.24, 0.15);
        }} else if (name === "good") {{
          playPluck(523.25, t + 0.00, 0.16, 0.16);
          playPluck(659.25, t + 0.09, 0.16, 0.16);
          playPluck(783.99, t + 0.18, 0.18, 0.17);
          playPluck(1046.5, t + 0.27, 0.38, 0.19);
        }} else if (name === "warn") {{
          playPluck(329.63, t + 0.00, 0.20, 0.14, null, false);
          playPluck(261.63, t + 0.16, 0.32, 0.14, null, false);
        }} else if (name === "why") {{
          playPluck(587.33, t + 0.00, 0.18, 0.14);
          playPluck(880.00, t + 0.12, 0.28, 0.15);
        }} else if (name === "dyk") {{
          playPluck(698.46, t + 0.00, 0.16, 0.14);
          playPluck(880.00, t + 0.09, 0.16, 0.14);
          playPluck(1046.5, t + 0.18, 0.18, 0.15);
          playPluck(1318.5, t + 0.27, 0.36, 0.16);
        }} else if (name === "action") {{
          playPluck(783.99, t + 0.00, 0.14, 0.13);
        }} else if (name === "storm_ok") {{
          playPluck(523.25, t + 0.00, 0.22, 0.15);
          playPluck(659.25, t + 0.11, 0.22, 0.15);
          playPluck(783.99, t + 0.22, 0.40, 0.17);
        }} else if (name === "storm_hit") {{
          playPluck(196.00, t + 0.00, 0.26, 0.14, null, false);
          playPluck(146.83, t + 0.18, 0.38, 0.14, null, false);
        }} else if (name === "win") {{
          [523.25, 659.25, 783.99, 1046.5, 783.99, 1046.5].forEach((f, i) => {{
            playPluck(f, t + i * 0.12, 0.30, 0.18);
          }});
        }}
      }}

      function unlockAndPlay() {{
        if (ctx.state === "suspended") {{
          ctx.resume().then(() => {{
            startCheerfulMusic();
            if (state.pendingCue) {{
              const c = state.pendingCue;
              state.pendingCue = "";
              triggerCue(c);
            }}
          }}).catch(() => {{}});
        }} else {{
          startCheerfulMusic();
        }}
      }}

      function bindDoc(doc) {{
        if (!doc || doc._lunaBound) return;
        doc._lunaBound = true;
        doc.addEventListener("pointerdown", unlockAndPlay, {{ passive: true }});
        doc.addEventListener("keydown", unlockAndPlay, {{ passive: true }});
      }}

      // Bind parent document and child iframes (like HOME_HTML)
      bindDoc(win.document);
      let checks = 0;
      const pollIframes = win.setInterval(() => {{
        win.document.querySelectorAll("iframe").forEach((ifr) => {{
          try {{
            bindDoc(ifr.contentDocument || (ifr.contentWindow && ifr.contentWindow.document));
          }} catch (e) {{}}
        }});
        if (++checks > 20) win.clearInterval(pollIframes);
      }}, 250);

      unlockAndPlay();

      if (state.musicGain) {{
        state.musicGain.gain.setTargetAtTime(state.muted ? 0.0 : 0.55, ctx.currentTime, 0.08);
      }}

      if (state.lastPlayId !== PLAY_ID) {{
        state.lastPlayId = PLAY_ID;
        if (ctx.state === "suspended") {{
          state.pendingCue = CUE;
        }} else {{
          triggerCue(CUE);
        }}
      }}
    }})();
    </script>
    """
    components.html(html, height=0, width=0)