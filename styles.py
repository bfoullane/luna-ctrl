"""CSS for the day screens and the ending screens."""

CSS = """<style>
/* Hide the invisible audio component iframe inside .st-key-page */
.st-key-page iframe {
  height: 0 !important;
  min-height: 0 !important;
  aspect-ratio: auto !important;
  position: absolute !important;
  pointer-events: none !important;
  opacity: 0 !important;
}
@keyframes cardPullUp {
  0% { opacity: 0; transform: translateY(28px) scale(0.97); }
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
.lc-top{display:flex;align-items:center;justify-content:space-between;gap:12px;color:#fff;font-weight:700;font-size:1.2rem;margin-bottom:.6rem}
.lc-dots{display:flex;gap:8px}.lc-dots i{width:16px;height:16px;border-radius:50%;background:#3C3489;border:2px solid #7fe7ff;display:inline-block}
.lc-dots i.done{background:#7fe7ff}.lc-dots i.now{background:#ffc93c;border-color:#ffc93c;transform:scale(1.25)}
.lc-lvl{background:#7fe7ff;color:#26215C;border-radius:999px;padding:4px 16px;font-size:.95rem}
.lc-m{margin-bottom:.35rem}.lc-mh{display:flex;justify-content:space-between;color:#fff;font-weight:700;font-size:1rem}
.lc-bar{height:14px;background:#3C3489;border-radius:999px;overflow:hidden}.lc-bar i{display:block;height:100%;border-radius:999px;transition:width .5s}
.lc-low{color:#ffb347;font-size:.8rem;font-weight:700;min-height:1rem}
.lc-sci{color:#ffd966;font-weight:800;font-size:1.05rem;text-align:right}
.lc-stage{animation:cardPullUp .45s cubic-bezier(.22,1,.36,1) both;background:#3C3489;border:2px solid #7F77DD;border-radius:22px;padding:22px 24px;margin-bottom:1rem;color:#fff}
.lc-badge{display:inline-block;background:#ffc93c;color:#1b1340;font-weight:800;font-size:.85rem;padding:4px 12px;border-radius:999px;text-transform:uppercase;letter-spacing:.5px;margin-bottom:.6rem}
.lc-step-pills{float:right;font-size:.85rem;color:#CECBF6;font-weight:700}
.lc-title{font-size:1.65rem;font-weight:800;color:#fff;margin:.2rem 0 .5rem}
.lc-sub{font-size:1.15rem;color:#EEEDFE;line-height:1.5;margin-bottom:.9rem}
.lc-art{background:#191442;border:1px solid #534ab7;border-radius:18px;padding:10px;text-align:center;margin-bottom:.8rem}
.lc-art svg{width:100%;max-height:185px;display:block;margin:0 auto}
.lc-choice-card{animation:cardPullUp .5s cubic-bezier(.22,1,.36,1) both;background:#26215C;border:2px solid #7fe7ff;border-radius:18px;padding:14px 16px;margin-bottom:.5rem;min-height:108px}
.lc-choice-card b{color:#fff;font-size:1.12rem;display:block;margin-bottom:6px}
.lc-chip{display:inline-block;border-radius:999px;padding:4px 12px;margin:3px 5px 3px 0;font-size:.9rem;font-weight:700}
.lc-chip.up{background:#1d6b3f;color:#d6ffe6}.lc-chip.dn{background:#7a2b3a;color:#ffe0e0}.lc-chip.wait{background:#5a4d19;color:#ffe999}
.lc-timer-wrap{background:#191442;border:1px solid #534ab7;border-radius:14px;padding:8px 14px;margin-bottom:.9rem}
.lc-timer-top{display:flex;justify-content:space-between;color:#EEEDFE;font-weight:700;font-size:.95rem;margin-bottom:5px}
.lc-timer-bar{height:10px;background:#3C3489;border-radius:999px;overflow:hidden}
.lc-timer-bar i{display:block;height:100%;border-radius:999px;transition:width .35s linear}
.lc-box-res{animation:cardPullUp .45s cubic-bezier(.22,1,.36,1) both;background:#1d1849;border:2px solid #4cd97b;border-radius:22px;padding:22px 24px;margin-bottom:1rem;color:#fff}
.lc-box-res.warn{border-color:#ff9a9a}
.lc-box-why{animation:cardPullUp .45s cubic-bezier(.22,1,.36,1) both;background:#221c57;border:2px solid #7fe7ff;border-radius:22px;padding:22px 24px;margin-bottom:1rem;color:#EEEDFE}
.lc-box-dyk{animation:cardPullUp .45s cubic-bezier(.22,1,.36,1) both;background:#342669;border:2px dashed #ffc93c;border-radius:22px;padding:22px 24px;margin-bottom:1rem;color:#fff}
.lc-tip{display:flex;align-items:center;gap:16px;margin-top:1rem;background:rgba(255,255,255,0.06);border-radius:18px;padding:12px 16px}
.lc-tip svg{width:82px;flex:none;overflow:visible;animation:floatSlow 3s ease-in-out infinite}
.lc-say{background:#fff;color:#26215C;border-radius:18px;padding:12px 16px;font-weight:700;font-size:1.05rem;line-height:1.4}
button[data-testid="stBaseButton-primary"]{background:#FFC93C!important;color:#1b1340!important;box-shadow:0 4px 0 #d9961b;animation:pulseGlow 2.5s infinite}
div.stButton>button{min-height:3.1rem;font-size:1.05rem}
</style>"""

ENDING_CSS = """<style>
.lc-end{animation:cardPullUp .6s cubic-bezier(.22,1,.36,1) both;border-radius:26px;padding:26px 24px;margin-bottom:1rem;color:#fff;text-align:center}
.lc-end.win{background:radial-gradient(circle at 50% 0%,#5b4bc4 0%,#3C3489 55%,#26215C 100%);border:3px solid #ffc93c;box-shadow:0 0 40px rgba(255,201,60,.35)}
.lc-end.lose{background:#1d1849;border:3px solid #ff9a9a}
.lc-end .lc-tip{text-align:left}
.lc-patch{width:170px;display:block;margin:.4rem auto;animation:patchPop .9s cubic-bezier(.34,1.56,.64,1) both}
@keyframes patchPop{0%{transform:scale(0) rotate(-30deg)}100%{transform:scale(1) rotate(0)}}
.lc-rank{font-size:2.1rem;font-weight:900;color:#ffd966;margin:.2rem 0 .3rem}
.lc-bigsci{font-size:1.5rem;font-weight:800;color:#ffd966;margin:.4rem 0}
.lc-newbest{display:inline-block;background:#ffc93c;color:#1b1340;font-weight:800;border-radius:999px;padding:4px 16px;margin:.2rem 0 .6rem;animation:pulseGlow 2.5s infinite}
.lc-journey{display:flex;gap:10px;justify-content:center;margin:.9rem 0}
.lc-journey span{width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;background:#3C3489;border:2px solid #7fe7ff;color:#fff}
.lc-journey span.ok{background:#1d6b3f;border-color:#4cd97b}
.lc-journey span.bad{background:#7a2b3a;border-color:#ff9a9a}
.lc-journey span.na{opacity:.35}
.lc-chip.neu{background:#3C3489;color:#fff}
.lc-cause{background:#2c1a3d;border:2px dashed #ffb347;border-radius:18px;padding:14px 18px;margin:.8rem 0;text-align:left;color:#fff}
.lc-cause b{color:#ffd966;font-size:1.15rem}
.lc-confetti{position:fixed;inset:0;pointer-events:none;z-index:9998;overflow:hidden}
.lc-confetti i{position:absolute;top:-20px;width:10px;height:16px;border-radius:2px;opacity:0;animation:confettiFall linear 1 both}
@keyframes confettiFall{0%{transform:translateY(-20px) rotate(0);opacity:1}100%{transform:translateY(110vh) rotate(720deg);opacity:1}}
</style>"""