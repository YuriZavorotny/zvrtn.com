# -*- coding: utf-8 -*-
"""Сборка сайта: python3 build.py <out_dir> <home_href>
   home_href: "index.html" для локальной папки, "./" для опубликованной версии."""
import sys, json, html, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
out, HOME = sys.argv[1], sys.argv[2]
esc = html.escape

FONTS = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter+Tight:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">'''

# стрелка: тонкая, острый кончик, стоит после названия
ARROW = '<span class="ar" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="butt" stroke-linejoin="miter"><path d="M1 12H22"/><path d="M15 5l7 7-7 7"/></svg></span>'

CASES = [
 dict(slug="sweed", title="Sweed", role="Senior/Staff Product Designer", period="Dec 2023 – Jan 2026", years="2023–2026", video="v/sweed.mp4",
      link=("sweedpos.com", "https://sweedpos.com"),
      metric=["Orders placed 2.8x", "Open rate +19%", "CTR +12%", "Revenue per user +$27"]),
 dict(slug="juro", title="Juro", role="Lead Product Designer", period="Sep 2020 – Dec 2023", years="2020–2023", video="v/juro.mp4",
      link=("juro.com", "https://juro.com"),
      metric=["Document import +29.5%", "Key feature adoption +19%", "6,000+ customers"]),
 dict(slug="microsoft-azure", title="Microsoft Azure", role="UX Expert", period="Oct 2019 – Sep 2020", years="2019–2020", video="v/azure.mp4",
      link=("azure.microsoft.com", "https://azure.microsoft.com")),
 dict(slug="real-time-tech", title="Real Time Tech", role="Senior Product Designer", period="Oct 2017 – Oct 2019", years="2017–2019", video="v/webka.mp4",
      link=("webka.com", "https://webka.com")),
 dict(slug="it-test", title="IT Test", role="Lead UX/UI Designer", period="Dec 2015 – Oct 2017", years="2015–2017", video="v/freezio.mp4",
      tint=[.975, .985, 1]),
 dict(slug="inter-rao", title="Inter RAO", role="UX/UI Designer", period="Feb 2013 – Dec 2015", years="2013–2015", video="v/inter-rao.mp4",
      link=("interrao.lt", "https://interrao.lt")),
]
for c in CASES: c["href"] = "case-%s.html" % c["slug"]

# ------------------------------------------------------------------ CSS
CSS = r'''
:root{
  --bg:#fff; --ink:#000; --gray:#8f8f8f; --line:#e4e4e4;
  --serif:"Instrument Serif","Times New Roman",serif;                 /* антиква: только крупно */
  --grot:"Inter Tight","Helvetica Neue",Helvetica,Arial,sans-serif;   /* гротеск: акценты, имена, длинный текст */
  --mono:"IBM Plex Mono",ui-monospace,Menlo,monospace;                /* моно: служебное */
  --u:calc(min(100vw,1741px)/1024);
  --m:calc(40*var(--u));                 /* боковое поле */
  --lbl:max(12px,calc(11.5*var(--u)));   /* кегль моно */
  --ease:cubic-bezier(.65,0,.35,1);
}
*{box-sizing:border-box}
html{background:var(--bg)}
body{margin:0;background:transparent;color:var(--ink);font-family:var(--grot);-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
a{color:inherit;text-decoration:none}
p,h1,h2,h3,figure,ul{margin:0;padding:0}
ul{list-style:none}
button{font:inherit;color:inherit;background:none;border:0;padding:0;cursor:pointer}
img,video{display:block;max-width:100%}

/* моно: служебный текст */
.lbl,.top nav a,.top .ddb,.foot a,.foot span{font-family:var(--mono);font-weight:500;font-size:var(--lbl);line-height:1.5;text-transform:uppercase;letter-spacing:.04em}
.gray{color:var(--gray)}

#gl{position:fixed;inset:0;width:100%;height:100%;z-index:0;pointer-events:none;display:block}

/* ---------- шапка ---------- */
.top{position:fixed;z-index:20;top:0;left:0;right:0;display:flex;align-items:center;justify-content:space-between;
  height:max(44px,calc(34*var(--u)));padding:0 var(--m);
  background:rgba(255,255,255,.6);-webkit-backdrop-filter:blur(22px) contrast(.3) brightness(2.2);backdrop-filter:blur(22px) contrast(.3) brightness(2.2)}
.top .me{font-family:var(--grot);font-weight:700;font-size:max(14px,calc(13.5*var(--u)));letter-spacing:-.02em}
.top nav{display:flex;align-items:center;gap:calc(34*var(--u))}
.top nav a,.foot a,.top .ddb{position:relative;line-height:1.3}
.top nav>a::after,.foot a::after,.top .ddb .t::after{content:"";position:absolute;left:0;right:0;bottom:-2px;height:1px;background:currentColor;transform:scaleX(0);transform-origin:left;transition:transform .6s var(--ease)}
.top nav>a:hover::after,.foot a:hover::after,.top nav>a.on::after,.dd.open .ddb .t::after,.dd.on .ddb .t::after{transform:scaleX(1)}
/* выпадающий список кейсов */
.dd{position:relative;display:flex;align-items:center;height:max(44px,calc(34*var(--u)))}
.ddb{display:inline-flex;align-items:center;gap:.5em}
.ddb .t{position:relative}
.ddb .car{width:.5em;height:.5em;border-right:1.5px solid currentColor;border-bottom:1.5px solid currentColor;transform:translateY(-25%) rotate(45deg);transition:transform .4s var(--ease)}
.dd.open .ddb .car{transform:translateY(15%) rotate(225deg)}
.ddp{position:absolute;top:100%;right:calc(-1*var(--lbl));min-width:max(280px,calc(250*var(--u)));padding:8px var(--lbl) 12px;background:#fff;
  border-top:1px solid var(--ink);visibility:hidden;opacity:0;transform:translateY(-6px);transition:opacity .25s,transform .35s var(--ease),visibility 0s .35s}
.dd.open .ddp{visibility:visible;opacity:1;transform:none;transition:opacity .25s,transform .35s var(--ease)}
.ddp a{display:flex;justify-content:space-between;gap:2em;padding:.55em 0;border-bottom:1px solid var(--line);white-space:nowrap;transition:padding .4s var(--ease)}
.ddp a:last-child{border-bottom:0}
.ddp a i{font-style:normal;color:var(--gray)}
.ddp a:hover{padding-left:.6em}
.ddp a.on{color:var(--gray)}

/* ---------- общий каркас ---------- */
.stage,.page{position:relative;z-index:1;width:100%;max-width:1741px;margin:0 auto}
.page{padding-top:max(44px,calc(34*var(--u)))}
/* единый заголовок внутренних страниц: подпись, под ней линия */
.phead{display:flex;justify-content:space-between;align-items:baseline;gap:20px;margin:0 var(--m);padding:calc(96*var(--u)) 0 calc(14*var(--u));border-bottom:1px solid var(--ink)}
.sec{margin:0 var(--m);padding:calc(30*var(--u)) 0 calc(110*var(--u));border-top:1px solid var(--ink);display:grid;grid-template-columns:calc(236*var(--u)) 1fr;column-gap:calc(20*var(--u))}
.sec.first{border-top:0}
.sec.tight{padding-bottom:calc(64*var(--u))}
.sec.sub{border-top-color:var(--line)}

/* антиква: крупные высказывания */
.big{font-family:var(--serif);font-weight:400;font-size:max(30px,calc(56*var(--u)));line-height:.94;text-transform:uppercase;letter-spacing:-.01em}
.big b,.state b{font-family:var(--grot);font-weight:700;letter-spacing:-.04em}
.state{font-family:var(--serif);font-weight:400;font-size:max(24px,calc(31*var(--u)));line-height:1.06;letter-spacing:-.005em;max-width:22em}
/* гротеск: длинный текст */
.body{font-family:var(--grot);font-weight:400;font-size:max(16px,calc(12.6*var(--u)));line-height:1.5;letter-spacing:.004em;max-width:66ch}
.body p+p{margin-top:1em}
.body ul{margin:1em 0}
.body li{position:relative;padding-left:1.4em;margin-top:.45em}
.body li::before{content:"";position:absolute;left:0;top:.72em;width:.7em;height:1px;background:currentColor}
.body b,.body strong{font-weight:700}
.h3{font-family:var(--grot);font-weight:700;font-size:max(16px,calc(14.5*var(--u)));letter-spacing:-.02em;line-height:1.2;margin-bottom:.7em}

/* стрелка после названия: выезжает из-за края */
.ar{display:inline-block;position:relative;width:0;height:.62em;overflow:hidden;vertical-align:baseline;transition:width .6s var(--ease)}
.ar svg{position:absolute;right:0;top:0;width:.62em;height:.62em;transform:translateX(-110%);transition:transform .6s var(--ease)}
.hov .ar,a:hover>.g>.ar,a:hover>.ar{width:.84em}
.hov .ar svg,a:hover>.g>.ar svg,a:hover>.ar svg{transform:none}

/* ---------- главная ---------- */
.hero{padding:calc(132*var(--u)) var(--m) calc(64*var(--u))}
.hero .big{text-wrap:pretty}
.hero .w{display:inline-block;white-space:nowrap}
.hero .c{display:inline-block;will-change:transform;transform-origin:50% 60%}
.hint{display:flex;justify-content:space-between;align-items:center;margin:0 var(--m) calc(56*var(--u));padding-top:calc(14*var(--u));border-top:1px solid var(--ink)}
.hint .dn{display:inline-flex;align-items:center;gap:.7em}
.hint .dn svg{width:.9em;height:.9em;transform:rotate(90deg);animation:bob 1.8s var(--ease) infinite}
@keyframes bob{0%,100%{translate:0 -3px}50%{translate:0 3px}}

#list{position:relative;height:calc(2700*var(--u))}
.row{position:absolute;left:0;right:0;top:calc(var(--y)*var(--u));height:calc(280*var(--u));pointer-events:none}
.asset{position:absolute;top:0;width:calc(449*var(--u));height:calc(280*var(--u));pointer-events:auto;background:transparent;display:block}
.asset video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.row.r .asset{left:calc(525*var(--u))}
.row.l .asset{left:calc(50*var(--u))}
.txt{position:absolute;top:0;height:calc(280*var(--u));width:calc(320*var(--u));pointer-events:auto;display:flex;flex-direction:column;justify-content:space-between}
.row.r .txt{left:calc(100*var(--u))}
.row.l .txt{left:calc(624*var(--u))}
.ttl{font-family:var(--serif);font-weight:400;text-transform:uppercase;font-size:max(36px,calc(47*var(--u)));line-height:.9;letter-spacing:-.005em;margin-top:-.09em}
.meta{margin-bottom:-.3em}
.meta .mt{color:var(--gray)}
.meta .dt + .mt{margin-top:1em}
.item.gl-on .asset video{opacity:0}
.scr-pre{visibility:hidden}
.scr-w{white-space:nowrap}
.scr-c{display:inline-block;text-align:left;white-space:pre}

.recs{margin:calc(40*var(--u)) var(--m) 0;padding:calc(110*var(--u)) calc(60*var(--u)) 0;border-top:1px solid var(--ink)}
.recs .grid{display:grid;grid-template-columns:1fr 1fr;column-gap:calc(90*var(--u));row-gap:calc(84*var(--u))}
.recs q{display:block;quotes:none;font-family:var(--serif);font-weight:400;font-size:max(22px,calc(24*var(--u)));line-height:1.12;letter-spacing:-.005em}
.recs figcaption{margin-top:calc(20*var(--u))}
.nm2{font-family:var(--grot);font-weight:700;font-size:max(14px,calc(13.5*var(--u)));letter-spacing:-.02em}

.foot{display:flex;justify-content:space-between;align-items:baseline;padding:calc(170*var(--u)) var(--m) calc(30*var(--u))}
.foot nav{display:flex;gap:calc(34*var(--u))}

/* ---------- гигантские строки-ссылки ---------- */
.rows{margin:0 var(--m)}
.gl{display:flex;align-items:baseline;justify-content:space-between;gap:calc(30*var(--u));padding:calc(18*var(--u)) 0 calc(8*var(--u));border-bottom:1px solid var(--ink);transition:color .5s var(--ease)}
.gl .g{font-family:var(--serif);font-weight:400;text-transform:uppercase;font-size:max(40px,calc(74*var(--u)));line-height:.92;letter-spacing:-.01em}
.gl .side{text-align:right;flex:none;padding-bottom:calc(8*var(--u))}
.rows:hover .gl{color:var(--gray)}
.rows:hover .gl:hover{color:var(--ink)}
.copy{margin:calc(18*var(--u)) var(--m) 0;display:flex;justify-content:space-between;align-items:baseline;gap:20px}
.copy button{position:relative}
.copy button::after{content:"";position:absolute;left:0;right:0;bottom:-2px;height:1px;background:currentColor}

/* ---------- about ---------- */
.abt{display:grid;grid-template-columns:calc(330*var(--u)) 1fr;column-gap:calc(62*var(--u));align-items:start}
.ph .fr{position:relative;overflow:hidden;aspect-ratio:1013/1554;background:#efefef;clip-path:inset(0 0 100% 0);transition:clip-path 1.4s var(--ease)}
.ph.in .fr{clip-path:inset(0 0 0 0)}
.ph img{position:absolute;left:0;top:-6%;width:100%;height:112%;object-fit:cover;transform:scale(1.12);transition:transform 1.8s var(--ease);will-change:transform}
.ph.in img{transform:scale(1) translateY(var(--py,0px))}
.ph figcaption{display:flex;justify-content:space-between;gap:12px;margin-top:calc(12*var(--u))}
.abt .state{margin-bottom:calc(28*var(--u))}
.nums{display:grid;grid-template-columns:1fr 1fr;column-gap:calc(40*var(--u));row-gap:calc(56*var(--u))}
.nums.four{grid-template-columns:repeat(4,1fr)}
.nums b{display:block;font-family:var(--serif);font-weight:400;font-size:max(44px,calc(72*var(--u)));line-height:.86;letter-spacing:-.02em;margin-bottom:calc(14*var(--u))}
.xp li{border-bottom:1px solid var(--line)}
.xp li:first-child .xr{padding-top:0}
.xr{display:grid;grid-template-columns:1.1fr 1.3fr .9fr;align-items:baseline;padding:calc(12*var(--u)) 0}
.xp .co{font-family:var(--grot);font-weight:700;font-size:max(19px,calc(22*var(--u)));letter-spacing:-.035em;line-height:1.05}
.xp .yr{text-align:right}
.xp a.xr .co{transition:transform .5s var(--ease)}
.xp a.xr:hover .co{transform:translateX(.35em)}
.edu{display:grid;grid-template-columns:1fr 1fr;column-gap:calc(40*var(--u))}
.edu p{margin-top:.2em}

/* ---------- страница кейса ---------- */
.ctitle{margin:0 var(--m);padding:calc(26*var(--u)) 0 calc(30*var(--u))}
.ctitle h1{font-family:var(--serif);font-weight:400;text-transform:uppercase;font-size:max(48px,calc(96*var(--u)));line-height:.88;letter-spacing:-.012em;margin-left:-.03em}
.ctitle .cm{display:flex;flex-wrap:wrap;gap:.2em 2.4em;margin-top:calc(18*var(--u))}
.cvid{margin:0 var(--m) calc(64*var(--u));aspect-ratio:1152/720;background:#f3f3f3;overflow:hidden}
.cvid video{width:100%;height:100%;object-fit:cover}
.shots{display:grid;grid-template-columns:repeat(2,1fr);gap:calc(14*var(--u));margin-top:calc(34*var(--u))}
.shots.c3{grid-template-columns:repeat(3,1fr)}
.shots.c5{grid-template-columns:repeat(5,1fr)}
.shots.wide{grid-template-columns:1fr}
.shots img{width:100%;height:auto;border:1px solid var(--line)}
.shots figcaption{margin-top:.7em}
.cap{margin-top:calc(12*var(--u))}
.qs{display:grid;grid-template-columns:repeat(3,1fr);gap:calc(26*var(--u)) calc(30*var(--u));margin:calc(18*var(--u)) 0 calc(44*var(--u))}
.qs blockquote{margin:0;font-size:max(15px,calc(11.6*var(--u)));line-height:1.45}
.qs cite{display:block;font-style:normal;margin-top:.8em}
.jobs{display:grid;grid-template-columns:1fr 1fr;gap:calc(22*var(--u)) calc(40*var(--u));margin:calc(16*var(--u)) 0 calc(44*var(--u))}
.jobs p{font-size:max(15px,calc(11.6*var(--u)));line-height:1.45}
.body .h3{margin-top:2em}
.body .h3:first-child{margin-top:0}
.nextc{margin-top:calc(20*var(--u))}

@media (max-width:700px){
  :root{--m:20px}
  .top nav{gap:18px}
  .ddp{position:fixed;top:44px;left:0;right:0;min-width:0;padding:6px 20px 14px}
  .ddp a{padding:.8em 0}
  .phead{padding:64px 0 12px}
  .sec{grid-template-columns:1fr;row-gap:22px;padding:18px 0 72px}
  .sec.tight{padding-bottom:48px}
  .hero{padding:104px 20px 44px}
  .big{font-size:32px}
  .hint{margin-bottom:28px}
  #list{height:auto;padding:0}
  .row{position:static;height:auto;margin-bottom:120px}
  .asset{position:relative;left:0!important;width:100%;height:auto;aspect-ratio:449/280}
  .txt{position:static;width:auto;height:auto;margin-top:20px;padding:0 20px;gap:18px}
  .ttl{font-size:40px}
  .recs{padding:56px 0 0;margin-top:0}.recs .grid{grid-template-columns:1fr;row-gap:48px}
  .foot{padding:72px 20px 28px;flex-wrap:wrap;gap:12px}.foot nav{gap:16px}
  .gl{flex-direction:column;align-items:flex-start;gap:6px;padding:18px 0 14px}
  .gl .g{font-size:11.5vw}.gl .side{text-align:left;padding:0}
  .abt{grid-template-columns:1fr;row-gap:32px}
  .ph{max-width:78%}
  .nums,.nums.four{grid-template-columns:1fr 1fr;row-gap:40px;column-gap:20px}.nums b{font-size:46px}
  .xr{grid-template-columns:1fr;row-gap:2px;padding:14px 0}.xp .yr{text-align:left}
  .edu{grid-template-columns:1fr;row-gap:28px}
  .ctitle{padding:18px 0 22px}.ctitle h1{font-size:14vw}
  .cvid{margin:0 0 44px}
  .shots,.shots.c3{grid-template-columns:1fr;gap:12px}.shots.c5{grid-template-columns:1fr 1fr}
  .qs,.jobs{grid-template-columns:1fr}
}
'''

# ------------------------------------------------------------------ JS
SCRAMBLE = open(os.path.join(HERE, "scramble.src.js"), encoding="utf-8").read()
# набор букв только на моноширинном тексте
SCRAMBLE = SCRAMBLE.replace('".top nav a, .foot span, .foot a, .meta .mt, .recs .rl, [data-scr]"', '".top nav > a, .top .ddb .t, .foot span, .foot a, .meta .mt, .recs .rl, [data-scr]"')
SCRAMBLE = SCRAMBLE.replace('document.querySelectorAll(".top a, .foot a")', 'document.querySelectorAll(".top nav > a, .top .ddb .t, .foot a")')
assert '.top .ddb .t, .foot a")' in SCRAMBLE and '[data-scr]"' in SCRAMBLE

COMMON_JS = r'''
/* меню Works: открывается по наведению и по клику */
(function(){
var dd=document.querySelector(".dd"); if(!dd) return;
var b=dd.querySelector(".ddb"),t=null,fine=matchMedia("(hover: hover) and (pointer: fine)").matches;
function set(o){dd.classList.toggle("open",o);b.setAttribute("aria-expanded",o?"true":"false")}
b.addEventListener("click",function(e){e.stopPropagation();set(!dd.classList.contains("open"))});
if(fine){dd.addEventListener("pointerenter",function(){clearTimeout(t);set(true)});dd.addEventListener("pointerleave",function(){t=setTimeout(function(){set(false)},180)})}
document.addEventListener("click",function(e){if(!dd.contains(e.target))set(false)});
document.addEventListener("keydown",function(e){if(e.key==="Escape")set(false)});
})();
/* телефон: ховера нет, стрелка появляется, когда строка проходит середину экрана */
(function(){
if(!matchMedia("(hover: none)").matches||!("IntersectionObserver" in window)) return;
var io=new IntersectionObserver(function(es){es.forEach(function(e){e.target.classList.toggle("hov",e.isIntersecting)})},{rootMargin:"-38% 0px -38% 0px"});
[].forEach.call(document.querySelectorAll(".row, .gl"),function(r){io.observe(r)});
})();
'''

WARP_JS = r'''
/* первый экран: буквы слегка тянутся и деформируются под курсором (только мышь) */
(function(){
if(!matchMedia("(hover: hover) and (pointer: fine)").matches||matchMedia("(prefers-reduced-motion: reduce)").matches) return;
var h=document.querySelector(".hero .big"); if(!h) return;
var chars=[],raf=0,mx=-9999,my=-9999,vx=0,vy=0,lx=0,ly=0,inside=false;
function build(){
  /* 1) слова в span, 2) меряем естественные (с кернингом) ширины букв, 3) режем на буквы с этими ширинами */
  var words=[];
  (function walk(n){[].slice.call(n.childNodes).forEach(function(c){
    if(c.nodeType===3){var f=document.createDocumentFragment();
      c.textContent.split(/([ \t\r\n]+)/).forEach(function(t){if(!t)return;if(/^[ \t\r\n]+$/.test(t)){f.appendChild(document.createTextNode(" "));return}
        var w=document.createElement("span");w.className="w";w.textContent=t;f.appendChild(w);words.push(w)});
      n.replaceChild(f,c)}
    else if(c.nodeType===1) walk(c)})})(h);
  var plan=words.map(function(w){var tn=w.firstChild,t=tn.textContent,r=document.createRange(),ws=[];
    for(var i=0;i<t.length;i++){r.setStart(tn,i);r.setEnd(tn,i+1);ws.push(r.getBoundingClientRect().width)} return {w:w,t:t,ws:ws}});
  plan.forEach(function(p){p.w.textContent="";p.t.split("").forEach(function(ch,i){
    var s=document.createElement("span");s.className="c";s.textContent=ch;s.style.width=p.ws[i].toFixed(2)+"px";p.w.appendChild(s);
    chars.push({el:s,x:0,y:0,tx:0,ty:0,sx:1,sy:1,sk:0,cx:0,cy:0})})});
  h.setAttribute("aria-label",h.textContent);
  measure();
}
function measure(){var sy=scrollY;chars.forEach(function(c){c.el.style.transform="";var r=c.el.getBoundingClientRect();c.cx=r.left+r.width/2;c.cy=r.top+sy+r.height/2})}
function rebuild(){ /* при смене ширины окна ширины букв пересчитываются с нуля */
  chars.forEach(function(c){c.el.style.width=""});
  var ws=chars.map(function(c){return c.el.getBoundingClientRect().width});
  chars.forEach(function(c,i){c.el.style.width=ws[i].toFixed(2)+"px"}); measure();
}
function loop(){
  var R=Math.max(120,innerWidth*.095),py=my+scrollY,busy=false;
  vx*=.86;vy*=.86;
  for(var i=0;i<chars.length;i++){var c=chars[i],dx=c.cx-mx,dy=c.cy-py,d=Math.sqrt(dx*dx+dy*dy),f=inside?Math.max(0,1-d/R):0;
    f=f*f*(3-2*f);
    var tx=0,ty=0,sx=1,sy=1,sk=0;
    if(f>0){var n=d||1;tx=dx/n*f*7+vx*f*.35;ty=dy/n*f*9+vy*f*.25;sy=1+f*.2;sx=1-f*.06;sk=Math.max(-7,Math.min(7,-vx*.35))*f}
    c.x+=(tx-c.x)*.14;c.y+=(ty-c.y)*.14;c.sx+=(sx-c.sx)*.14;c.sy+=(sy-c.sy)*.14;c.sk+=(sk-c.sk)*.14;
    if(Math.abs(c.x)+Math.abs(c.y)+Math.abs(c.sy-1)+Math.abs(c.sk)>.02){busy=true;
      c.el.style.transform="translate("+c.x.toFixed(2)+"px,"+c.y.toFixed(2)+"px) skewX("+c.sk.toFixed(2)+"deg) scale("+c.sx.toFixed(3)+","+c.sy.toFixed(3)+")"}
    else if(c.el.style.transform) c.el.style.transform="";
  }
  raf=(busy||inside)?requestAnimationFrame(loop):0;
}
function start(){ if(!raf) raf=requestAnimationFrame(loop) }
function init(){
  build();
  addEventListener("pointermove",function(e){
    var r=h.getBoundingClientRect();inside=e.clientY>r.top-120&&e.clientY<r.bottom+120;
    vx+=(e.clientX-lx)*.6;vy+=(e.clientY-ly)*.6;lx=e.clientX;ly=e.clientY;mx=e.clientX;my=e.clientY;start()},{passive:true});
  document.addEventListener("pointerleave",function(){inside=false;start()});
  var rt;addEventListener("resize",function(){clearTimeout(rt);rt=setTimeout(rebuild,150)});
}
(document.fonts&&document.fonts.ready?document.fonts.ready:Promise.resolve()).then(function(){requestAnimationFrame(init)});
})();
'''

def home_gl():
    s = open(os.path.join(HERE, "home_gl.src.js"), encoding="utf-8").read()
    a = s.index("var ARROW="); b = s.index('}).join("");', a) + len('}).join("");')
    new = r'''var ARROW=%s;
document.getElementById("list").innerHTML=PROJECTS.map(function(p,i){
  return '<article class="row item '+(i%%2?'l':'r')+'" style="--y:'+(470*i)+'"'+(p.tint?' data-tint="'+p.tint.join(",")+'"':'')+'>'+
    '<a class="asset" href="'+esc(p.href)+'" aria-label="'+esc(p.title)+'"><video src="'+esc(p.video)+'" muted loop playsinline preload="auto" autoplay></video></a>'+
    '<a class="txt" href="'+esc(p.href)+'">'+
      '<h3 class="ttl">'+esc(p.title)+ARROW+'</h3>'+
      '<div class="meta"><p class="lbl role">'+esc(p.role)+'</p><p class="lbl dt">'+esc(p.period)+'</p>'+(p.metric||[]).map(function(m){return '<p class="lbl mt">'+esc(m)+'</p>'}).join('')+'</div>'+
    '</a>'+
  '</article>';
}).join("");''' % json.dumps(ARROW)
    s = s[:a] + new + s[b:]
    def rep(x, y):
        nonlocal s
        assert x in s, x[:60]
        s = s.replace(x, y, 1)
    rep("var haveFluid=!!extCBF;", "var haveFluid=false;   // свечение под курсором убрано")
    # десктоп: искажение при прокрутке заметно слабее, на телефоне как было
    rep("gl.uniform1f(U.uFisheye,CFG.FISHEYE*3);gl.uniform1f(U.uVelocity,sv);", "gl.uniform1f(U.uFisheye,CFG.FISHEYE*(touch?3:1));gl.uniform1f(U.uVelocity,touch?sv:sv*.4);")
    # десктоп: у краёв экрана видео искажается заметно слабее и в более узкой полосе
    rep("/* телефон: canvas лежит в документе", "if(!touch){CFG.EDGE_ZONE=.14;CFG.LENS_STRENGTH=.05;CFG.CA_STRENGTH=.007;CFG.SMEAR_STRENGTH=.05;CFG.LIQUID_STRENGTH=.02}\n/* телефон: canvas лежит в документе")
    return s

# ------------------------------------------------------------------ каркас
def nav(cur):
    def a(h, t, k): return '<a href="%s"%s>%s</a>' % (h, ' class="on"' if k == cur else '', t)
    dd = "".join('<a href="%s"%s><span>%s</span><i>%s</i></a>' % (c["href"], ' class="on"' if cur == c["slug"] else '', esc(c["title"]), c["years"]) for c in CASES)
    on = " on" if cur in [c["slug"] for c in CASES] else ""
    return ('<div class="dd%s"><button class="ddb" type="button" aria-expanded="false" aria-haspopup="true"><span class="t">Works</span><span class="car" aria-hidden="true"></span></button>'
            '<div class="ddp lbl">%s</div></div>%s%s') % (on, dd, a("about.html", "About", "about"), a("contact.html", "Contact", "contact"))

FOOT = '''  <footer class="foot">
    <span>© 2026</span>
    <nav>
      <a href="https://www.linkedin.com/in/zvrtn" target="_blank" rel="noopener">LinkedIn</a>
      <a href="https://t.me/zavorotny_yuri" target="_blank" rel="noopener">Telegram</a>
      <a href="mailto:zavorotny.yuri@gmail.com">Email</a>
    </nav>
  </footer>'''

def shell(cur, title, main, scripts="", pre="", main_cls="page"):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
{FONTS}
<style>{CSS}</style>
</head>
<body>
{pre}<header class="top">
  <a class="me" href="{HOME}">Yuri Zavorotny</a>
  <nav>{nav(cur)}</nav>
</header>
<main class="{main_cls}">
{main}
{FOOT}
</main>
{scripts}<script>{SCRAMBLE}</script>
<script>{COMMON_JS}</script>
</body>
</html>
'''

def phead(left, right=""):
    return '  <div class="phead"><p class="lbl" data-scr>%s</p>%s</div>\n' % (left, ('<p class="lbl gray">%s</p>' % right) if right else "")

def nums(items, cls=""):
    return '<div class="nums %s">%s</div>' % (cls, "".join('<div><b>%s</b><p class="lbl">%s</p>%s</div>' % (n, esc(a), ('<p class="lbl gray">%s</p>' % esc(c)) if c else "") for n, a, c in items))

def sec(label, inner, cls=""):
    return '  <section class="sec %s">\n    <p class="lbl" data-scr>%s</p>\n    <div>%s</div>\n  </section>\n' % (cls, label, inner)

def ps(*paras): return "".join("<p>%s</p>" % esc(p) for p in paras)
def shots(slug, idx, cls="", cap=None):
    f = "".join('<img src="img/%s-%02d.jpg" alt="" loading="lazy">' % (slug, i) for i in idx)
    return '<div class="shots %s">%s</div>%s' % (cls, f, ('<p class="lbl gray cap">%s</p>' % esc(cap)) if cap else "")

# ------------------------------------------------------------------ главная
RECS = [("Richard Mabey", "CEO at Juro, Oct 2023", "Yuri was instrumental in building our design function at Juro from the earliest days. What the world saw was clean UI that just worked."),
        ("Anton Solovev", "Senior Product Manager, Oct 2025", "Yuri has a real talent for turning messy, high-friction flows into smooth, intuitive experiences that users actually trust."),
        ("Max Nealon", "Product, Nov 2023", "Yuri is everything you need in a product designer and a whole lot more. He is highly iterative, he seeks out feedback and actually listens and considers."),
        ("Alex Fenin", "UX Researcher, Oct 2023", "His exceptional work of building the Editor experience in Juro doesn't simply meet expectations, it consistently overachieves them."),
        ("Howard Davies", "Staff Product Designer, Oct 2023", "He is a thoughtful and conscientious designer with a genuine, deep knowledge of best practises."),
        ("Viktor Avdeev", "Software Engineer, Nov 2023", "His approach to design is both innovative and user-centric, ensuring that every solution is not only aesthetically pleasing but also highly functional.")]

def home():
    recs = "".join('<figure><q>%s</q><figcaption><p class="nm2">%s</p><p class="lbl gray rl">%s</p></figcaption></figure>\n      ' % (esc(q), n, r) for n, r, q in RECS)
    main = f'''  <section class="hero">
    <h1 class="big"><b>Product designer</b> with 12 years in B2B &amp; SaaS products. <b>AI features</b> that ship, prototype in code and measure what works</h1>
  </section>
  <a class="hint" href="#list"><span class="lbl" data-scr>Selected work, 2013 – 2026</span><span class="lbl dn"><span data-scr>Scroll</span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M1 12H22"/><path d="M15 5l7 7-7 7"/></svg></span></a>
  <div id="list"></div>
  <section class="recs" id="recs">
    <div class="grid">
      {recs}</div>
  </section>'''
    pj = [dict(title=c["title"], role=c["role"], period=c["period"], video=c["video"], href=c["href"], metric=c.get("metric"), tint=c.get("tint")) for c in CASES]
    scripts = "<script>var PROJECTS=%s;</script>\n<script>%s</script>\n<script>%s</script>\n" % (json.dumps(pj, ensure_ascii=False), home_gl(), WARP_JS)
    return shell("home", "Yuri Zavorotny · Product Designer", main, scripts, pre='<canvas id="gl" aria-hidden="true"></canvas>\n', main_cls="stage")

# ------------------------------------------------------------------ about
def about():
    by = {c["title"]: c["href"] for c in CASES}
    xp = [("Profi", "Senior Product Designer", "Mar 2026 – now")] + [(c["title"], c["role"], c["period"]) for c in CASES]
    def xrow(c, r, y):
        inner = '<span class="co">%s</span><span class="lbl">%s</span><span class="lbl gray yr">%s</span>' % (c, r, y)
        return '<li>%s</li>' % (('<a class="xr" href="%s">%s</a>' % (by[c], inner)) if c in by else '<div class="xr">%s</div>' % inner)
    main = phead("About") + f'''  <section class="sec first">
    <p class="lbl gray"></p>
    <div class="abt">
      <figure class="ph" id="ph"><div class="fr"><img src="img/yuri.jpg" alt="Portrait of Yuri Zavorotny" onerror="this.closest('figure').remove()"></div><figcaption class="lbl"><span>Yuri Zavorotny</span><span class="gray">Product designer</span></figcaption></figure>
      <div>
        <p class="state">Designing digital products with a focus on structure, clarity, and predictable UX</p>
        <div class="body"><p>I’ve led design teams, mentored designers, and collaborated closely with product and engineering to turn ambitious ideas into reliable, user-centered solutions. Looking for a team that values clarity, craft, and shared responsibility, a place where designers and engineers build together, not in silos. I’m driven by thoughtful, data-informed design that creates real user impact.</p></div>
      </div>
    </div>
  </section>
''' + sec("In numbers", nums([("+21%", "Client-to-contact conversion", "Profi, top-3 recommendations, A/B test"), ("2.8x", "Order-placed rate", "Sweed, A/B testing inside Workflows"),
                              ("+29.5%", "Document import into the editor", "Juro, editor redesign"), ("6,000+", "Customers on the platform", "Juro")], "four")) \
      + sec("Experience", '<ul class="xp">%s</ul>' % "".join(xrow(*x) for x in xp)) \
      + sec("Education", '''<div class="edu">
      <div><p class="h3">Saint Petersburg State University</p><p class="body">Master's degree in Art History</p><p class="lbl gray">2014 – 2016</p></div>
      <div><p class="h3">Emperor Alexander I St. Petersburg State Transport University</p><p class="body">Economics</p><p class="lbl gray">2007 – 2012</p></div>
    </div>''', "tight")
    js = '''<script>
(function(){var f=document.getElementById("ph");if(!f)return;
if(!("IntersectionObserver" in window)){f.classList.add("in");return}
var io=new IntersectionObserver(function(es){if(es[0].isIntersecting){f.classList.add("in");io.disconnect()}},{threshold:.1});io.observe(f);
/* лёгкий параллакс портрета при прокрутке */
if(matchMedia("(prefers-reduced-motion: reduce)").matches) return;
var img=f.querySelector("img"),tick=false;
addEventListener("scroll",function(){if(tick)return;tick=true;requestAnimationFrame(function(){tick=false;var r=f.getBoundingClientRect();
  var p=(r.top+r.height/2-innerHeight/2)/innerHeight;img.style.setProperty("--py",(-p*r.height*.05).toFixed(1)+"px")})},{passive:true});
})();
</script>
'''
    return shell("about", "About · Yuri Zavorotny", main, js)

# ------------------------------------------------------------------ contact
def contact():
    rows = [("Email", "mailto:zavorotny.yuri@gmail.com", "zavorotny.yuri@gmail.com", ""),
            ("LinkedIn", "https://www.linkedin.com/in/zvrtn", "linkedin.com/in/zvrtn", ' target="_blank" rel="noopener"'),
            ("Telegram", "https://t.me/zavorotny_yuri", "@zavorotny_yuri", ' target="_blank" rel="noopener"')]
    main = phead("Contact") + '  <div class="rows">\n' + "".join(
        '    <a class="gl" href="%s"%s><span class="g">%s%s</span><span class="side lbl">%s</span></a>\n' % (h, t, n, ARROW, v) for n, h, v, t in rows) + '''  </div>
  <div class="copy"><p class="lbl gray">Let's keep in touch</p><button class="lbl" type="button" id="cp" data-v="zavorotny.yuri@gmail.com">Copy email</button></div>
'''
    js = '''<script>
(function(){var b=document.getElementById("cp");if(!b)return;var t;
b.addEventListener("click",function(){var v=b.dataset.v;
  function ok(){b.textContent="Copied";clearTimeout(t);t=setTimeout(function(){b.textContent="Copy email"},1600)}
  function old(){var i=document.createElement("textarea");i.value=v;i.style.position="fixed";i.style.opacity="0";document.body.appendChild(i);i.select();try{document.execCommand("copy");ok()}catch(e){}i.remove()}
  if(navigator.clipboard&&navigator.clipboard.writeText) navigator.clipboard.writeText(v).then(ok,old); else old()});
})();
</script>
'''
    return shell("contact", "Contact · Yuri Zavorotny", main, js)

# ------------------------------------------------------------------ кейсы
def qgroup(title, qs):
    return '<p class="h3">%s</p><div class="qs">%s</div>' % (esc(title), "".join('<blockquote>%s<cite class="lbl gray">%s</cite></blockquote>' % (esc(q), esc(w)) for q, w in qs))
def jobs(name, stories):
    return '<p class="h3">%s</p><div class="jobs">%s</div>' % (esc(name), "".join("<p>%s</p>" % esc(s) for s in stories))
def body(*parts): return '<div class="body">%s</div>' % "".join(parts)
def ul(*items): return "<ul>%s</ul>" % "".join("<li>%s</li>" % esc(i) for i in items)
def h3(t): return '<p class="h3">%s</p>' % esc(t)

def content(slug):
    if slug == "juro":
        return (
          sec("Company", body(ps("Juro is a London-based AI-powered contract management platform that accelerates contract creation. With over 6,000 global clients, it was established in 2016 by legal and tech experts to streamline the contract creation process. Main competitors: PandaDoc, DocuSign, Ironclad."))) +
          sec("Role", body(ps("At Juro, I grew from Product Designer to Senior and later Lead Product Designer, taking ownership of high-impact initiatives. I led the redesign of Juro’s core text editor for a SaaS platform with 6,000+ customers, resulting in a 29.5% increase in document imports, 19% higher adoption of key features, and a 2.5% reduction in Word/PDF exports.",
                               "As a team lead, I contributed to strategic planning, optimized design workflows, mentored designers, and temporarily stepped in for the Design Director. Working closely with product and engineering, I drove user-centered, data-informed decisions that improved collaboration flows and daily efficiency for legal and sales teams."))) +
          sec("Results", nums([("+29.5%", "Document imports", ""), ("+19%", "Adoption of key features", ""), ("−2.5%", "Word/PDF exports", ""), ("6,000+", "Customers on the platform", "")], "four")) +
          sec("Case study", '<p class="state">Evolution of the Text Editor: Improving Workflow for Efficient Contract Management</p>' +
              body(ps("Welcome to my case study on upgrading the text editor in Juro. In this study, I will share my process of addressing challenges and finding ways to improve functionality, making contract management more intuitive and user-friendly. This case study covers the following stages:"),
                   ul("Problem statement", "Feedback and insights", "Personas and JTBD", "Qualitative and quantitative metrics", "Design solution", "Checking")) +
              shots("juro", [13, 14], cap="New and old versions of the editor")) +
          sec("I. Problem statement", body(ps("The problem statement is like the compass that points us in the right direction by highlighting what users struggle with and where the product needs to do better.",
              "The old text editor in Juro was limited in functionality compared to popular platforms like Microsoft Word and Google Docs, forcing users to seek additional tools for certain contract-related tasks. The limitations of this editor prevented a seamless and efficient workflow for working with contracts, from creation to signing, without the need for external platforms.")), "sub") +
          sec("II. Feedback and insights", body(ps("By organizing user feedback into distinct categories, we gained insights that guided our next steps.")) +
              '<div style="margin-top:2em">' +
              qgroup("1. Unfamiliar design patterns", [("I wish the text editor in Juro could allow for more advanced formatting options like Word. It would make the editing process much smoother and familiar.", "John Ramirez, Legal Counsel at Foody Corporation"),
                  ("Having the ability to easily create tables and insert images within the text editor would be incredibly beneficial for creating comprehensive contracts.", "Samantha Smith, Contracts Manager at Regain"),
                  ("The current text editor lacks the intuitive features that I'm used to in Word. A more similar interface would significantly improve my workflow.", "David Johnson, Compliance Officer at LMN Inc.")]) +
              qgroup("2. Visibility and accessibility of additional features", [("It would be great if I didn't have to search through multiple menus to find the option to add comments or signatures. Having these functions readily visible would save me a lot of time.", "Emily Williams, Sales Coordinator at Loop"),
                  ("I often struggle to locate the attachment option in the current text editor. It would be helpful if it was more prominently displayed on the main screen.", "Michael Brown, Legal Consultant at DEF Industries"),
                  ("The current text editor has some hidden features that I only discovered after exploring the menu extensively. Having these features more accessible would streamline my document management process.", "Olivia Davis, Sales Director at Oregano Ltd.")]) +
              qgroup("3. More compact header for improved viewing", [("The header in the text editor takes up too much space, making it difficult to focus on the main text. A more compact design would greatly improve the overall viewing experience.", "Daniel Wilson, Legal Coordinator at OPQ"),
                  ("I find the current header to be distracting and unnecessary. A sleeker design that doesn't interfere with the document's content would be much appreciated.", "Sophia Lee, Legal Consultant at RapidX"),
                  ("When reviewing lengthy contracts, the bulky header often gets in the way of my reading. A more streamlined header would make the document more readable and user-friendly.", "Andrew Miller, Sales Specialist at GHI Incorporated")]) +
              qgroup("4. Easy access to key contract functions", [("I frequently need to export contracts for further processing, but finding the export option in the current editor is cumbersome. A more accessible export feature would save me valuable time.", "Emma Thompson, Sales Analyst at Virago"),
                  ("The current process for managing versions of a contract is convoluted. Having a one-click version control option would significantly simplify my workflow.", "William Garcia, Contracts Administrator at Fortitude"),
                  ("I often struggle to find the option to lock a contract for editing. A more prominent and easily accessible locking function would prevent accidental modifications and ensure data integrity.", "Isabella Martinez, Sales Manager at STU Inc.")]) +
              qgroup("5. Instant visibility of essential contract data", [("It would be incredibly helpful to immediately see the status of a contract as soon as I open the editor. This would allow me to prioritize my tasks more efficiently.", "Alexander Harris, Legal Officer at VWX Corporation"),
                  ("I often have to navigate through multiple screens to find information about the participants involved in a contract. Having this data readily visible would streamline my understanding of the document's context.", "Sophie Johnson, Sales Specialist at Rebel"),
                  ("Knowing the status of a contract without having to go through several menus would improve my decision-making process. Instant visibility of this information is crucial for managing multiple contracts simultaneously.", "Ethan White, Sales Advisor at BCD Ltd.")]) + '</div>', "sub") +
          sec("III. JTBD", body(ps("The Jobs-to-be-Done framework emphasizes understanding the job a customer is trying to accomplish, rather than just focusing on their demographics or preferences. Job stories humanize the needs and motivations of users and keep the design process user-centric and outcome-driven.")) +
              '<div style="margin-top:2em">' +
              jobs("Alex Green, Head Counsel, Alpha Inc. Legal", ["When I'm reviewing a lengthy contract with multiple stakeholders' input, I want the text editor to track changes and versions efficiently, so that I can ensure the accuracy and legality of the document during collaborative editing processes.",
                  "When I need to draft a new legal agreement from scratch, I want the text editor to provide customizable legal templates and clauses, so that I can expedite the contract creation process while ensuring compliance with legal standards.",
                  "When I have to compare two versions of a contract to identify the differences, I want the text editor to have a clear, user-friendly comparison feature, so that I can quickly pinpoint any modifications and ensure the accuracy of the changes made.",
                  "When I'm preparing legal documentation for client presentations or court submissions, I want the text editor to support easy export to PDF with formatting consistency, so that I can deliver professional-looking documents that adhere to industry standards."]) +
              jobs("Sarah Smith, Sales Manager / HR Manager, Compass Industries", ["When I'm creating a new employment contract for a new hire, I want the text editor to offer a streamlined way to input specific terms and conditions, so that I can ensure all necessary employment details are accurately captured and legally compliant.",
                  "When I'm sending out sales proposals to potential clients, I want the text editor to provide seamless integration with our CRM system, so that I can easily keep track of communication and follow up on the proposal's progress.",
                  "When I'm onboarding new employees and need to handle multiple documents, I want the text editor to enable easy document organization and categorization, so that I can efficiently manage the influx of paperwork during the onboarding process.",
                  "When I'm collaborating with the legal team on contract negotiations, I want the text editor to facilitate smooth communication and feedback exchange, so that we can swiftly finalize contracts with mutually agreed-upon terms and conditions."]) + '</div>', "sub") +
          sec("IV. Metrics", body(ps("Quantitative and qualitative metrics are essential for evaluating different aspects of a product. Quantitative metrics provide numerical data, allowing teams to measure specific outcomes and track changes over time. Qualitative metrics offer insights into user perceptions, experiences, and behaviors."),
              h3("Qualitative targets"),
              ul("Improved collaboration and communication feedback. Collecting customer feedback to assess improvements in collaboration and communication resulting from the implementation of the text editor.",
                 "Ease of integration with existing workflows. Assessing how seamlessly the text editor integrates with the existing workflow processes of the organization, minimizing disruptions and maximizing productivity."),
              h3("Quantitative targets"),
              ul("Percentage of import usage. Share of users importing documents into the updated text editor for editing or updating existing contracts and agreements, relative to the total number of users over a specific period of time.",
                 "Percentage of Word/PDF export usage. Proportion of users exporting created documents from the updated text editor to Word/PDF format for further work or exchange, relative to the total number of users over a specific period of time.",
                 "Feature adoption rate. Percentage of users actively using key features (such as template creation, version control, PDF export) in the text editor compared to the total number of users over a specific period.",
                 "Percentage of documents created from templates. Share of documents that were created based on pre-prepared document templates compared to the overall number of created documents.")), "sub") +
          sec("V. Design solution", body(ps("And finally, the design solution for the new editor. Its testing, refinement, and the metrics verification can be discussed in more detail during a personal interview.")) +
              shots("juro", range(1, 13), "c3"), "sub") +
          sec("VI. Checking", body(ps("This section examines the impact of the design solution by assessing key metrics. It serves as a critical evaluation of how the design improvements affected user engagement and behavior."),
              h3("Qualitative results"),
              ul("Customer feedback highlighting improved collaboration and communication as a result of the text editor's implementation, indicating smoother workflows and enhanced teamwork.",
                 "Positive feedback from users regarding the seamless integration of the text editor with existing workflows, leading to reduced disruptions and increased overall productivity within the organization."),
              h3("Quantitative results"),
              ul("29.5% increase in the number of documents imported into the updated text editor over a month.",
                 "2.5% decrease in users exporting documents to Word/PDF format after the update.",
                 "19% increase in users actively utilizing key features in the text editor over a specific period, compared to the previous rate.",
                 "6.6% of documents created based on pre-prepared templates, compared to the previous rate.")), "sub"))
    if slug == "sweed":
        return (
          sec("Company", body(ps("Sweed is a U.S.-based AI-powered point-of-sale platform tailored for regulated retail businesses. Founded in 2021, it unifies checkout, inventory, e-commerce, and delivery management into a single system, helping companies stay compliant and efficient in complex regulatory environments."))) +
          sec("Role", body(ps("At Sweed, I led design across multiple product streams for the internal admin platform during rapid growth, acting as a design lead and cross-team connector.",
              "I drove the redesign of core operational workflows, which reduced support load by ~15% and increased engagement with new admin workflows by ~25%. Alongside delivery, I provided design leadership, aligning product and engineering around shared UX principles, mentoring designers, and shaping a consistent, scalable admin platform that became a central control hub for the Sweed ecosystem."))) +
          sec("Results", nums([("−15%", "Support load", "Redesign of core operational workflows"), ("+25%", "Engagement with new admin workflows", "")])) +
          sec("Case study", '<p class="state">Designing the Admin Portal End-to-End Across All Product Streams</p>' +
              body(ps("In Sweed Portal I worked across the entire admin platform, not a single vertical. I was responsible for the UX and cross-stream consistency of key product modules.",
                      "Even though my formal title was Senior Product Designer, the scope of responsibility and impact was closer to a Staff level role: I connected multiple teams, unified interaction patterns, aligned product logic between modules and ensured a seamless, predictable UX across the whole portal."))) +
          sec("I. Dashboard / Reports / Money / Inventory", body(ps("These are the core operational modules of the portal that store managers and back-office teams work with every day."),
              ul("Dashboard provides a quick operational snapshot of store performance", "Reports: analytics and performance tracking across locations", "Money: shift and cashflow control and reconciliation", "Inventory: stock operations, purchases, adjustments and transfers"),
              ps("Together, these sections power the daily operational backbone of the retail workflow.",
                 "When I joined, these areas were already live, but required design ownership as they were evolving quickly across multiple product streams. I was responsible for refining and extending the existing UX, maintaining consistency between modules, and integrating new features without breaking user expectations. This included restructuring interactions, improving data hierarchy and edge cases, aligning patterns, and scaling layouts for new functionality.",
                 "My role was to make these modules more predictable and stable from a UX perspective as they continued to grow. Rather than designing one-off pages, I worked at the system level, ensuring that each change fit into a cohesive logic shared across the portal.")) +
              shots("sweed", range(1, 7)) + '<p class="lbl gray cap">Not every subsection is shown, only the representative ones</p>', "sub") +
          sec("II. Customers", body(ps("The Customers module is the foundation of the portal’s buyer management and patient verification logic. It is used by dispensary staff to validate identities, maintain medical records, manage documents, connect caregivers to patients, and handle compliance checks before a sale. This section also ties customer profiles to loyalty, segmentation and e-commerce identity, making it a central hub for everything related to the end user inside the portal.",
              "My work here focused on extending and maturing the existing UX: improving flows around validation, document management and medical eligibility, clarifying states and edge cases, and supporting compliance integrations. I also streamlined navigation patterns and reworked key interaction points to reduce friction for high-frequency operational tasks.",
              "Because this module directly affects the checkout experience and compliance risk, it needed clarity, predictability and robustness more than visual novelty. I ensured consistency with the rest of the portal while supporting new business logic and regulatory requirements as they appeared.",
              "Beyond individual screens, a large part of the work in this module was about shaping the system-level rules that govern customer states: how and when eligibility changes, which validations are blocking vs non-blocking, how caregiver relationships cascade through the experience, and when compliance overrides UI choices. This meant collaborating closely with product and engineering to define edge scenarios and prevent accidental loopholes that could lead to regulatory violations or checkout failure. The result is a more resilient, transparent layer of customer logic that other modules can reliably build upon.")) +
              shots("sweed", range(7, 13)), "sub") +
          sec("III. E-commerce / Marketing", body(ps("E-commerce in the portal is responsible for the configuration and management of the online storefront: product availability, pickup and delivery flows, dispatching logic and customer-facing experience. Marketing is tightly connected to it, enabling targeted campaigns, promotions, segmentation and loyalty mechanics that drive returning traffic and higher conversion. These two sections work as the growth layer of the platform, turning inventory and operational data into real revenue through personalization and engagement.",
              "My work here involved refining the configuration flows, aligning the logic of delivery and assignment with store-level settings, and improving the usability of tools used by non-technical staff. I also ensured visual and interaction consistency between marketing tools and e-commerce settings so that campaign creation, offer logic and storefront rules feel like part of a single system rather than separate features.",
              "Unlike the operational modules, this part of the portal required more attention to business intent and user mental models (what the manager expects to happen vs what the system actually does). A big part of the work was reducing hidden states and clarifying cause-and-effect in configuration screens, so that store admins could understand not only what they are setting up, but also how it will affect the live storefront and campaigns.",
              "On a system level, this work was about making configuration predictable enough that business outcomes become intentional rather than accidental. Many of these controls influence pricing visibility, eligibility, delivery promise and campaign triggers, which means that a small UX ambiguity can translate into lost revenue or misaligned offers on the storefront. By unifying the logic behind these controls and exposing key dependencies more transparently, I helped turn E-commerce and Marketing into a more reliable growth engine, rather than a set of isolated settings screens.")) +
              shots("sweed", range(13, 19)), "sub") +
          sec("IV. Store Setup", body(ps("Store Setup is the configuration layer of the portal. This is where the structure of the store is defined: products, brands, categories, taxes, permissions, hardware, fulfillment rules and compliance-driven constraints. Put simply, this section controls what the business actually looks like operationally, before any sales or campaigns even happen.",
              "My role here was to evolve and maintain the UX for these foundational settings so that the portal remains scalable as new features and regulatory requirements appear. This included refining navigation hierarchy, clarifying dependencies between settings, and making complex configurations easier to apply without breaking the store logic. Many of the flows in Store Setup are high-impact: a single wrong setting can change pricing, eligibility or fulfillment, so the UX here had to reinforce safety and clarity.",
              "Unlike more transactional sections, Store Setup is a source-of-truth module, and most downstream experiences (POS, E-commerce, Inventory, Marketing) depend directly on it. A key part of the design work was ensuring that store operators can configure advanced behaviors without needing deep system knowledge.",
              "Because this section acts as the operational foundation of the portal, a large portion of the UX work was not about visual changes but about modeling the logic behind settings: which options should be global vs store-level, which controls should be grouped, and what should be surfaced only in advanced menus. A big challenge was reducing cognitive load while still allowing full configurability for power users. This required careful prioritization of defaults, progressive disclosure, and structuring dependencies so that the system helps guide the user toward valid configurations.")) +
              shots("sweed", range(19, 25)), "sub") +
          sec("V. Settings", body(ps("Settings is the infrastructure layer of the portal. This is where global behavior of the system is defined: organization-level rules, compliance integrations, timezones, delivery constraints, automation defaults and platform-level toggles. It is less visible to end users but is the backbone of the entire portal logic. My responsibility here was to support the growing complexity of platform-level configuration while maintaining a clean, predictable UX model.",
              "Much of the work was about untangling technical concepts into understandable controls, consolidating scattered toggles into structured groups, and ensuring that sensitive changes (compliance, integrations, state-level rules) are both traceable and safe to edit. In contrast to Store Setup, which configures a store, Settings configures how the platform behaves as a system. This required tighter alignment with backend logic, integration flows and governance rules, and a focus on clarity over visual novelty.",
              "A significant part of the work in this area was establishing clear boundaries between organization-level and store-level logic, so that configuration changes have predictable scope and do not accidentally cascade across locations. This meant rethinking how inheritance, overrides and defaults are exposed to the user, and ensuring that the interface communicates not only what is being changed, but where and to what extent it will take effect.",
              "Unlike front-facing modules, design changes here have long-term architectural consequences: a poorly structured setting today becomes technical debt for all future features. Because many of the controls in Settings are prerequisites for other modules to function at all, the design work required a system-thinking mindset: making sure configuration is auditable, reversible when possible, and resistant to misconfiguration. The goal was to make platform-wide decisions safer, not just easier to click through.")) +
              shots("sweed", range(25, 31)), "sub"))
    if slug == "microsoft-azure":
        return (
          sec("Company", body(ps("Microsoft Azure is one of the world’s largest cloud platforms, used across enterprises and engineering teams globally. At this scale, even internal tools must meet strict reliability, governance and security standards, because small UX decisions impact thousands of users and downstream workflows."))) +
          sec("Project", body(ps("I worked with the Azure team on designing an internal feedback processing system used by product and engineering teams to collect, normalize and act on user insights at scale. The goal was to turn fragmented input from multiple sources into structured, decision-ready data, helping teams prioritize improvements and close the loop with users more effectively."))) +
          sec("Role", body(ps("My role covered discovery, UX architecture, interaction design and collaboration with engineering to ensure the system integrated cleanly into Azure’s internal workflows. I translated complex requirements from multiple stakeholder groups into a unified model of how feedback is captured, routed, enriched and resolved, turning it from a passive inbox into an actionable product signal.")) +
              shots("azure", range(1, 6))))
    if slug == "real-time-tech":
        return (
          sec("Company", body(ps("Real Time Technologies was developing a live-streaming platform Webka that combined Twitch-style interactivity with the structured format of MasterClass, built for teaching and professional sessions rather than entertainment. The product launched on desktop and mobile."))) +
          sec("Role", body(ps("I led the design of the platform’s core experience: streaming interfaces, viewer interaction models, discovery and session tools, onboarding for creators, and internal studio tools. My role covered both product definition and UX: translating live teaching workflows into a scalable interaction model, designing controls that work in real time, and ensuring low-friction engagement for different audience types.",
              "I conducted research with streamers and early adopters, validated participation mechanics, and helped evolve the interface through several iterations as new use cases emerged. In parallel, I managed the design direction for the wider product team: aligning interaction patterns across desktop and mobile, mentoring designers, and working closely with engineering to ensure performance and usability in live conditions.")) +
              shots("webka", range(1, 7))))
    if slug == "it-test":
        return (
          sec("Company", body(ps("IT Test is a mobile and software development studio. I joined as the sole UX/UI designer and later built and led the internal design team. The key product I worked on was Freezio, a 3D training and visualization app for figure skaters, used by athletes and coaches worldwide."))) +
          sec("Role", body(ps("My role covered the full product cycle: user research, translating domain-specific training workflows into interface logic, prototyping interaction models, creating UI, and supporting engineering during implementation.",
              "As the product grew, I was responsible not only for design execution, but also for shaping the long-term product direction: defining how onboarding should work for both athletes and coaches, what level of visual abstraction was needed to make complex movements understandable on mobile, and how to balance consumer accessibility with professional detail.",
              "Over time, I also formalized design practices inside the company, mentored new designers, and aligned multiple products around a consistent UX approach. Beyond Freezio, I contributed to other applications within the studio, helping transition the company from feature delivery to a more product-led mindset.")) +
              shots("freezio", range(1, 6))))
    if slug == "inter-rao":
        return (
          sec("Company", body(ps("Inter RAO is one of the largest state-linked energy holdings in Eastern Europe and the CIS, operating across generation, trading and energy distribution. The company manages a wide network of subsidiaries, which makes internal coordination highly regulated and legally sensitive."))) +
          sec("Role", body(ps("When I joined the company, the UX/UI profession was still in its formative stage. My official title was Interface Designer, but in practice I was responsible for the full product design cycle: from research and prototyping to UI and implementation support.",
              "I designed a mobile document management system that allowed employees to review, approve and sign internal documents remotely, significantly accelerating internal decision-making workflows. Before this project, approvals were often tied to desktop access, which created delays, especially for managers who traveled frequently between branches. The mobile application introduced real-time visibility and status tracking, enabling faster cross-department collaboration and shortening approval cycles."))) +
          sec("Outcome", body(ps("This product is still in use inside the company today (with only minor updates), which validates both the durability of the UX model and the robustness of the original information architecture. At that time there were no established design systems or mature UX methodologies in the region, so many of the patterns had to be developed from first principles. The experience shaped my early approach to product design: focusing on clarity, structured logic and long-term maintainability rather than a visual refresh.")) +
              shots("interrao", range(1, 11), "c5")))
    raise KeyError(slug)

def case(i):
    c = CASES[i]; nx = CASES[(i + 1) % len(CASES)]
    link = ('<a class="lbl" href="%s" target="_blank" rel="noopener" style="text-decoration:underline;text-underline-offset:.25em">%s</a>' % (c["link"][1], c["link"][0])) if c.get("link") else ""
    main = phead("Case %02d / %02d" % (i + 1, len(CASES))) + f'''  <div class="ctitle">
    <h1>{esc(c["title"])}</h1>
    <div class="cm"><span class="lbl">{esc(c["role"])}</span><span class="lbl gray">{esc(c["period"])}</span>{link}</div>
  </div>
  <div class="cvid"><video src="{c["video"]}" muted loop playsinline autoplay preload="auto"></video></div>
''' + content(c["slug"]) + f'''  <div class="rows nextc" style="border-top:1px solid var(--ink)">
    <a class="gl" href="{nx["href"]}"><span class="g">{esc(nx["title"])}{ARROW}</span><span class="side lbl">Next case<br><span class="gray">{esc(nx["role"])}</span></span></a>
  </div>
'''
    js = '''<script>(function(){var v=document.querySelector(".cvid video");if(!v)return;function k(){if(v.paused){var p=v.play();p&&p.catch&&p.catch(function(){})}}
v.addEventListener("canplay",k);["pointerdown","touchstart","scroll"].forEach(function(e){addEventListener(e,k,{passive:true,once:true})});})();</script>
'''
    return shell(c["slug"], "%s · Yuri Zavorotny" % c["title"], main, js)

os.makedirs(out, exist_ok=True)
def w(name, s):
    assert "—" not in re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S), name   # без длинных тире в тексте
    open(os.path.join(out, name), "w", encoding="utf-8").write(s)
w("index.html", home()); w("about.html", about()); w("contact.html", contact())
for i, c in enumerate(CASES): w(c["href"], case(i))
print("ok", out)
