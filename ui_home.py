HOME_HTML = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&display=swap');
body{margin:0}
.lc{position:relative;height:100vh;min-height:480px;--m:24vh;overflow:hidden;font-family:'Fredoka',system-ui,sans-serif;color:#fff;background:linear-gradient(#0a0630 0%,#1b1060 55%,#3a2a8c 100%);display:flex;flex-direction:column;align-items:center;box-sizing:border-box;padding:3vh 20px 0}
.st{position:absolute;inset:0;background-repeat:repeat}
.s1{background-image:radial-gradient(1.5px 1.5px at 20px 30px,#fff,transparent),radial-gradient(1px 1px at 90px 70px,#fff,transparent),radial-gradient(1.5px 1.5px at 150px 20px,#cfe,transparent),radial-gradient(1px 1px at 60px 140px,#fff,transparent);background-size:200px 180px;animation:tw 3s ease-in-out infinite}
.s2{background-image:radial-gradient(2px 2px at 40px 60px,#ffe9a8,transparent),radial-gradient(2px 2px at 170px 110px,#fff,transparent),radial-gradient(1.5px 1.5px at 110px 160px,#bfe3ff,transparent);background-size:260px 210px;animation:tw 4.5s ease-in-out 1.2s infinite}
@keyframes tw{0%,100%{opacity:.35}50%{opacity:1}}
.shoot{position:absolute;top:18%;left:-10%;width:120px;height:2px;background:linear-gradient(90deg,transparent,#fff);transform:rotate(18deg);opacity:0;animation:sh 8s linear 2s infinite}
@keyframes sh{0%{left:-10%;opacity:0}3%{opacity:1}14%{left:70%;top:34%;opacity:0}100%{left:70%;opacity:0}}
.sun{position:absolute;top:36px;left:4%;width:clamp(84px,11vw,140px);aspect-ratio:1;border-radius:50%;background:radial-gradient(circle at 40% 38%,#fff6b0,#ffc93c 55%,#ff8a3d);box-shadow:0 0 60px 20px rgba(255,190,60,.55);animation:pulse 3s ease-in-out infinite,storm 12s infinite;z-index:1}
.sun:before,.sun:after{content:"";position:absolute;inset:-14px;border-radius:50%;border:3px dotted rgba(255,214,90,.8);animation:spin 18s linear infinite}
.sun:after{inset:-30px;border-style:dashed;border-color:rgba(255,214,90,.4);animation-direction:reverse}
.sun i{position:absolute;inset:0;border-radius:50%;border:2px solid rgba(255,201,60,.7);animation:ring 4s ease-out infinite}
.sun i+i{animation-delay:2s}
@keyframes storm{0%,44%{box-shadow:0 0 60px 20px rgba(255,190,60,.55)}48%,70%{box-shadow:0 0 120px 55px rgba(255,110,40,.9)}74%,100%{box-shadow:0 0 60px 20px rgba(255,190,60,.55)}}
@keyframes pulse{50%{transform:scale(1.06)}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes ring{from{transform:scale(1);opacity:.9}to{transform:scale(5);opacity:0}}
.earth{position:absolute;top:60px;right:7%;width:clamp(64px,8vw,100px);aspect-ratio:1;border-radius:50%;overflow:hidden;background:#2a7de1;box-shadow:0 0 30px rgba(120,190,255,.6),inset -14px -10px 24px rgba(0,0,40,.55);animation:bob 6s ease-in-out infinite;z-index:1}
.earth svg{position:absolute;top:0;left:0;width:200%;height:100%;animation:glide 22s linear infinite}
@keyframes glide{to{transform:translateX(-50%)}}
@keyframes bob{50%{transform:translateY(-10px)}}
.hero{position:relative;z-index:2;text-align:center;max-width:760px;display:flex;flex-direction:column;align-items:center;gap:1.8vh;margin-top:2vh}
.badge{font-size:15px;font-weight:500;padding:8px 18px;border-radius:999px;background:rgba(255,255,255,.14);border:1.5px solid rgba(255,255,255,.4)}
.logo{margin:0;font-size:clamp(44px,min(10vw,13vh),112px);font-weight:700;letter-spacing:2px;line-height:1;background:linear-gradient(#fff,#ffd966);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 6px 0 #6a3fd0);animation:float 4s ease-in-out infinite}
@keyframes float{50%{transform:translateY(-8px)}}
.tag{margin:0;font-size:clamp(18px,2.4vw,26px);font-weight:500;line-height:1.35;max-width:620px}
.lv{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin-top:6px}
.sr{position:absolute;opacity:0;width:1px;height:1px}
.chip{min-height:44px;box-sizing:border-box;padding:10px 20px;border-radius:999px;border:2px solid rgba(255,255,255,.55);background:rgba(255,255,255,.1);font-size:17px;font-weight:500;cursor:pointer;display:inline-flex;align-items:center;transition:transform .15s,background .15s}
.chip:hover{transform:translateY(-3px);background:rgba(255,255,255,.22)}
.sr:checked+.chip{background:#7fe7ff;color:#14104a;border-color:#7fe7ff;font-weight:700}
.sr:focus-visible+.chip{outline:3px solid #ffc93c;outline-offset:3px}
.row{display:flex;flex-wrap:wrap;justify-content:center;gap:16px;margin-top:8px}
.play{min-height:64px;padding:14px 46px;border:0;border-radius:999px;background:#ffc93c;color:#1b1340;font:700 clamp(24px,3vw,32px) 'Fredoka',sans-serif;box-shadow:0 7px 0 #d9961b;cursor:pointer;animation:beat 2.2s ease-in-out infinite;transition:transform .12s,box-shadow .12s}
.play:hover{transform:translateY(-4px) scale(1.05);box-shadow:0 11px 0 #d9961b;animation:none}
.play:active{transform:translateY(5px);box-shadow:0 2px 0 #d9961b}
@keyframes beat{50%{transform:scale(1.04)}}
.ghost{min-height:64px;padding:14px 30px;border-radius:999px;border:2.5px solid #fff;background:rgba(255,255,255,.12);color:#fff;font:600 22px 'Fredoka',sans-serif;cursor:pointer;transition:transform .12s,background .12s}
.ghost:hover{transform:translateY(-4px);background:rgba(255,255,255,.26)}
.days{display:flex;align-items:center;gap:10px;margin-top:10px;font-size:16px;font-weight:500}
.d{width:44px;height:44px;border-radius:50%;display:grid;place-items:center;background:#2a1f80;border:2px solid #7fe7ff;font-weight:700;animation:bob 3s ease-in-out infinite}
.d:nth-child(2){animation-delay:.3s}.d:nth-child(3){animation-delay:.6s}.d:nth-child(4){animation-delay:.9s}.d:nth-child(5){animation-delay:1.2s}
.moon{position:absolute;left:-12%;bottom:0;width:124%;height:var(--m);border-radius:50% 50% 0 0/70px 70px 0 0;background:linear-gradient(#dcd9ee,#8f8ab0 70%,#6f6a94);z-index:2;box-shadow:0 -10px 40px rgba(180,170,255,.35)}
.cr{position:absolute;border-radius:50%;background:rgba(80,70,120,.28);box-shadow:inset 5px 6px 0 rgba(60,50,100,.35)}
.base{position:absolute;right:10%;bottom:calc(var(--m) - 50px);width:clamp(170px,22vw,290px);z-index:2;overflow:visible}
.shield{animation:shd 12s infinite}
@keyframes shd{0%,44%{opacity:0}46%{opacity:1}50%{opacity:.25}54%{opacity:1}58%{opacity:.5}62%,70%{opacity:.95}74%,100%{opacity:0}}
.dish{transform-origin:130px 50px;animation:dsh 5s ease-in-out infinite}
@keyframes dsh{0%,100%{transform:rotate(-28deg)}50%{transform:rotate(28deg)}}
.pan{transform-origin:249px 90px;animation:pn 8s ease-in-out infinite}
@keyframes pn{0%,100%{transform:rotate(-18deg)}50%{transform:rotate(18deg)}}
.dot{animation:tw 1.6s ease-in-out infinite}
.itiri{position:absolute;left:clamp(8px,12%,220px);bottom:calc(var(--m) - 50px);width:clamp(86px,10vw,128px);padding:0;border:0;background:none;cursor:pointer;z-index:3;animation:hop 7s ease-in-out infinite}
.itiri svg{display:block;width:100%;height:auto;overflow:visible}
.itiri.go{animation:flip 1s ease-in-out}
.itiri:focus-visible{outline:3px solid #ffc93c;outline-offset:6px;border-radius:24px}
@keyframes hop{0%,30%,55%,85%,100%{transform:translateY(0)}15%{transform:translateY(-52px)}70%{transform:translateY(-70px)}}
.rover{position:absolute;bottom:calc(var(--m) * .28);left:-10%;width:clamp(56px,6vw,76px);z-index:3;animation:drive 32s linear infinite}
.rover svg{display:block;width:100%;height:auto}
.rb{animation:bmp .45s ease-in-out infinite}.tr{animation:trk .5s linear infinite}
@keyframes bmp{50%{transform:translateY(-1.5px)}}
@keyframes trk{to{stroke-dashoffset:-10}}
@keyframes drive{0%{left:-10%;transform:scaleX(1)}47%{left:100%;transform:scaleX(1)}50%{left:100%;transform:scaleX(-1)}97%{left:-10%;transform:scaleX(-1)}100%{left:-10%;transform:scaleX(1)}}
@keyframes fh{0%,43%{opacity:1}45%,95%{opacity:0}97%,100%{opacity:1}}
@keyframes fw{0%,44%{opacity:0}46%,71%{opacity:1}73%,100%{opacity:0}}
@keyframes fj{0%,73%{opacity:0}75%,93%{opacity:1}95%,100%{opacity:0}}
.fh{animation:fh 12s infinite}.fw{animation:fw 12s infinite}.fj{animation:fj 12s infinite}
@keyframes flip{0%{transform:translateY(0) rotate(0)}50%{transform:translateY(-90px) rotate(180deg)}100%{transform:translateY(0) rotate(360deg)}}
.wave{transform-origin:30px 92px;animation:wv 1s ease-in-out infinite}
@keyframes wv{50%{transform:rotate(-35deg)}}
.eye{transform-box:fill-box;transform-origin:center;animation:bl 4s infinite}
@keyframes bl{0%,92%,100%{transform:scaleY(1)}96%{transform:scaleY(.1)}}
.say{position:absolute;left:clamp(90px,17%,380px);bottom:calc(var(--m) + 88px);z-index:3;width:220px;height:72px;pointer-events:none}
.say span{position:absolute;inset:0;box-sizing:border-box;padding:10px 14px;background:#fff;color:#1b1340;border-radius:18px;font-size:16px;font-weight:600;line-height:1.2;opacity:0}
.say span.fh{opacity:1}

.fm{display:flex;flex-direction:column;align-items:center;gap:1.8vh;margin:0}
.fm .row,.fm .lv{margin-top:0}
.how{display:none;position:absolute;inset:0;z-index:10;background:rgba(10,6,48,.85);align-items:center;justify-content:center;padding:20px}
.tg:checked~.how{display:flex}
.hb{background:#2a1f80;border:2px solid #7fe7ff;border-radius:24px;padding:3vh 32px;max-width:560px;max-height:90%;overflow:auto;box-sizing:border-box}
.hb h2{margin:0 0 1vh;font-size:clamp(24px,4vh,34px)}
.hb ol{margin:0 0 2vh;padding-left:24px;font-size:clamp(15px,2.6vh,20px);line-height:1.4}
@media (prefers-reduced-motion:reduce){.lc *,.lc *:before,.lc *:after{animation:none!important}}
@media (max-width:640px){.say{display:none}.base{display:none}}
</style>
<div class="lc">
<input class="sr tg" type="checkbox" id="how" aria-label="Show how to play">
<div class="st s1"></div>
<div class="st s2"></div>
<div class="shoot"></div>
<div class="sun" aria-hidden="true"><i></i><i></i></div>
<div class="earth" aria-hidden="true">
<svg viewBox="0 0 200 100" preserveAspectRatio="none">
<g fill="#4cc36b"><path d="M20 25q10-12 25-6q10 8 4 20q-6 10-14 8q-12-4-15-22z"/><path d="M55 55q12-6 20 4q6 12-4 22q-12 6-18-6q-4-12 2-20z"/><path d="M72 20q12-4 18 6q2 10-8 12q-10 0-10-18z"/></g>
<g fill="#4cc36b" transform="translate(100 0)"><path d="M20 25q10-12 25-6q10 8 4 20q-6 10-14 8q-12-4-15-22z"/><path d="M55 55q12-6 20 4q6 12-4 22q-12 6-18-6q-4-12 2-20z"/><path d="M72 20q12-4 18 6q2 10-8 12q-10 0-10-18z"/></g>
</svg>
</div>
<div class="hero">
<div class="badge">Real NASA solar storm data inside</div>
<h1 class="logo">LUNA-CTRL</h1>
<p class="tag">You are the commander of a Moon base. Keep your crew alive for 5 days while the Sun throws a real storm at you!</p>
<form class="fm" onsubmit="return startGame(this)">
<div class="lv" role="radiogroup" aria-label="Choose your level">
<input class="sr" type="radio" name="level" value="junior" id="l1"><label class="chip" for="l1">Junior · ages 7–9</label>
<input class="sr" type="radio" name="level" value="commander" id="l2" checked><label class="chip" for="l2">Commander · ages 10–12</label>
<input class="sr" type="radio" name="level" value="expert" id="l3"><label class="chip" for="l3">Expert · family</label>
</div>
<div class="row">
<button class="play" type="submit">Start mission</button>
<button class="ghost" type="button" onclick="document.getElementById('how').checked=true">How to play</button>
</div>
</form>
<div class="days" aria-label="5 days to survive"><span>Survive</span><span class="d">1</span><span class="d">2</span><span class="d">3</span><span class="d">4</span><span class="d">5</span><span>days</span></div>
</div>
<div class="moon">
<div class="cr" style="left:30%;top:60px;width:90px;height:26px"></div>
<div class="cr" style="left:52%;top:110px;width:140px;height:34px"></div>
<div class="cr" style="left:74%;top:50px;width:60px;height:18px"></div>
<div class="cr" style="left:12%;top:130px;width:70px;height:20px"></div>
</div>
<svg class="base" viewBox="0 0 260 110" role="img" aria-label="Moon base made of a greenhouse, a command hub and living quarters, with a shield that switches on during storms">
<rect x="76" y="88" width="20" height="9" fill="#cfcbe6"/><rect x="164" y="88" width="18" height="9" fill="#cfcbe6"/>
<path d="M9 100a36 36 0 0 1 72 0z" fill="#bff3d0" stroke="#fff" stroke-width="2"/>
<g fill="#2fae5a"><circle cx="32" cy="92" r="6"/><circle cx="46" cy="90" r="7"/><circle cx="60" cy="93" r="5"/></g>
<path d="M174 100a32 32 0 0 1 64 0z" fill="#ffd9b8" stroke="#fff" stroke-width="2"/>
<circle class="dot" cx="196" cy="88" r="4" fill="#7fe7ff"/><circle class="dot" cx="216" cy="88" r="4" fill="#ffc93c"/>
<path d="M92 100a38 38 0 0 1 76 0z" fill="#f1efff" stroke="#fff" stroke-width="2"/>
<rect x="122" y="72" width="16" height="28" rx="8" fill="#1e2a78"/>
<path d="M130 62v-12" stroke="#fff" stroke-width="3"/>
<g class="dish"><ellipse cx="130" cy="47" rx="12" ry="4.5" fill="#fff"/><circle cx="130" cy="42" r="2.5" fill="#ffc93c"/></g>
<path d="M249 100v-10" stroke="#fff" stroke-width="3"/>
<rect class="pan" x="238" y="86" width="22" height="6" rx="1" fill="#2a7de1" stroke="#fff" stroke-width="1.5"/>
<path class="shield" d="M0 104A130 100 0 0 1 260 104" fill="rgba(127,231,255,.14)" stroke="#7fe7ff" stroke-width="3" stroke-dasharray="7 4"/>
</svg>
<div class="rover" aria-hidden="true"><svg viewBox="0 0 64 50"><rect x="26" y="8" width="12" height="8" fill="#9a95c0"/><circle cx="24" cy="6" r="6" fill="#fff"/><circle cx="40" cy="6" r="6" fill="#fff"/><circle cx="25" cy="6" r="2.6" fill="#1e2a78"/><circle cx="41" cy="6" r="2.6" fill="#1e2a78"/><g class="rb"><rect x="8" y="16" width="48" height="22" rx="6" fill="#ffc93c"/><rect x="14" y="22" width="14" height="8" rx="2" fill="#d9961b"/><circle cx="46" cy="27" r="4" fill="#ff8a3d"/></g><rect x="3" y="36" width="58" height="12" rx="6" fill="#4a4670"/><path class="tr" d="M10 42h44" stroke="#b9b5da" stroke-width="3" stroke-dasharray="5 5"/></svg></div>
<div class="say" aria-hidden="true"><span class="fh">Hi, Commander! I'm Itiri. Tap me!</span><span class="fw">Solar storm warning! Shield up!</span><span class="fj">Phew! The crew is safe!</span></div>
<button class="itiri" aria-label="Itiri the mascot. Tap to make Itiri flip." onclick="var b=this;b.classList.remove('go');void b.offsetWidth;b.classList.add('go');setTimeout(function(){b.classList.remove('go')},1000)">
<svg viewBox="0 0 120 150" aria-hidden="true">
<path d="M60 26v-12" stroke="#fff" stroke-width="3"/><circle class="dot" cx="60" cy="9" r="6" fill="#ffc93c"/>
<rect x="40" y="118" width="14" height="24" rx="7" fill="#fff"/><rect x="66" y="118" width="14" height="24" rx="7" fill="#fff"/>
<rect x="32" y="80" width="56" height="46" rx="22" fill="#ff8a3d"/>
<rect x="84" y="88" width="12" height="30" rx="6" fill="#fff"/>
<rect class="wave" x="24" y="88" width="12" height="30" rx="6" fill="#fff"/>
<circle cx="60" cy="102" r="7" fill="#ffc93c"/>
<circle cx="60" cy="52" r="38" fill="#fff"/>
<ellipse cx="60" cy="54" rx="29" ry="25" fill="#1e2a78"/>
<g class="fh"><ellipse class="eye" cx="50" cy="52" rx="5" ry="7" fill="#7fe7ff"/><ellipse class="eye" cx="70" cy="52" rx="5" ry="7" fill="#7fe7ff"/><path d="M52 64q8 7 16 0" stroke="#7fe7ff" stroke-width="3" fill="none" stroke-linecap="round"/></g>
<g class="fw"><circle cx="50" cy="52" r="6.5" fill="#ffb347"/><circle cx="70" cy="52" r="6.5" fill="#ffb347"/><circle cx="50" cy="53" r="2.4" fill="#1e2a78"/><circle cx="70" cy="53" r="2.4" fill="#1e2a78"/><path d="M52 67q4-4 8 0q4 4 8 0" stroke="#ffb347" stroke-width="3" fill="none" stroke-linecap="round"/><path d="M84 38q5 8 0 12q-5-4 0-12z" fill="#7fe7ff"/><g transform="translate(88 6)"><path d="M10 0l10 18H0z" fill="#ffc93c"/><rect x="9" y="6" width="2" height="6" fill="#1b1340"/><circle cx="10" cy="15" r="1.2" fill="#1b1340"/></g></g>
<g class="fj"><path d="M50 44l2.4 5.2 5.6.6-4.2 3.8 1.2 5.6-5-2.8-5 2.8 1.2-5.6-4.2-3.8 5.6-.6z" fill="#ffd966"/><path transform="translate(20 0)" d="M50 44l2.4 5.2 5.6.6-4.2 3.8 1.2 5.6-5-2.8-5 2.8 1.2-5.6-4.2-3.8 5.6-.6z" fill="#ffd966"/><path d="M49 62q11 13 22 0z" fill="#7fe7ff"/></g>
</svg>
</button>
<div class="how" role="dialog" aria-label="How to play"><div class="hb"><h2>How to play</h2><ol>
<li>See the real event the Sun made that day.</li>
<li>Handle each event. You get two choices, and neither is free.</li>
<li>Pick 2 actions to spend your power and air.</li>
<li>End the day and watch the storm hit.</li>
<li>Survive all 5 days. Don't let power or air hit zero!</li>
</ol><button class="play" type="button" onclick="document.getElementById('how').checked=false">Got it!</button></div></div>
</div>
<script>
function startGame(f){
  var lv = (new FormData(f)).get("level") || "commander";
  try {
    var b = window.parent.document.querySelector(".st-key-start_" + lv + " button");
    if (b) { b.click(); }
  } catch (e) {}
  return false;
}
</script>
"""