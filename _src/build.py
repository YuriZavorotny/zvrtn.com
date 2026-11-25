# -*- coding: utf-8 -*-
"""Сборка сайта: python3 build.py <out_dir> <home_href>
   home_href: "index.html" для локальной папки, "./" для опубликованной версии."""
import sys, json, html, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
out, HOME = sys.argv[1], sys.argv[2]
esc = html.escape
BG = "#ecebe8"          # светло-серый фон сайта
BG_RGB = [0xec / 255, 0xeb / 255, 0xe8 / 255]

FONTS = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter+Tight:wght@400..700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">'''

AR_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="butt" stroke-linejoin="miter"><path d="M1 12H22"/><path d="M15 5l7 7-7 7"/></svg>'
ARROW = '<span class="ar" aria-hidden="true">%s</span>' % AR_SVG
ICO_COPY = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path class="i1" d="M8.5 8.5h11v12h-11z M15.5 8.5v-5h-11v12h4"/><path class="i2" d="M4 12.5l5.5 5.5L20 6.5"/></svg>'
ICO_OUT = '<svg class="out" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 19L19 5"/><path d="M8.5 5H19v10.5"/></svg>'

CASES = [
 dict(slug="sweed", title="Sweed", role="Senior/Staff Product Designer", period="Dec 2023 – Feb 2026", video="v/sweed.mp4", big=True,
      product="AI marketing and admin platform for regulated retail", link=("sweedpos.com", "https://www.sweedpos.com"),
      metric=["Orders placed 2.8x", "Open rate +19%", "CTR +12%", "Revenue per user +$27"]),
 dict(slug="juro", title="Juro", role="Lead Product Designer", period="Sep 2020 – Dec 2023", video="v/juro.mp4", big=True,
      product="Contract editor, legal tech SaaS", link=("juro.com", "https://juro.com"),
      metric=["Document import +29.5%", "Key feature adoption +19%", "6,000+ customers"]),
 dict(slug="microsoft-azure", title="Microsoft Azure", role="UX Expert", period="Oct 2019 – Sep 2020", video="v/azure.mp4", big=True,
      product="Internal feedback processing system", link=("feedbackportal.microsoft.com", "https://feedbackportal.microsoft.com/feedback/"),
      metric=["Feedback processing 2.7x", "Requests analyzed per day +170%", "~200 feedback items a day"]),
 dict(slug="real-time-tech", title="Real Time Tech", role="Senior Product Designer", period="Oct 2017 – Oct 2019", video="v/webka.mp4",
      product="Webka, live-streaming platform", link=("webka.com", "https://webka.com/air/3CZW98Zhk4"),
      stores=[("Google Play", "https://play.google.com/store/apps/details?id=com.webka.app"), ("App Store", "https://apps.apple.com/ru/app/webka-com/id1534358718?l=en-GB")]),
 dict(slug="it-test", title="IT Test", role="Lead UX/UI Designer", period="Dec 2015 – Oct 2017", video="v/freezio.mp4",
      product="Freezio, 3D app for figure skaters",
      stores=[("App Store", "https://apps.apple.com/us/app/freezio-figure-skating-3d-app/id1465212617")]),
 dict(slug="inter-rao", title="Inter RAO", role="UX/UI Designer", period="Feb 2013 – Dec 2015", video="v/inter-rao.mp4",
      product="Mobile document management", link=("interrao.lt", "https://interrao.lt")),
]
for c in CASES: c["href"] = "case-%s.html" % c["slug"]

# ------------------------------------------------------------------ CSS
CSS = r'''
:root{
  --bg:%(BG)s; --ink:#000; --gray:#86857f; --soft:#55544f; --line:rgba(0,0,0,.13); --panel:#fff;
  --serif:"Instrument Serif","Times New Roman",serif;                 /* антиква: крупные высказывания */
  --grot:"Inter Tight","Helvetica Neue",Helvetica,Arial,sans-serif;   /* гротеск: акценты, имена, длинный текст */
  --mono:"IBM Plex Mono",ui-monospace,Menlo,monospace;                /* моно: служебное */
  --u:calc(min(100vw,1741px)/1024);
  --m:calc(40*var(--u));
  --lbl:max(11.5px,calc(9.6*var(--u)));
  --lbs:max(10.5px,calc(8.4*var(--u)));
  --hh:max(46px,calc(34*var(--u)));      /* высота шапки */
  --ease:cubic-bezier(.65,0,.35,1);
}
*{box-sizing:border-box}
html{background:var(--bg)}
html,body{overflow-x:clip}
body{margin:0;background:transparent;color:var(--ink);font-family:var(--grot);-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
a{color:inherit;text-decoration:none}
p,h1,h2,h3,figure,ul,dl,dd,dt,blockquote{margin:0;padding:0}
ul{list-style:none}
button{font:inherit;color:inherit;background:none;border:0;padding:0;cursor:pointer}
img,video{display:block;max-width:100%%}

.lbl,.top nav a,.top .ddb,.foot a,.foot span{font-family:var(--mono);font-weight:500;font-size:var(--lbl);line-height:1.5;text-transform:uppercase;letter-spacing:.04em}
.gray{color:var(--gray)}

#gl{position:fixed;inset:0;width:100%%;height:100%%;z-index:0;pointer-events:none;display:block}

/* ---------- шапка: прозрачная наверху, матовое стекло при прокрутке ---------- */
.top{position:fixed;z-index:20;top:0;left:0;right:0;display:flex;align-items:center;justify-content:space-between;height:var(--hh);padding:0 var(--m)}
.top::before{content:"";position:absolute;inset:0;z-index:-1;background:rgba(236,235,232,.88);
  -webkit-backdrop-filter:blur(30px) saturate(1.6);backdrop-filter:blur(30px) saturate(1.6)}
.top::before{opacity:0;transition:opacity .45s;box-shadow:0 1px 0 rgba(0,0,0,.09)}
.top.sc::before{opacity:1}
.top .me{font-family:var(--mono);font-weight:500;font-size:var(--lbl);letter-spacing:.04em;text-transform:uppercase;line-height:1.3;position:relative}
.top .me::after{content:"";position:absolute;left:0;right:0;bottom:-2px;height:1px;background:currentColor;transform:scaleX(0);transform-origin:left;transition:transform .6s var(--ease)}
.top .me:hover::after{transform:scaleX(1)}
.top nav{display:flex;align-items:center;gap:calc(32*var(--u))}
.top nav a,.foot a,.top .ddb{position:relative;line-height:1.3}
.top nav>a::after,.foot a::after,.top .ddb .t::after,.ul::after{content:"";position:absolute;left:0;right:0;bottom:-2px;height:1px;background:currentColor;transform:scaleX(0);transform-origin:left;transition:transform .6s var(--ease)}
.top nav>a:hover::after,.foot a:hover::after,.top nav>a.on::after,.dd.open .ddb .t::after,.dd.on .ddb .t::after,.ul:hover::after{transform:scaleX(1)}
.ul{position:relative}
.dd{position:relative;display:flex;align-items:center;height:var(--hh)}
.ddb{display:inline-flex;align-items:center;gap:.5em}
.ddb .t{position:relative}
.ddb .car{width:.45em;height:.45em;border-right:1.5px solid currentColor;border-bottom:1.5px solid currentColor;transform:translateY(-25%%) rotate(45deg);transition:transform .4s var(--ease)}
.dd.open .ddb .car{transform:translateY(15%%) rotate(225deg)}
.ddp{position:absolute;top:calc(100%% - 6px);right:calc(-1.4*var(--lbl));padding:.7em calc(1.4*var(--lbl)) .9em;white-space:nowrap;background:#262624;color:#ecebe8;
  visibility:hidden;opacity:0;transition:opacity .25s,visibility 0s .25s}
.dd.open .ddp{visibility:visible;opacity:1;transition:opacity .25s}
.ddp a{display:flex;align-items:center;padding:.42em 0;transition:color .3s}
.ddp .ar svg{transform:translateX(-110%%)}
.ddp a:hover .ar{width:1.5em}
.ddp .ar svg{left:0;right:auto}
.ddp a:hover .ar svg{transform:none}
.ddp .ar{height:.9em}.ddp .ar svg{width:.9em;height:.9em}
.ddp a.on{color:#8a8983}

/* ---------- каркас ---------- */
.stage,.page{position:relative;z-index:1;width:100%%;max-width:1741px;margin:0 auto}
.phead{display:flex;justify-content:space-between;align-items:baseline;gap:20px;margin:0 var(--m);padding:calc(190*var(--u)) 0 calc(12*var(--u));border-bottom:1px solid var(--line);color:var(--gray)}
.phead nav{display:flex;gap:2.2em}
.sec{margin:0 var(--m);padding:calc(26*var(--u)) 0 calc(96*var(--u));border-top:1px solid var(--line);display:grid;grid-template-columns:calc(236*var(--u)) 1fr;column-gap:calc(20*var(--u))}
.sec.first{border-top:0;padding-top:calc(40*var(--u))}

.big{font-family:var(--serif);font-weight:400;font-size:max(32px,calc(60*var(--u)));line-height:.95;text-transform:uppercase;letter-spacing:-.008em}
.big b{font-family:var(--grot);font-weight:700;letter-spacing:-.022em}
.big .nw{white-space:nowrap}
@media (min-width:700px){.big .nwd{white-space:nowrap}}
.big .hmb{display:none}
/* антиква для высказываний: отзывы, about, выноски в кейсах */
.say{font-family:var(--serif);font-weight:400;font-size:max(20px,calc(17.5*var(--u)));line-height:1.14;letter-spacing:-.004em}
.say+.say{margin-top:.7em}
.rq{font-family:var(--grot);font-weight:450;font-size:max(17px,calc(13*var(--u)));line-height:1.42;letter-spacing:-.003em}
.rq+.rq{margin-top:.8em}
.ptop{height:calc(190*var(--u))}
.nm2{font-family:var(--grot);font-weight:700;font-size:max(13px,calc(11*var(--u)));letter-spacing:-.02em}
/* гротеск: длинный текст */
.body{font-family:var(--grot);font-weight:450;font-size:max(15px,calc(10.2*var(--u)));line-height:1.55;letter-spacing:.004em;max-width:58ch}
.body p{text-wrap:pretty}
.body p+p{margin-top:.95em}
.body ul{margin:.95em 0}
.body li{position:relative;padding-left:1.4em;margin-top:.4em}
.body li::before{content:"";position:absolute;left:0;top:.74em;width:.7em;height:1px;background:currentColor}
.body.soft{color:var(--soft)}
.h3{font-family:var(--grot);font-weight:700;font-size:max(14px,calc(11*var(--u)));letter-spacing:-.02em;line-height:1.2;margin-bottom:.7em}

.ar{display:inline-block;position:relative;width:0;height:.62em;overflow:hidden;vertical-align:baseline;transition:width .36s var(--ease)}
.ar svg{position:absolute;right:0;top:0;width:.62em;height:.62em;transform:translateX(-110%%);transition:transform .36s var(--ease)}
.hov .ar{width:.84em}.hov .ar svg{transform:none}
@media (hover:hover){a:hover>.g>.ar,a:hover>.ar,.gl:hover .ar{width:.84em}a:hover>.g>.ar svg,a:hover>.ar svg,.gl:hover .ar svg{transform:none}}

/* ---------- главная ---------- */
.hero{padding:calc(180*var(--u)) var(--m) calc(34*var(--u))}
@media (min-width:700px){.hero{box-sizing:border-box;min-height:calc(89svh - 56*var(--u) - 62px);padding-top:calc(110*var(--u));padding-bottom:calc(56*var(--u));display:flex;flex-direction:column;justify-content:flex-end}}
.hero .big{text-wrap:pretty}
.inkw{display:grid}

.inkw>*{grid-area:1/1}
.inkw .ink{pointer-events:none;color:transparent;opacity:0;transition:opacity .5s;filter:url(#oilf);
  background:linear-gradient(105deg,#5a5cff,#36c9c3,#c48bff,#ffb86b,#ff7fc4,#5a5cff) 0 0/300%% 100%%;-webkit-background-clip:text;background-clip:text}
.inkw .ink b{color:transparent}
.inkw.on .ink{opacity:1}
.hint{display:flex;justify-content:space-between;align-items:center;margin:0 var(--m) calc(64*var(--u));padding-top:max(16px,calc(22*var(--u)));border-top:1px solid var(--line);color:var(--gray)}
.inkw,.inkw *{cursor:default}
.hint .dn{display:inline-flex;align-items:center;gap:.7em}
.hint .dn svg{width:.9em;height:.9em;transform:rotate(90deg);animation:bob 1.8s var(--ease) infinite}
@keyframes bob{0%%,100%%{translate:0 -3px}50%%{translate:0 3px}}

#list{position:relative;height:calc(1160*var(--u))}
.row{position:absolute;left:0;right:0;top:calc(var(--y)*var(--u));height:calc(280*var(--u));pointer-events:none}
.asset{position:absolute;top:0;width:calc(449*var(--u));height:calc(280*var(--u));pointer-events:auto;background:transparent;display:block}
.asset video{position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover}
.row.r .asset{left:calc(440*var(--u))}
.row.l .asset{left:calc(135*var(--u))}
.txt{position:absolute;top:0;width:calc(300*var(--u));pointer-events:auto;display:block}
.row.r .txt{left:calc(76*var(--u))}
.row.l .txt{left:calc(648*var(--u))}
.ttl{font-family:var(--serif);font-weight:400;text-transform:uppercase;font-size:max(30px,calc(34*var(--u)));line-height:.9;letter-spacing:-.005em;margin-top:-.09em}
.meta{margin-top:calc(16*var(--u))}
.meta .mt{color:var(--gray)}
.meta .dt + .mt{margin-top:.9em}
.item.gl-on .asset video{opacity:0}
.asset video{transition:filter .45s,opacity .45s}
@media (hover:hover){.stage:has(.item.hov) .item:not(.hov):not(.gl-on) .asset video{filter:grayscale(1);opacity:.38}}
/* ранние работы: три колонки поменьше */
.early{margin:calc(170*var(--u)) var(--m) 0;display:grid;grid-template-columns:calc(236*var(--u)) 1fr;column-gap:calc(20*var(--u))}
.early .grid3{display:grid;grid-template-columns:repeat(3,1fr);column-gap:calc(40*var(--u))}
.early .asset{position:relative;width:100%%;height:auto;aspect-ratio:449/280}
.early .txt{position:static;width:auto;margin-top:calc(18*var(--u))}
.early .ttl{font-size:max(20px,calc(17*var(--u)))}
.early .meta{margin-top:calc(9*var(--u))}
.early .meta .lbl{font-size:var(--lbs);color:var(--gray)}
.early .meta .mt{display:none}
.scr-pre{visibility:hidden}
.scr-w{white-space:nowrap}
.scr-c{display:inline-block;text-align:left;white-space:pre}
.top nav>a,.foot a{display:inline-block;height:1.3em}
.top nav .scr-w,.top nav .scr-c,.foot .scr-w,.foot .scr-c{vertical-align:top;line-height:1.3;height:1.3em}

.recs{margin:calc(150*var(--u)) var(--m) 0;padding:calc(96*var(--u)) calc(60*var(--u)) 0;border-top:1px solid var(--line)}
.recs .grid{display:grid;grid-template-columns:1fr 1fr;column-gap:calc(90*var(--u));row-gap:calc(64*var(--u))}
.recs .nm2 a{display:inline-flex;align-items:center;gap:.35em}.recs .nm2 .out{opacity:.45}
.recs q{display:block;quotes:none;max-width:52ch}
.recs .nm2,.abt .sig .nm2{font-family:var(--mono);font-weight:500;font-size:var(--lbl);letter-spacing:.04em;text-transform:uppercase}
.recs figcaption{margin-top:max(18px,calc(22*var(--u)))}
.recs .more{display:inline-flex;align-items:center;gap:.6em;margin-top:calc(72*var(--u))}
.out{width:.8em;height:.8em}

.foot{display:flex;justify-content:space-between;align-items:baseline;padding:calc(150*var(--u)) var(--m) calc(28*var(--u))}
.foot nav{display:flex;gap:calc(32*var(--u))}

/* ---------- contact ---------- */
.rows{margin:0 var(--m)}
.one{height:100vh;height:100svh;display:flex;flex-direction:column;overflow:hidden}
.one .phead{padding-top:max(110px,calc(150*var(--u)))}
.one .rows{margin-top:0}
.one .foot{margin-top:auto;padding-top:20px}
.gl{display:flex;align-items:baseline;justify-content:space-between;gap:calc(30*var(--u));padding:calc(16*var(--u)) 0 calc(7*var(--u));border-bottom:1px solid var(--line);transition:color .5s var(--ease)}
.gl .g{font-family:var(--serif);font-weight:400;text-transform:uppercase;font-size:max(38px,calc(50*var(--u)));line-height:.92;letter-spacing:-.01em;flex:1}
.gl .side{display:flex;align-items:center;gap:1em;flex:none;padding-bottom:calc(6*var(--u))}
@media (hover:hover){.rows:hover .gl{color:var(--gray)}.rows:hover .gl:hover{color:var(--ink)}}
@media (hover:none){.rows:has(.gl.hov) .gl:not(.hov){color:var(--gray)}}
.gl{-webkit-touch-callout:none;-webkit-user-select:none;user-select:none}
.cpi{display:inline-flex;width:1.5em;height:1.5em;align-items:center;justify-content:center;color:var(--ink);opacity:.55;transition:opacity .3s}
.cpi:hover{opacity:1}
.gl .side a{user-select:text;-webkit-user-select:text;-webkit-user-drag:none}
.gl .side:has(.cpi){gap:.5em}
.cpi svg{width:1.15em;height:1.15em}
.foot a.cp{position:relative}.foot a.cp>*{visibility:hidden}.foot a.cp::before{content:"Copied";position:absolute;left:0;top:0;white-space:nowrap}
.cpi .i2{display:none}.cpi.ok .i1{display:none}.cpi.ok .i2{display:block}

/* ---------- about ---------- */
.abt{display:grid;grid-template-columns:calc(150*var(--u)) 1fr;column-gap:calc(56*var(--u));align-items:stretch}
.abt .tx{max-width:calc(430*var(--u))}
.abt .sig{margin-top:calc(22*var(--u))}
.ph{width:100%%}
.ph{position:relative}
.ph .fr{position:absolute;inset:0;overflow:hidden;background:#dedcd7}
.ph img{position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover;object-position:50%% 78%%}

.nums{display:grid;grid-template-columns:1fr 1fr;column-gap:calc(40*var(--u));row-gap:calc(46*var(--u))}
.nums.four{grid-template-columns:repeat(4,1fr)}
.nums b{display:block;font-family:var(--serif);font-weight:400;font-size:max(38px,calc(44*var(--u)));line-height:.88;letter-spacing:-.02em;margin-bottom:calc(12*var(--u))}
.xp li{border-bottom:1px solid var(--line)}
.xp li:first-child .xr{padding-top:0}
.xr{display:grid;grid-template-columns:1.1fr 1.3fr .9fr;align-items:baseline;column-gap:20px;padding:calc(10*var(--u)) 0}
.edu{display:grid;grid-template-columns:1fr 1fr;column-gap:calc(40*var(--u))}
.edu .body{margin:.15em 0 .5em}
.edu .deg{font-family:var(--serif);font-weight:400;text-transform:uppercase;font-size:max(30px,calc(34*var(--u)));line-height:.9;margin-bottom:calc(14*var(--u))}
.edu .lbl{max-width:none;white-space:nowrap}
.nums p{white-space:nowrap}
.nums b{white-space:nowrap}
.xp .co{font-family:var(--grot);font-weight:700;font-size:max(15px,calc(11.5*var(--u)));letter-spacing:-.01em;line-height:1.1}
.xp .yr{text-align:right}
.xp a.xr .co{transition:transform .5s var(--ease)}
@media (hover:hover){.xp a.xr:hover .co{transform:translateX(.35em)}}

/* ---------- кейс ---------- */
.case .chead{display:grid;grid-template-columns:1fr calc(520*var(--u));column-gap:calc(40*var(--u));align-items:start;margin:0 var(--m);padding:calc(56*var(--u)) 0 0}
.chead h1{font-family:var(--serif);font-weight:400;text-transform:uppercase;font-size:max(44px,calc(60*var(--u)));line-height:.86;letter-spacing:-.012em;margin:-.06em 0 0 -.03em}
.chead .links{display:flex;flex-wrap:wrap;gap:.4em 1.6em;margin-top:calc(16*var(--u))}
.chead .links a{display:inline-flex;align-items:center;gap:.45em}
.chead .prod{margin-top:calc(18*var(--u))}
.chead .links{margin-top:calc(18*var(--u))}
.chead .rp{margin-top:calc(34*var(--u))}
.chead .item{position:relative}
.chead .asset{position:relative;display:block;width:100%%;height:auto;aspect-ratio:1152/720;left:auto;top:auto;background:transparent}
.chead .asset video{position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover}
.stores{display:flex;gap:1.6em;flex-wrap:wrap}
.stores a{display:inline-flex;align-items:center;gap:.5em}
/* компания и роль рядом */
.cintro{display:grid;grid-template-columns:calc(300*var(--u)) 1fr;column-gap:calc(96*var(--u));margin:calc(120*var(--u)) var(--m) 0;padding-left:calc(100*var(--u))}
.cintro.solo{grid-template-columns:1fr}.cintro.solo>div{max-width:calc(560*var(--u))}
.cintro .lbl{margin-bottom:1.1em}
.panel{background:var(--panel);margin:calc(84*var(--u)) var(--m) 0;padding:calc(34*var(--u)) calc(40*var(--u)) calc(38*var(--u))}
.panel>.lbl{margin-bottom:calc(26*var(--u))}
.study{margin:calc(130*var(--u)) var(--m) 0;padding-left:calc(100*var(--u))}
.study>h2{max-width:calc(700*var(--u))}.study>.body{max-width:58ch}
.study h2{font-family:var(--serif);font-weight:400;font-size:max(28px,calc(32*var(--u)));line-height:1;letter-spacing:-.01em;margin:calc(14*var(--u)) 0 calc(28*var(--u));text-wrap:balance}
.chap{display:grid;grid-template-columns:calc(250*var(--u)) 1fr;column-gap:calc(60*var(--u));margin:calc(120*var(--u)) var(--m) 0;align-items:start}
.chap .ct{position:sticky;top:calc(var(--hh) + 24px)}
.chap .ct h3{font-family:var(--serif);font-weight:400;font-size:max(22px,calc(20*var(--u)));line-height:1.02;letter-spacing:-.005em;margin-top:.45em;text-wrap:balance}
.pull{font-family:var(--grot);font-weight:700;font-size:max(18px,calc(14.5*var(--u)));line-height:1.22;letter-spacing:-.012em;max-width:26em;margin-bottom:max(16px,calc(20*var(--u)));text-wrap:balance}
.shots{display:grid;grid-template-columns:repeat(2,1fr);gap:calc(8*var(--u));margin-top:calc(40*var(--u))}
.shots.c3{grid-template-columns:repeat(3,1fr)}
.shots.c5{grid-template-columns:repeat(5,1fr)}
.shots.c1{grid-template-columns:1fr}
.vshot{margin-top:calc(40*var(--u))}
.vshot video{display:block;width:100%%;height:auto;aspect-ratio:2000/1196;background:#fff}
.shots figure,.mq figure{position:relative;cursor:zoom-in;overflow:hidden;background:rgba(255,255,255,.35)}
.shots img{width:100%%;height:auto}
.shots img,.mq img{transition:filter .45s,opacity .45s}
.shots:hover figure:not(:hover) img,.mq:hover figure:not(:hover) img,.ndaw:has(figure:hover) figure:not(:hover) img{filter:grayscale(1);opacity:.35}
.ndaw figure{cursor:default}
.cap{font-size:var(--lbs)}
.cap{margin-top:calc(10*var(--u))}
/* компактные карточки Juro */
.cards{display:grid;grid-template-columns:repeat(2,1fr);column-gap:calc(40*var(--u));row-gap:max(34px,calc(48*var(--u)));margin-top:max(24px,calc(36*var(--u)))}
.qc{border-top:1px solid var(--line);padding-top:max(30px,calc(40*var(--u)));display:flex;flex-direction:column;gap:.5em}
.qc .h3{margin:0}
.qc .lbl+.h3{margin-top:-.1em}
.qc cite{margin-top:.5em;font-size:var(--lbs)}
.qc q{quotes:none;font-family:var(--serif);font-size:max(18px,calc(15.5*var(--u)));line-height:1.15}
.qc cite{font-style:normal}
.qc .js{font-size:max(14.5px,calc(9.8*var(--u)));line-height:1.45}
.qc .js b{font-weight:400;color:var(--gray)}
.qc .js+.js{margin-top:.9em}
.qc .h3+.js{margin-top:.5em}
.qs{display:grid;grid-template-columns:repeat(3,1fr);gap:calc(10*var(--u));margin:calc(14*var(--u)) 0 calc(44*var(--u))}
.qs blockquote{background:var(--panel);padding:calc(18*var(--u)) calc(18*var(--u)) calc(16*var(--u));font-size:max(15px,calc(10.6*var(--u)));line-height:1.45;display:flex;flex-direction:column;justify-content:space-between;gap:1.4em}
.qs blockquote:first-child{font-family:var(--serif);font-size:max(20px,calc(16.5*var(--u)));line-height:1.14}
.qs cite{display:block;font-style:normal}
.jobs{display:grid;grid-template-columns:1fr 1fr;gap:calc(10*var(--u));margin:calc(14*var(--u)) 0 calc(44*var(--u))}
.jobs p{background:var(--panel);padding:calc(16*var(--u)) calc(18*var(--u));font-size:max(15px,calc(10.6*var(--u)));line-height:1.45}
.jobs p b{font-weight:400;color:var(--gray)}
.body .h3{margin-top:2em}
.body .h3:first-child{margin-top:0}
/* лента скриншотов */
.mqw{position:relative;width:100vw;margin:calc(120*var(--u)) 0 0 calc(50%% - 50vw);overflow:hidden;cursor:grab;touch-action:pan-y;user-select:none;-webkit-user-select:none}
.mqw.drag,.mqw.drag figure{cursor:grabbing}
.mqw img{-webkit-user-drag:none;pointer-events:none}

.mq{display:flex;gap:calc(8*var(--u));width:max-content;will-change:transform}
.mq figure img{height:var(--h);width:auto;max-width:none}
@keyframes mq{from{transform:translateX(0)}to{transform:translateX(-50%%)}}

/* NDA: маленькая стеклянная плашка */
.ndab{display:flex;width:fit-content;align-items:center;gap:.6em;margin-top:2.4em;padding:.55em 1em;background:rgba(255,255,255,.4);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);box-shadow:inset 0 0 0 1px rgba(255,255,255,.7),0 1px 0 rgba(0,0,0,.06)}
.ndab::before{content:"";width:.55em;height:.45em;border:1.5px solid currentColor;border-top-width:1.5px;margin-top:.25em;box-shadow:0 -.32em 0 -.05em var(--bg),0 -.32em 0 0 currentColor;border-radius:1px}
.lk{display:inline-flex;align-items:center;gap:.5em;margin-top:1.6em}
/* NDA */
.nda{position:relative;width:100vw;margin-left:calc(50%% - 50vw);height:100vh;height:100svh;min-height:520px;margin-top:calc(130*var(--u));background:#000;color:#ecebe8;overflow:hidden;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;cursor:default}
.nda .glow{position:absolute;left:0;top:0;width:calc(560*var(--u));height:calc(560*var(--u));min-width:380px;min-height:380px;border-radius:50%%;pointer-events:none;
  background:radial-gradient(closest-side,rgba(150,180,255,.55),rgba(210,150,255,.28) 38%%,rgba(120,230,210,.12) 62%%,transparent);filter:blur(30px);mix-blend-mode:screen;transform:translate(-50%%,-50%%)}
.nda h2{position:relative;font-family:var(--serif);font-weight:400;text-transform:uppercase;font-size:max(40px,calc(64*var(--u)));line-height:.9;letter-spacing:-.01em}
.nda p{position:relative;margin-top:1.6em;color:#8a8983}
.nums.three{grid-template-columns:repeat(3,1fr)}
.nums>div{min-width:0}
.mbr{display:none}
/* ссылка на Fluent */
.flu{margin:calc(110*var(--u)) var(--m) 0;padding-left:calc(100*var(--u))}
.fluc{display:grid;grid-template-columns:1fr calc(420*var(--u));column-gap:calc(60*var(--u));align-items:end;padding:calc(26*var(--u)) calc(30*var(--u)) calc(28*var(--u));background:rgba(255,255,255,.5);box-shadow:inset 0 0 0 1px rgba(255,255,255,.7);transition:background .4s}
.fluc:hover{background:rgba(255,255,255,.8)}
.fluc>.lbl{grid-column:1/-1;margin-bottom:calc(16*var(--u))}
.fluc .g{font-family:var(--serif);font-weight:400;text-transform:uppercase;font-size:max(30px,calc(38*var(--u)));line-height:.92;letter-spacing:-.01em}
.fluc:hover .ar{width:.84em}.fluc:hover .ar svg{transform:none}
/* NDA: стеклянная завеса поверх скриншотов */
.ndaw{position:relative;margin-top:calc(40*var(--u))}
.ndaw .shots{margin-top:0}
.ndaw .veil{position:absolute;left:0;right:0;bottom:0;top:38%%;-webkit-mask-image:linear-gradient(to bottom,transparent,#000 22%%);mask-image:linear-gradient(to bottom,transparent,#000 22%%);display:flex;align-items:center;justify-content:center;overflow:hidden;
  background:rgba(236,235,232,.2);-webkit-backdrop-filter:blur(0px);backdrop-filter:blur(0px);
  transition:backdrop-filter 1.8s var(--ease),-webkit-backdrop-filter 1.8s var(--ease),background 1.8s}
.ndaw.in .veil{-webkit-backdrop-filter:blur(26px) saturate(1.2);backdrop-filter:blur(26px) saturate(1.2);background:rgba(236,235,232,.45)}
.veil .sheen{position:absolute;inset:-50%%;background:linear-gradient(115deg,transparent 38%%,rgba(150,180,255,.35) 46%%,rgba(225,160,255,.3) 51%%,rgba(140,235,210,.28) 56%%,transparent 64%%);
  transform:translateX(-60%%);animation:sheen 7s cubic-bezier(.45,0,.2,1) infinite;mix-blend-mode:soft-light;pointer-events:none}
@keyframes sheen{0%%{transform:translateX(-60%%)}55%%,100%%{transform:translateX(60%%)}}
.veil .glow{position:absolute;left:var(--gx,50%%);top:var(--gy,50%%);width:calc(420*var(--u));height:calc(420*var(--u));min-width:280px;min-height:280px;transform:translate(-50%%,-50%%);border-radius:50%%;
  background:radial-gradient(closest-side,rgba(255,255,255,.55),rgba(190,200,255,.25) 50%%,transparent);mix-blend-mode:soft-light;pointer-events:none;transition:left .25s,top .25s}
.veil .ndab{position:relative;display:inline-flex;align-items:center;gap:.7em;margin:0;padding:.7em 1.2em;background:rgba(255,255,255,.55);box-shadow:inset 0 0 0 1px rgba(255,255,255,.8),0 8px 30px rgba(0,0,0,.06);
  opacity:0;transform:translateY(10px);transition:opacity .9s .6s,transform .9s .6s var(--ease)}
.ndaw.in .veil .ndab{opacity:1;transform:none}
.veil .ndab::before{content:"";width:.6em;height:.5em;margin-top:.3em;border:1.5px solid currentColor;border-radius:1px;box-shadow:0 -.36em 0 -.06em rgba(255,255,255,.9),0 -.36em 0 0 currentColor}
@media (prefers-reduced-motion:reduce){.veil .sheen{animation:none}}
/* другие работы */
.early .side .lbl+.lbl{margin-top:.3em}
.early .pd{font-family:var(--mono);font-weight:500;font-size:var(--lbs);text-transform:uppercase;letter-spacing:.04em;color:var(--ink);margin-top:calc(10*var(--u))}
.early .meta{margin-top:calc(6*var(--u))}
/* отзывы: имя антиквой со стрелкой */
.recs .rn{display:inline-block;font-family:var(--serif);font-weight:400;text-transform:uppercase;font-size:max(17px,calc(15*var(--u)));line-height:.95;letter-spacing:-.005em}
.recs figure:hover .ar{width:.84em}.recs figure:hover .ar svg{transform:none}
.recs .rl{margin-top:.5em}
/* песок */
.hero .w{display:inline-block;white-space:nowrap}
.hero .c{display:inline-block;will-change:transform;transform-origin:50%% 60%%}
/* переходы между страницами */
html.vt #gl{visibility:hidden}
html.vt .item.gl-on .asset video{opacity:1!important}
/* было / стало */
.cmp{position:relative;margin-top:calc(44*var(--u));user-select:none;-webkit-user-select:none;touch-action:pan-y}
.cmp .in{position:relative;overflow:visible;aspect-ratio:2374/1252}.cmp.drag .in{cursor:grabbing!important}
.cmp img{position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover;pointer-events:none}
.cmp .b{clip-path:inset(0 0 0 var(--p,50%%))}
.cmp .hd{position:absolute;top:0;bottom:0;left:var(--p,50%%);width:1px;background:var(--ink);pointer-events:none;z-index:6}
.cmp .hd::after{content:"";position:absolute;left:50%%;top:50%%;width:calc(24*var(--u));height:calc(24*var(--u));min-width:34px;min-height:34px;transform:translate(-50%%,-50%%);border-radius:50%%;background:var(--ink)}
.cmp .hd svg{position:absolute;z-index:1;left:50%%;top:50%%;width:14px;height:14px;transform:translate(-50%%,-50%%);color:#fff}
.cmp .tg{position:absolute;z-index:3;bottom:calc(10*var(--u));background:var(--ink);color:#fff;padding:.25em .7em;pointer-events:none}
.cmp .tg.l{left:calc(10*var(--u))}.cmp .tg.r{right:calc(10*var(--u))}
/* назад / вперёд */
.pn{display:grid;grid-template-columns:1fr 1fr;column-gap:calc(40*var(--u));margin:calc(170*var(--u)) var(--m) 0}
.pn a{display:block}
.pn a.nx{text-align:right}
.pn .n{font-family:var(--serif);font-weight:400;text-transform:uppercase;font-size:max(28px,calc(34*var(--u)));line-height:.95;margin-top:.25em;display:block}
.pn a:hover .ar{width:.84em}
.pn a.nx:hover .ar svg{transform:none}
.pn a.pv .ar svg{transform:translateX(110%%) rotate(180deg);right:auto;left:0}
.pn a.pv:hover .ar svg{transform:rotate(180deg)}
/* увеличение скриншотов */
.lb{position:fixed;inset:0;z-index:50;background:rgba(236,235,232,.96);display:none;align-items:center;justify-content:center;cursor:zoom-out}
.lb.on{display:flex}
.lb img{max-width:calc(100vw - 2*var(--m));max-height:calc(100vh - 110px);box-shadow:0 0 0 1px var(--line)}
.lb .bar{position:absolute;left:var(--m);right:var(--m);bottom:20px;display:flex;justify-content:space-between;align-items:center}
.lb .bar nav{display:flex;gap:2em}

@media (max-width:700px){
  :root{--m:20px}
  .top nav{gap:16px}
  .ddp{position:fixed;top:var(--hh);left:0;right:0;padding:6px 20px 16px}
  .ddp a{padding:.75em 0}
  .phead{padding:120px 0 10px}
  .sec{grid-template-columns:1fr;row-gap:20px;padding:16px 0 64px}
  .hero{box-sizing:border-box;min-height:calc(88svh - 96px);padding:110px 20px 64px;display:flex;flex-direction:column;justify-content:center}
  .big{font-size:calc((100vw - 40px)*.0975);line-height:1.06}.big .hdt{display:none}.big .hmb{display:inline}
  .hint{margin-bottom:56px}
  #list{height:auto;padding:0}
  .row,.early .item{position:static;height:auto;margin-bottom:104px}
  .asset,.early .asset{position:relative;left:0!important;width:100%%;height:auto;aspect-ratio:449/280}
  .txt,.early .txt{position:static;width:auto;margin-top:18px;padding:0 20px}
  .ttl,.early .ttl{font-size:38px}
  .meta,.early .meta{margin-top:12px}
  .early{margin:0;display:block}.early>.side{display:none}.early .grid3{display:block}
  .recs{padding:48px 0 0;margin-top:0}.recs .grid{grid-template-columns:1fr;row-gap:64px}.recs .rn{font-size:22px}
  .foot{padding:72px 20px 28px;flex-wrap:wrap;gap:12px}.foot nav{gap:16px}
  .gl{flex-direction:column;align-items:flex-start;gap:4px;padding:16px 0 12px}
  .gl .g{font-size:11vw}.gl .side{padding:0}
  .abt{grid-template-columns:1fr;row-gap:30px}.abt .tx{max-width:none}.mbr{display:inline}
  .ph{width:46%%;aspect-ratio:1013/1554}
  .edu{grid-template-columns:1fr;row-gap:28px}
  .nums,.nums.four,.nums.three{grid-template-columns:repeat(2,minmax(0,1fr));row-gap:34px;column-gap:20px}.nums b{font-size:40px}.nums p{white-space:normal}
  .xr{grid-template-columns:1fr auto;column-gap:16px;row-gap:4px;padding:14px 0}.xp .co{grid-column:1;grid-row:1}.xp .yr{grid-column:2;grid-row:1;text-align:right}.xr>.lbl:not(.yr){grid-column:1/-1;grid-row:2}
  .case .chead{grid-template-columns:1fr;row-gap:30px;padding-top:22px}
  .chead h1{font-size:14vw}
  .case .chead{padding-top:28px}
  .chead .rp{margin-top:26px}
  .chead .item{margin:0 -20px}
  .cintro{grid-template-columns:1fr;row-gap:40px;padding:0;margin-top:64px}
  .panel{margin:56px 0 0;padding:24px 20px 28px}
  .study{padding:0;margin-top:80px}
  .chap{grid-template-columns:1fr;row-gap:22px;margin-top:84px}
  .chap .ct{position:static}
  .shots,.shots.c3{grid-template-columns:1fr;gap:8px}.shots.c5{grid-template-columns:1fr 1fr}
  .cmp{margin-left:-20px;margin-right:-20px}.cmp .in{aspect-ratio:2000/1252}
  .vshot,.shots{margin-top:23px}
  .qs,.jobs,.cards{grid-template-columns:1fr}
  .ndaw .shots,.ndaw .shots.c3{margin-left:0;margin-right:0}
  .mqw{margin-top:72px}.mq figure img{height:var(--hm)}
  .pn{margin-top:96px;column-gap:16px}.pn .n{font-size:24px}
}
''' % dict(BG=BG)

# ------------------------------------------------------------------ JS
SCRAMBLE = open(os.path.join(HERE, "scramble.src.js"), encoding="utf-8").read()
SCRAMBLE = SCRAMBLE.replace('".top nav a, .foot span, .foot a, .meta .mt, .recs .rl, [data-scr]"', '".top nav > a, .top .ddb .t, .foot span, .foot a, .meta .lbl, .recs .rl, .case main .lbl, .about main .lbl, [data-scr]"')
SCRAMBLE = SCRAMBLE.replace('function add(el,delay){ if(!el) return;', 'function add(el,delay){ if(!el||el.closest(".mq,.cmp,.ddp")||el.textContent.trim().length>42) return;')
SCRAMBLE = SCRAMBLE.replace('document.querySelectorAll(".top a, .foot a")', 'document.querySelectorAll(".top nav > a, .top .ddb .t, .foot a")')
assert 'length>42' in SCRAMBLE and '.case main .lbl' in SCRAMBLE and '.top .ddb .t, .foot a")' in SCRAMBLE

SCRAMBLE = SCRAMBLE.replace('/* что набираем: только меню */', 'window.__scr=function(el){if(!el.classList.contains("scr-pre"))run(el,"resc",0)};\n/* что набираем: только меню */')
assert 'window.__scr' in SCRAMBLE
COMMON_JS = r'''
/* шапка: подложка появляется при прокрутке */
(function(){var t=document.querySelector(".top");function f(){t.classList.toggle("sc",scrollY>12)}f();addEventListener("scroll",f,{passive:true})})();
/* меню Works */
(function(){
var dd=document.querySelector(".dd"); if(!dd) return;
var b=dd.querySelector(".ddb"),t=null,fine=matchMedia("(hover: hover) and (pointer: fine)").matches;
function set(o){dd.classList.toggle("open",o);b.setAttribute("aria-expanded",o?"true":"false")}
b.addEventListener("click",function(e){e.stopPropagation();set(!dd.classList.contains("open"))});
if(fine){dd.addEventListener("pointerenter",function(){clearTimeout(t);set(true)});dd.addEventListener("pointerleave",function(){t=setTimeout(function(){set(false)},180)})}
document.addEventListener("click",function(e){if(!dd.contains(e.target))set(false)});
document.addEventListener("keydown",function(e){if(e.key==="Escape")set(false)});
})();
/* телефон: активен один блок, ближайший к центру экрана (стрелка, цвет), остальные гаснут */
(function(){
if(!matchMedia("(hover: none)").matches) return;
var raf=0;
function pickIn(sel){var els=[].slice.call(document.querySelectorAll(sel));if(!els.length)return null;var c=innerHeight/2,best=null,bd=1e9;
  els.forEach(function(el){var r=el.getBoundingClientRect(),d=Math.abs((r.top+r.bottom)/2-c);if(d<bd){bd=d;best=el}});
  var on=bd<innerHeight*.5?best:null;els.forEach(function(el){el.classList.toggle("hov",el===on)});return on}
function pick(){raf=0;window.__activeLi=pickIn(".item")}
var held=0;
function sched(){if(!raf&&!held)raf=requestAnimationFrame(pick)}
[].forEach.call(document.querySelectorAll(".gl"),function(g){
  function on(){held=1;[].forEach.call(document.querySelectorAll(".gl"),function(x){x.classList.toggle("hov",x===g)})}
  function off(){setTimeout(function(){held=0;g.classList.remove("hov");sched()},500)}
  g.addEventListener("touchstart",on,{passive:true});g.addEventListener("touchend",off);g.addEventListener("touchcancel",off);
  g.addEventListener("contextmenu",function(e){e.preventDefault()})});
addEventListener("scroll",sched,{passive:true});addEventListener("resize",sched);addEventListener("load",sched);
setTimeout(pick,150);setTimeout(pick,900);
})();
/* NDA: свечение за курсором */
(function(){
var s=document.querySelector(".nda"); if(!s) return;
var g=s.querySelector(".glow"),x=.5,y=.5,tx=.5,ty=.5,on=false,t0=performance.now();
s.addEventListener("pointermove",function(e){var r=s.getBoundingClientRect();tx=(e.clientX-r.left)/r.width;ty=(e.clientY-r.top)/r.height;on=true});
s.addEventListener("pointerleave",function(){on=false});
(function loop(now){
  if(!on){var k=(now-t0)/1000;tx=.5+Math.cos(k*.35)*.22;ty=.5+Math.sin(k*.5)*.18}
  x+=(tx-x)*.07;y+=(ty-y)*.07;
  g.style.left=(x*100).toFixed(2)+"%";g.style.top=(y*100).toFixed(2)+"%";
  requestAnimationFrame(loop)})(t0);
})();
/* ленты скриншотов: бесконечная прокрутка, тянется мышью и колесом */
(function(){
var red=matchMedia("(prefers-reduced-motion: reduce)").matches;
[].forEach.call(document.querySelectorAll(".mqw"),function(w){
  var q=w.querySelector(".mq"),base=[].slice.call(q.children),x=0,half=0,v=0,hover=false,drag=false,sx=0,x0=0,moved=0,last=performance.now();
  base.forEach(function(f,i){f.dataset.k=i});
  function measure(){
    var need=innerWidth*1.15,set=0;base.forEach(function(f){set+=f.getBoundingClientRect().width});if(!set)return;
    var gap=parseFloat(getComputedStyle(q).columnGap)||0;set+=gap*base.length;
    var k=Math.max(1,Math.ceil(need/set));
    while(q.children.length<base.length*k*2){base.forEach(function(f){var c=f.cloneNode(true);c.setAttribute("aria-hidden","true");c.classList.add("cl");q.appendChild(c)})}
    half=set*Math.ceil(q.children.length/base.length/2)}
  function ready(){measure()}
  var imgs=w.querySelectorAll("img"),n=imgs.length;[].forEach.call(imgs,function(i){if(i.complete)n--;else i.addEventListener("load",function(){if(--n<=0)ready()},{once:true})});if(n<=0)ready();
  addEventListener("resize",measure);
  w.addEventListener("pointerenter",function(e){if(e.pointerType==="mouse")hover=true});
  w.addEventListener("pointerleave",function(){hover=false});
  w.addEventListener("pointerdown",function(e){if(e.pointerType==="mouse"&&e.button!==0)return;drag=true;moved=0;sx=e.clientX;x0=x});
  addEventListener("pointermove",function(e){if(!drag)return;var d=e.clientX-sx;moved=Math.max(moved,Math.abs(d));if(moved>6)w.classList.add("drag");x=x0+d});
  function up(){drag=false;w.classList.remove("drag")}
  addEventListener("pointerup",up);addEventListener("pointercancel",up);
  w.addEventListener("click",function(e){if(moved>6){e.stopPropagation();e.preventDefault()}},true);
  w.addEventListener("wheel",function(e){if(Math.abs(e.deltaX)>Math.abs(e.deltaY)){x-=e.deltaX;e.preventDefault()}},{passive:false});
  (function loop(now){var dt=Math.min(.05,(now-last)/1000);last=now;
    var tv=(red||drag)?0:(hover?0:-42);v+=(tv-v)*Math.min(1,dt*4);x+=v*dt;
    if(half){x=((x%half)-half)%half}
    q.style.transform="translate3d("+x.toFixed(2)+"px,0,0)";requestAnimationFrame(loop)})(last);
});
})();
/* метрики в кейсах: при наведении перебираются подписи */
(function(){
[].forEach.call(document.querySelectorAll(".case .nums>div"),function(c){var t=0;
  c.addEventListener("pointerenter",function(e){if(e.pointerType!=="mouse"||!window.__scr)return;var n=performance.now();if(n-t<700)return;t=n;
    [].forEach.call(c.querySelectorAll(".lbl"),function(l){window.__scr(l)})});
});
})();
/* увеличение скриншотов по клику */
(function(){
var figs=[].slice.call(document.querySelectorAll(".shots figure, .mq figure:not([aria-hidden])")).filter(function(f){return !f.closest(".ndaw")}); if(!figs.length) return;
var lb=document.createElement("div");lb.className="lb";lb.innerHTML='<img alt=""><div class="bar"><span class="lbl gray" id="lbc"></span><nav><button class="lbl" data-d="-1">Prev</button><button class="lbl" data-d="1">Next</button><button class="lbl" data-d="0">Close</button></nav></div>';
document.body.appendChild(lb);
var im=lb.querySelector("img"),cn=lb.querySelector("#lbc"),i=0;
function show(k){i=(k+figs.length)%figs.length;var f=figs[i],src=f.querySelector("img");
  var c=f.querySelector("figcaption");cn.textContent=(i+1)+" / "+figs.length+(c?"  "+c.textContent:"");
  im.src=src.src;lb.classList.add("on");document.documentElement.style.overflow="hidden"}
function hide(){lb.classList.remove("on");document.documentElement.style.overflow=""}
document.addEventListener("click",function(e){var f=e.target.closest&&e.target.closest(".shots figure, .mq figure");if(!f||f.closest(".ndaw")||lb.contains(f))return;
  var o=f;if(f.classList.contains("cl")){o=[].filter.call(f.parentNode.children,function(x){return !x.classList.contains("cl")&&x.dataset.k===f.dataset.k})[0]}
  var k=figs.indexOf(o);if(k>=0)show(k)});
lb.addEventListener("click",function(e){var d=e.target.dataset&&e.target.dataset.d;if(d==="1"||d==="-1"){e.stopPropagation();show(i+ +d)}else hide()});
document.addEventListener("keydown",function(e){if(!lb.classList.contains("on"))return;if(e.key==="Escape")hide();if(e.key==="ArrowRight")show(i+1);if(e.key==="ArrowLeft")show(i-1)});
})();
/* было / стало: тянем разделитель */
(function(){
[].forEach.call(document.querySelectorAll(".cmp .in"),function(el){
  var drag=false,dx=0,box=el.parentNode,kn=box.querySelector(".hd");
  function set(x){var r=el.getBoundingClientRect(),p=Math.max(0,Math.min(1,(x-r.left)/r.width));box.style.setProperty("--p",(p*100).toFixed(2)+"%")}
  function near(e){var r=el.getBoundingClientRect(),k=kn.getBoundingClientRect(),R=parseFloat(getComputedStyle(kn,"::after").width)/2+8;return Math.hypot(e.clientX-k.left,e.clientY-(r.top+r.height/2))<=Math.max(R,26)}
  el.addEventListener("pointerdown",function(e){if(!near(e))return;drag=true;dx=e.clientX-kn.getBoundingClientRect().left;el.setPointerCapture(e.pointerId);box.classList.add("drag");e.preventDefault()});
  el.addEventListener("pointermove",function(e){if(drag){set(e.clientX-dx);return}el.style.cursor=near(e)?"grab":""});
  function up(){drag=false;box.classList.remove("drag")}
  el.addEventListener("pointerup",up);el.addEventListener("pointercancel",up);
});
})();
/* mailto внутри встроенного окна открывает пустую страницу: там копируем адрес */
(function(){
if(window.top===window) return;
function copy(v,ok){function old(){var i=document.createElement("textarea");i.value=v;i.style.position="fixed";i.style.opacity="0";document.body.appendChild(i);i.select();try{document.execCommand("copy");ok()}catch(e){}i.remove()}
  if(navigator.clipboard&&navigator.clipboard.writeText) navigator.clipboard.writeText(v).then(ok,old); else old()}
[].forEach.call(document.querySelectorAll('a[href^="mailto:"]'),function(a){
  a.addEventListener("click",function(e){e.preventDefault();var v=a.getAttribute("href").replace(/^mailto:/,"");
    copy(v,function(){var row=a.closest(".gl"),b=row&&row.querySelector(".cpi");
      if(b){b.classList.add("ok");setTimeout(function(){b.classList.remove("ok")},1600)}
      else{a.classList.add("cp");setTimeout(function(){a.classList.remove("cp")},1400)}})})});
})();
/* копирование почты */
(function(){var b=document.querySelector(".cpi");if(!b)return;var t;
b.addEventListener("click",function(e){e.preventDefault();e.stopPropagation();var v=b.dataset.v;
  function ok(){b.classList.add("ok");clearTimeout(t);t=setTimeout(function(){b.classList.remove("ok")},1600)}
  function old(){var i=document.createElement("textarea");i.value=v;i.style.position="fixed";i.style.opacity="0";document.body.appendChild(i);i.select();try{document.execCommand("copy");ok()}catch(e){}i.remove()}
  if(navigator.clipboard&&navigator.clipboard.writeText) navigator.clipboard.writeText(v).then(ok,old); else old()});
})();
/* NDA: завеса затуманивается при появлении, блик идёт за курсором */
(function(){var n=document.getElementById("nda");if(!n)return;var v=n.querySelector(".veil");
if("IntersectionObserver" in window){var io=new IntersectionObserver(function(es){if(es[0].isIntersecting){setTimeout(function(){n.classList.add("in")},250);io.disconnect()}},{threshold:.35});io.observe(n)}else n.classList.add("in");
n.addEventListener("pointermove",function(e){var r=n.getBoundingClientRect();v.style.setProperty("--gx",((e.clientX-r.left)/r.width*100).toFixed(1)+"%");v.style.setProperty("--gy",((e.clientY-r.top)/r.height*100).toFixed(1)+"%")});
n.addEventListener("pointerleave",function(){v.style.setProperty("--gx","50%");v.style.setProperty("--gy","50%")});})();

/* ролики-превью: играет только один, тот что лучше всего виден; при переходе к нему стартует с начала */
(function(){var vs=[].slice.call(document.querySelectorAll(".vshot video"));if(!vs.length||!("IntersectionObserver" in window)||matchMedia("(prefers-reduced-motion: reduce)").matches)return;
var ratio=new Map(),cur=null;
function pick(){var best=null,br=.6;vs.forEach(function(v){var r=ratio.get(v)||0;if(r>br){br=r;best=v}});
 if(best===cur)return;
 if(cur)cur.pause();
 cur=best;
 if(cur){try{cur.currentTime=0}catch(e){}var p=cur.play();if(p&&p.catch)p.catch(function(){})}}
var io=new IntersectionObserver(function(es){es.forEach(function(e){ratio.set(e.target,e.intersectionRatio)});pick()},{threshold:[0,.2,.4,.6,.7,.8,.9,1]});
vs.forEach(function(v){io.observe(v)})})();
'''

_old = open(os.path.join(HERE, "content_src.py"), encoding="utf-8").read()

INK_JS = r'''
/* первый экран: под курсором текст рассыпается в песок */
(function(){
if(!matchMedia("(hover: hover) and (pointer: fine)").matches||matchMedia("(prefers-reduced-motion: reduce)").matches) return;
var w=document.querySelector(".inkw"); if(!w) return;
var h=w.querySelector("h1"),cv=document.createElement("canvas"),ctx=cv.getContext("2d");
cv.className="sand";cv.setAttribute("aria-hidden","true");w.appendChild(cv);
var PAD=40,dpr=Math.min(2,window.devicePixelRatio||1),W=0,H=0,N=0,ox,oy,px,py,rnd,ready=false;
var mx=-1e4,my=-1e4,r=0,tr=0,vx=0,vy=0,lx=0,ly=0,raf=0,t0=performance.now();
function build(){
  var b=w.getBoundingClientRect();W=b.width+PAD*2;H=b.height+PAD*2;
  cv.width=Math.round(W*dpr);cv.height=Math.round(H*dpr);
  var off=document.createElement("canvas");off.width=cv.width;off.height=cv.height;var o=off.getContext("2d");
  o.scale(dpr,dpr);o.fillStyle="#000";o.textBaseline="alphabetic";
  var walker=document.createTreeWalker(h,NodeFilter.SHOW_TEXT),n,rg=document.createRange();
  while((n=walker.nextNode())){
    var cs=getComputedStyle(n.parentNode),up=cs.textTransform==="uppercase";
    o.font=cs.fontStyle+" "+cs.fontWeight+" "+cs.fontSize+" "+cs.fontFamily;
    try{o.letterSpacing="0px"}catch(e){}
    var t=n.textContent;
    for(var i=0;i<t.length;i++){
      var ch=up?t[i].toUpperCase():t[i]; if(/\s/.test(ch)) continue;
      rg.setStart(n,i);rg.setEnd(n,i+1);var rr=rg.getClientRects()[0]; if(!rr||!rr.width) continue;
      var m=o.measureText(ch),asc=m.fontBoundingBoxAscent||parseFloat(cs.fontSize)*.8;
      o.fillText(ch,rr.left-b.left+PAD,rr.top-b.top+PAD+asc);
    }
  }
  var d=o.getImageData(0,0,off.width,off.height).data,step=Math.max(2,Math.round(2.6*dpr)),pts=[];
  for(var y=0;y<off.height;y+=step) for(var x=0;x<off.width;x+=step) if(d[(y*off.width+x)*4+3]>110) pts.push(x/dpr,y/dpr);
  N=pts.length/2;ox=new Float32Array(N);oy=new Float32Array(N);px=new Float32Array(N);py=new Float32Array(N);rnd=new Float32Array(N);
  for(var k=0;k<N;k++){ox[k]=px[k]=pts[k*2];oy[k]=py[k]=pts[k*2+1];rnd[k]=Math.random()}
  ready=true;
}
function mask(){
  var g="radial-gradient(circle "+r.toFixed(1)+"px at "+(mx-PAD).toFixed(1)+"px "+(my-PAD).toFixed(1)+"px, transparent 0, transparent 46%, #000 86%)";
  h.style.webkitMaskImage=g;h.style.maskImage=g;
}
function loop(now){
  r+=(tr-r)*.08;vx*=.9;vy*=.9;
  var k=(now-t0)/1000,busy=r>1;
  ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,W,H);ctx.fillStyle="#000";
  if(r>1) mask(); else {h.style.webkitMaskImage=h.style.maskImage=""}
  var R=Math.max(r,1),s=1.35;
  for(var i=0;i<N;i++){
    var dx=ox[i]-mx,dy=oy[i]-my,dd=dx*dx+dy*dy,tx=ox[i],ty=oy[i],a=0;
    if(dd<R*R*1.1){
      var d=Math.sqrt(dd),f=Math.max(0,1-d/R);
      a=Math.min(1,Math.max(0,(0.86-d/R)/0.4));
      var e=f*f,ang=rnd[i]*6.283+k*.6;
      tx=ox[i]+dx/(d||1)*e*26+Math.cos(ang)*e*9+vx*e*.6;
      ty=oy[i]+dy/(d||1)*e*18+Math.sin(ang)*e*9+e*e*22+vy*e*.4;
    }
    px[i]+=(tx-px[i])*.14;py[i]+=(ty-py[i])*.14;
    var mv=Math.abs(px[i]-ox[i])+Math.abs(py[i]-oy[i]);
    if(mv>.4) busy=true;
    if(a>0.02){ctx.globalAlpha=a;ctx.fillRect(px[i],py[i],s,s)}
    else if(mv>.6&&r>1){ctx.globalAlpha=Math.min(1,mv/14);ctx.fillRect(px[i],py[i],s,s)}
  }
  ctx.globalAlpha=1;
  raf=busy?requestAnimationFrame(loop):0;
}
function go(){ if(!raf) raf=requestAnimationFrame(loop) }
addEventListener("pointermove",function(e){
  if(!ready) return;
  var b=cv.getBoundingClientRect(),x=e.clientX-b.left,y=e.clientY-b.top;
  var inside=x>-40&&x<W+40&&y>-40&&y<H+40;
  vx+=(e.clientX-lx)*.5;vy+=(e.clientY-ly)*.5;lx=e.clientX;ly=e.clientY;
  mx=x;my=y;tr=inside?Math.max(110,Math.min(190,innerWidth*.11)):0;go();
},{passive:true});
document.addEventListener("pointerleave",function(){tr=0;go()});
var rt;addEventListener("resize",function(){clearTimeout(rt);rt=setTimeout(function(){ready=false;build()},200)});
(document.fonts&&document.fonts.ready?document.fonts.ready:Promise.resolve()).then(function(){requestAnimationFrame(build)});
})();
'''
WARP_JS = _old[_old.index("WARP_JS = r'''") + len("WARP_JS = r'''"):_old.index("'''", _old.index("WARP_JS = r'''") + 20)]

def home_gl():
    s = open(os.path.join(HERE, "home_gl.src.js"), encoding="utf-8").read()
    a = s.index("var ARROW="); b = s.index('}).join("");', a) + len('}).join("");')
    new = r"""var ARROW=%s;
function tile(p,cls,st){
  return '<article class="item '+cls+'"'+st+'>'+
    '<a class="asset" href="'+esc(p.href)+'" aria-label="'+esc(p.title)+'"><video src="'+esc(p.video)+'" poster="'+esc(p.video.replace(/\.mp4$/,'.jpg'))+'" muted loop playsinline preload="auto" autoplay></video></a>'+
    '<a class="txt" href="'+esc(p.href)+'">'+
      '<h3 class="ttl">'+esc(p.title)+ARROW+'</h3>'+
      '<div class="meta"><p class="lbl role">'+esc(p.role)+'</p><p class="lbl dt">'+esc(p.period)+'</p>'+(p.metric||[]).map(function(m){return '<p class="lbl mt">'+esc(m)+'</p>'}).join('')+'</div>'+
    '</a></article>';
}
if(window.PROJECTS&&document.getElementById("list")){
var bigP=PROJECTS.filter(function(p){return p.big}),smallP=PROJECTS.filter(function(p){return !p.big});
document.getElementById("list").innerHTML=bigP.map(function(p,i){return tile(p,'row '+(i%%2?'l':'r'),' style="--y:'+(440*i)+'"')}).join("");
document.getElementById("early").innerHTML=smallP.map(function(p){return tile(p,'','')}).join("");
}""" % json.dumps(ARROW)
    s = s[:a] + new + s[b:]
    def rep(x, y):
        nonlocal s
        assert x in s, x[:60]
        s = s.replace(x, y, 1)
    # наведение на одно видео: остальные ч/б и полупрозрачные
    rep('uniform vec2 uSize;uniform vec3 uTint;', 'uniform vec2 uSize;uniform vec3 uTint;uniform float uDim;')
    rep(' col*=uTint;\\n', ' col*=uTint;\\n col=mix(col,vec3(dot(col,vec3(.299,.587,.114))),uDim);\\n')
    rep(' float a=uOpacity*mask;', ' float a=uOpacity*mask*(1.-uDim*.62);')
    rep('el.addEventListener("pointerenter",function(){clearTimeout(hovT);it.li.classList.add("hov");tween(1,1.8)});', 'el.addEventListener("pointerenter",function(e){if(e.pointerType==="touch")return;clearTimeout(hovT);it.li.classList.add("hov");window.__hovIt=it;tween(1,1.8)});')
    rep('el.addEventListener("pointerleave",function(){clearTimeout(hovT);hovT=setTimeout(function(){it.li.classList.remove("hov")},60);tween(0,1.2)});', 'el.addEventListener("pointerleave",function(e){if(e.pointerType==="touch")return;clearTimeout(hovT);hovT=setTimeout(function(){it.li.classList.remove("hov");if(window.__hovIt===it)window.__hovIt=null},60);tween(0,1.2)});')
    rep('gl.uniform1f(U.uHover,it.hover);', 'it.dim=(it.dim||0)+((((window.__hovIt&&window.__hovIt!==it)||(!window.__hovIt&&window.__activeLi&&window.__activeLi!==it.li))?1:0)-(it.dim||0))*.1;gl.uniform1f(U.uDim,it.dim);gl.uniform1f(U.uHover,it.hover);')
    rep("var haveFluid=!!extCBF;", "var haveFluid=false;   // свечение под курсором убрано")
    rep("var BG=[1,1,1];", "var BG=%s;" % json.dumps(BG_RGB))
    # растяжение при прокрутке на десктопе втрое слабее прежнего
    rep("gl.uniform1f(U.uFisheye,CFG.FISHEYE*3);gl.uniform1f(U.uVelocity,sv);", "gl.uniform1f(U.uFisheye,CFG.FISHEYE*(touch?3:1));gl.uniform1f(U.uVelocity,touch?sv:sv*.2);")
    rep("/* телефон: canvas лежит в документе", "if(!touch){CFG.EDGE_ZONE=.14;CFG.LENS_STRENGTH=.05;CFG.CA_STRENGTH=.007;CFG.SMEAR_STRENGTH=.05;CFG.LIQUID_STRENGTH=.02}\n/* телефон: canvas лежит в документе")
    rep('hoverEls:[li.querySelector(".asset"),li.querySelector(".txt")]', 'hoverEls:[li.querySelector(".asset"),li.querySelector(".txt")].filter(Boolean)')
    rep("var hr=heroEl.getBoundingClientRect()", "var hr=heroEl?heroEl.getBoundingClientRect():{bottom:0}")
    return s

# десктоп: первый экран кончается ровно по верху строки роли первого кейса: видно название и отступ под ним
FOLD_JS = r"""(function(){var h=document.querySelector(".hero");if(!h)return;
function fit(){if(innerWidth<=700){h.style.minHeight="";return}var d=document.querySelector(".item .role");if(!d)return;
h.style.minHeight="";var cs=getComputedStyle(d),fs=parseFloat(cs.fontSize),lh=parseFloat(cs.lineHeight)||fs*1.2,
cap=d.getBoundingClientRect().top+scrollY+(lh-fs*.7)/2,base=h.getBoundingClientRect().height;
h.style.minHeight=Math.max(0,base+(innerHeight+3-cap))+"px"}
fit();addEventListener("resize",fit);if(document.fonts&&document.fonts.ready)document.fonts.ready.then(fit);addEventListener("load",fit)})();"""

# на страницах кейсов canvas нужен только для видео в шапке: когда оно ушло из вида, прячем canvas, чтобы он ничего не рисовал поверх контента
CASE_GL_HIDE = r"""(function(){var it=document.querySelector(".item"),cv=document.getElementById("gl");if(!it||!cv||!("IntersectionObserver" in window))return;
new IntersectionObserver(function(es){es.forEach(function(e){cv.style.visibility=e.isIntersecting?"":"hidden"})},{rootMargin:"200px 0px"}).observe(it)})();"""

# ------------------------------------------------------------------ каркас
def nav(cur):
    def a(h, t, k): return '<a href="%s"%s>%s</a>' % (h, ' class="on"' if k == cur else '', t)
    dd = "".join('<a href="%s"%s>%s<span>%s</span></a>' % (c["href"], ' class="on"' if cur == c["slug"] else '', ARROW, esc(c["title"])) for c in CASES)
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

SITE = "https://zvrtn.com/"
OG_DESC = {"home": "Product designer with 13 years in web & apps. AI features, code prototypes, measurable impact.",
           "about": "Product designer. Led design teams, mentored designers, built design systems and AI features.",
           "contact": "Email, LinkedIn and Telegram."}
def og(cur, title):
    c = next((x for x in CASES if x["slug"] == cur), None)
    img = "og/%s.jpg" % (cur if c else ("home" if cur == "home" else "home"))
    desc = ("%s. %s, %s." % (c["product"], c["role"], c["period"])) if c else OG_DESC.get(cur, OG_DESC["home"])
    page = "" if cur == "home" else (c["href"] if c else cur + ".html")
    return ('<meta name="description" content="%s">\n<meta property="og:type" content="website">\n<meta property="og:site_name" content="Yuri Zavorotny">\n'
            '<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n<meta property="og:url" content="%s%s">\n'
            '<meta property="og:image" content="%s%s">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
            '<meta name="twitter:card" content="summary_large_image">\n<meta name="theme-color" content="#ecebe8">') % (esc(desc), esc(title), esc(desc), SITE, page, SITE, img)

def shell(cur, title, main, scripts="", pre="", main_cls="page", body_cls=""):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="theme-color" content="#ecebe8">
{og(cur, title)}

{FONTS}
<style>{CSS}</style>
</head>
<body class="{body_cls}">
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
    return '  <div class="phead"><p class="lbl gray" data-scr>%s</p>%s</div>\n' % (left, right)

def nums(items, cls=""):
    return '<div class="nums %s">%s</div>' % (cls, "".join('<div><b>%s</b><p class="lbl">%s</p>%s</div>' % (n, esc(a).replace("&lt;br&gt;", "<br>").replace("&lt;mbr&gt;", '<br class="mbr"> '), ('<p class="lbl gray">%s</p>' % esc(c)) if c else "") for n, a, c in items))

def sec(label, inner, cls=""):
    return '  <section class="sec %s">\n    <p class="lbl" data-scr>%s</p>\n    <div>%s</div>\n  </section>\n' % (cls, label, inner)

def ps(*paras): return "".join("<p>%s</p>" % esc(p) for p in paras)

# ------------------------------------------------------------------ главная
LI = {"Richard Mabey": "https://www.linkedin.com/in/rmabey/", "Alex Fenin": "https://www.linkedin.com/in/alexander-fenin/", "Howard Davies": "https://www.linkedin.com/in/howard-d/",
      "Anton Solovev": "https://www.linkedin.com/in/anton-solovev-8349801a2/", "Max Nealon": "https://www.linkedin.com/in/maxnealon/", "Viktor Avdeev": "https://www.linkedin.com/in/v-avdeev/"}
RECS = [("Richard Mabey", "CEO at Juro, Oct 2023", "Yuri was instrumental in building our design function at Juro from the earliest days. What the world saw was clean UI that just worked."),
        ("Alex Fenin", "UX Researcher, Oct 2023", "His exceptional work of building the Editor experience in Juro doesn't simply meet expectations, it consistently overachieves them."),
        ("Howard Davies", "Staff Product Designer, Oct 2023", "He is a thoughtful and conscientious designer with a genuine, deep knowledge of best practises."),
        ("Anton Solovev", "Senior Product Manager, Oct 2025", "Yuri has a real talent for turning messy, high-friction flows into smooth, intuitive experiences that users actually trust."),
        ("Max Nealon", "Head of Product", "Yuri is everything you need in a product designer and a whole lot more. He is highly iterative, he seeks out feedback and actually listens and considers."),
        ("Viktor Avdeev", "Software Engineer, Nov 2023", "His approach to design is both innovative and user-centric, ensuring that every solution is not only aesthetically pleasing but also highly functional.")]
LI_RECS = "https://www.linkedin.com/in/zvrtn/details/recommendations/"

def home():
    recs = "".join('<figure><q class="rq">%s</q><figcaption><a class="rn" href="%s" target="_blank" rel="noopener">%s%s</a><p class="lbl gray rl">%s</p></figcaption></figure>\n      ' % (esc(q), LI[n], n, ARROW, re.sub(r",\s+[A-Z][a-z]{2} \d{4}$", "", r)) for n, r, q in RECS)
    main = f'''  <section class="hero">
    <div class="inkw"><h1 class="big"><span class="hdt"><b>Product designer</b> with 13 years <span class="nwd">in web&nbsp;&amp;&nbsp;apps.</span> <span class="nw"><b>AI&nbsp;features</b>,</span> code prototypes, measurable impact</span><span class="hmb"><b>Product designer</b> with 13 years in web&nbsp;&amp;&nbsp;apps, shipping <b>AI&nbsp;features</b> with measurable impact</span></h1></div>
  </section>
  <a class="hint" href="#list"><span class="lbl dn"><span data-scr>Scroll</span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M1 12H22"/><path d="M15 5l7 7-7 7"/></svg></span><span class="lbl" data-scr>2013 – 2026</span></a>
  <div id="list"></div>
  <section class="early">
    <div class="side"><p class="lbl" data-scr>Other work</p><p class="lbl gray"><span data-scr>Streaming, sports tech,</span><br><span data-scr>enterprise mobile</span></p></div>
    <div class="grid3" id="early"></div>
  </section>
  <section class="recs" id="recs">
    <div class="grid">
      {recs}</div>
    <a class="lbl more ul" href="{LI_RECS}" target="_blank" rel="noopener"><span data-scr>All recommendations on LinkedIn</span>{ICO_OUT}</a>
  </section>'''
    pj = [dict(slug=c["slug"], product=c["product"], title=c["title"], role=c["role"], period=c["period"], video=c["video"], href=c["href"], metric=c.get("metric"), big=bool(c.get("big"))) for c in CASES]
    scripts = "<script>var PROJECTS=%s;</script>\n<script>%s</script>\n<script>%s</script>\n<script>%s</script>\n" % (json.dumps(pj, ensure_ascii=False), home_gl(), WARP_JS, FOLD_JS)
    return shell("home", "Yuri Zavorotny · Product Designer", main, scripts, pre='<canvas id="gl" aria-hidden="true"></canvas>\n', main_cls="stage")

# ------------------------------------------------------------------ about
def about():
    by = {c["title"]: c["href"] for c in CASES}
    xp = [("Profi", "Senior Product Designer", "Mar 2026 – now")] + [(c["title"], c["role"], c["period"]) for c in CASES]
    def xrow(c, r, y, link=True):
        inner = '<span class="co">%s</span><span class="lbl">%s</span><span class="lbl gray yr">%s</span>' % (c, r, y)
        return '<li>%s</li>' % (('<a class="xr" href="%s">%s</a>' % (by[c], inner)) if (link and c in by) else '<div class="xr">%s</div>' % inner)
    edu = [("Master's degree in Art History", "Saint Petersburg State University", "2014 – 2016"),
           ("Economics", "Emperor Alexander I St. Petersburg State Transport University", "2007 – 2012")]
    main = phead("About") + f'''  <section class="sec first">
    <p class="lbl gray"></p>
    <div class="abt">
<figure class="ph" id="ph"><div class="fr"><img src="img/yuri.jpg" alt="Portrait of Yuri Zavorotny" onerror="this.closest('figure').remove()"></div></figure>
      <div class="tx">
        <p class="rq">I like taking messy, high-stakes flows and making them calm and predictable for the people who use them every day: admin platforms, editors, internal tools. I check what works with research, A/B tests and prototypes in code.</p>
        <p class="rq">I’ve led design teams and mentored designers, and I do my best work close to product and engineering, building things together rather than handing files over a wall. That’s the kind of team I’m looking for.</p>
        <div class="sig"><p class="nm2">Yuri Zavorotny</p><p class="lbl gray" data-scr>Product designer</p></div>
      </div>
    </div>
  </section>
''' + sec("In numbers", '<div class="nums four">%s</div>' % "".join('<div><b>%s</b><p class="lbl">%s</p><p class="lbl gray">%s</p></div>' % x for x in [
          ("+21%", "Client-to-contact<br>conversion", "Profi"), ("+25%", "Engagement with<br>admin workflows", "Sweed"),
          ("+29.5%", "Document import<br>into the editor", "Juro"), ("2.7x", "Feedback<br>processing speed", "Microsoft Azure")])) \
      + sec("Education", '<div class="edu">%s</div>' % "".join('<div><p class="deg">%s</p><p class="lbl">%s</p><p class="lbl gray">%s</p></div>' % x for x in [
          ("Art History", "Master's degree, Saint Petersburg<br>State University", "2014 – 2016"),
          ("Economics", "Emperor Alexander I St. Petersburg<br>State Transport University", "2007 – 2012")])) \
      + sec("Experience", '<ul class="xp">%s</ul>' % "".join(xrow(*x) for x in xp))
    return shell("about", "About · Yuri Zavorotny", main, body_cls="about")

# ------------------------------------------------------------------ contact
def contact():
    mail = "zavorotny.yuri@gmail.com"
    rows = [("Email", "mailto:" + mail, mail, "", '<button class="cpi" type="button" data-v="%s" aria-label="Copy email" title="Copy email">%s</button>' % (mail, ICO_COPY)),
            ("LinkedIn", "https://www.linkedin.com/in/zvrtn", "linkedin.com/in/zvrtn", ' target="_blank" rel="noopener"', ""),
            ("Telegram", "https://t.me/zavorotny_yuri", "@zavorotny_yuri", ' target="_blank" rel="noopener"', "")]
    main = phead("Contact") + '  <div class="rows">\n' + "".join(
        '    <div class="gl"><a class="g" href="%s"%s>%s%s</a><span class="side lbl">%s%s</span></div>\n' % (h, t, n, ARROW, ('<a href="%s"%s>%s</a>' % (h, t, v)), x) for n, h, v, t, x in rows) + '  </div>\n'
    return shell("contact", "Contact · Yuri Zavorotny", main, main_cls="page one")

# ------------------------------------------------------------------ кейсы: кирпичики
_n = [0]
PULLS = {}
def body(*parts, cls=""): return '<div class="body %s">%s</div>' % (cls, "".join(parts))
def ul(*items): return "<ul>%s</ul>" % "".join("<li>%s</li>" % esc(i) for i in items)
def h3(t): return '<p class="h3">%s</p>' % esc(t)
def qgroup(title, qs):
    q, w = qs[0]
    return '<div class="qc"><p class="h3">%s</p><p class="js">%s</p><cite class="lbl gray">%s</cite></div>' % (esc(re.sub(r"^\d+\. ", "", title)), esc(q), esc(w))
_pc = [0]
def jobs(name, stories):
    _pc[0] += 1
    def fmt(s):
        return re.sub(r"^(When [^,]+,)", r"<b>\1</b>", esc(s))
    return '<div class="qc"><p class="lbl gray">Persona %d</p><p class="h3">%s</p>%s</div>' % (_pc[0], esc(name), "".join('<p class="js">%s</p>' % fmt(s) for s in stories[:2][::-1]))
def shots(slug, idx, cls="", cap=None, caps=None):
    idx = list(idx)
    f = "".join('<figure><img src="big/%s-%02d.jpg" alt="" decoding="async"></figure>' % (slug, i) for i in idx)
    return '<div class="shots %s">%s</div>%s' % (cls, f, ('<p class="lbl gray cap">%s</p>' % esc(cap)) if cap else "")
def compare(a, b, la="Before", lb="After"):
    return ('<div class="cmp"><div class="in"><img src="big/%s.jpg" alt="%s"><img class="b" src="big/%s.jpg" alt="%s">'
            '<span class="hd"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 6l-6 6 6 6M15 6l6 6-6 6"/></svg></span>'
            '<span class="lbl tg l">%s</span><span class="lbl tg r">%s</span></div></div><p class="lbl gray cap">Drag to compare the old and the new editor</p>') % (a, la, b, lb, la, lb)
def marquee(slug, idx, h, hm):
    one = "".join('<figure><img src="big/%s-%02d.jpg" alt=""></figure>' % (slug, i) for i in idx)
    return '  <div class="mqw" style="--h:%s;--hm:%s"><div class="mq">%s</div></div>\n' % (h, hm, one)
def nda():
    return ('  <section class="nda"><div class="glow" aria-hidden="true"></div><h2>Protected by NDA</h2>'
            '<p class="lbl">Research, process and internal data stay private.<br>Happy to walk through them in a call.</p></section>\n')
def company(inner): return '  <section class="cintro">\n    <div><p class="lbl gray">Company</p>%s</div>\n' % inner.replace('class="body ', 'class="body soft ', 1)
def role(inner, label="Role"): return '    <div><p class="lbl gray">%s</p>%s</div>\n  </section>\n' % (label, inner)
def results(inner): return '  <section class="panel">\n    <p class="lbl gray">Results</p>\n    %s\n  </section>\n' % inner
def study(inner, label="Case study"):
    return '  <section class="study">\n    <p class="lbl gray">%s</p>' % label + '\n    %s\n  </section>\n' % inner.replace('<p class="state">', '<h2>', 1).replace('</p><div class="body', '</h2><div class="body', 1)
def chapter(label, inner, cls=None):
    _n[0] += 1
    pull = PULLS.get(label)
    return ('  <section class="chap">\n    <div class="ct"><p class="lbl gray">%02d</p><h3>%s</h3></div>\n    <div>%s%s</div>\n  </section>\n'
            % (_n[0], esc(label), ('<p class="pull">%s</p>' % esc(pull)) if pull else "", inner))

# тексты Juro и Sweed берём из прежней версии сборки и раскладываем по новым блокам
_src = _old[_old.index("def content(slug):"):_old.index("def case(i):")]
_src = _src.replace('sec("Company", ', 'company(').replace('sec("Role", ', 'role(').replace('sec("Results", ', 'results(').replace('sec("Case study", ', 'study(')
_src = re.sub(r'sec\("[IVX]+\. ([^"]+)", ', r'chapter("\1", ', _src)
_src = _src.replace('shots("juro", [13, 14], cap="New and old versions of the editor")', 'compare("juro-13w", "juro-14w", "Old editor", "New editor")')
_src = _src.replace("def content(slug):", "def content_old(slug):")
exec(_src)

PULLS.update({
  "Problem statement": "The old editor forced users to seek additional tools for contract-related tasks.",
  "Dashboard / Reports / Money / Inventory": "Rather than designing one-off pages, I worked at the system level.",
  "Customers": "This module needed clarity, predictability and robustness more than visual novelty.",
  "E-commerce / Marketing": "A small UX ambiguity can translate into lost revenue or misaligned offers on the storefront.",
  "Store Setup": "A single wrong setting can change pricing, eligibility or fulfillment.",
  "Settings": "The goal was to make platform-wide decisions safer, not just easier to click through.",
})


AB_AI = (
  study('<p class="state">A/B testing with Sweed AI, built into Workflows</p>' +
        body(ps("Workflows is the canvas where dispensary marketers build automated campaigns: an audience, a delay, an email, a condition. I designed the A/B testing layer for it and the Sweed AI tools that live inside that layer.",
                "Sweed AI is the AI layer of the whole platform: product recommendations at the register, dynamic customer segments, on-screen help for budtenders, and in marketing it drafts banners, emails and survey insights. In Workflows I designed how Sweed AI works inside an A/B test.",
                "The idea is simple. AI is good at producing options and has no way of knowing which one will sell. So Sweed AI drafts, tunes and checks the variants, and the test decides.")), "Case study") +
  chapter("One email and a guess", body(ps("A step in Workflows could send only one version of an email. Marketers had no way to compare subject lines or content, so campaign performance was unpredictable and hard to improve."),
      ul("Built in: testing had to live inside the flow builder, with no redirects and no external tools",
         "Flexible: marketers needed control over test size, the winning metric and how the winner is chosen",
         "Light: setup and monitoring had to feel native and usable by any team, not only by analysts"))) +
  chapter("A test is a property of the step", body(ps("Instead of a separate tool, A/B testing became a checkbox on the email step. Turning it on opens the settings right in the side panel: the share of the segment that gets the test, the winning metric such as order placed rate, the test duration, and what the rest of the audience receives.",
      "Variants sit in a table below the settings, and the canvas marks the step as a test, so it reads at a glance even in a long flow."))) +
  chapter("What changed", body(ps("Curaleaf, one of the largest cannabis retailers in the US, ran its email campaigns with A/B testing in November and December 2024.",
      "Order-placed rate went from 9% to 26%, open rate from about 18% to 21.5%, and median revenue per user from $140 to $167. Click-through rate grew by 12%."))) +
  chapter("Sweed AI drafts, the test decides", body(ps("Sweed AI sits inside the test, not in front of it. Every suggestion is labeled and reversible, and nothing goes out until the marketer starts the test."),
      ul("Tunes the setup: suggests test share, metric and duration from the segment size and the campaign goal, and says why",
         "Drafts variants: the marketer describes the goal, AI writes subject lines and content from the store catalog, active promos and each customer's past purchases",
         "Checks compliance: every draft is checked against cannabis advertising rules before it can join the test, with a one-click rewrite",
         "Explains the result: after the test, AI says why the winner won and what to test next")) +
      '<div class="vshot"><video src="v/sweed-ai.mp4" poster="v/sweed-ai.jpg" muted loop playsinline preload="metadata" disablepictureinpicture aria-label="Walkthrough: generating variants with Sweed AI, starting the test and reading the result" style="aspect-ratio:2000/1248"></video></div>'
      '<p class="lbl gray cap">Numbers in the prototype are illustrative</p>')
)

def content(slug):
    _n[0] = 0; _pc[0] = 0
    if slug == "juro":
        s = content_old("juro").replace('<div style="margin-top:2em">', '<div class="cards">')
        s = s.replace("Alex Green, Head Counsel, Alpha Inc. Legal", "Jane Doe, Head Counsel").replace("Sarah Smith, Sales Manager / HR Manager, Compass Industries", "John Doe, Sales Manager / HR Manager")
        a = "<h3>JTBD</h3>"; assert a in s; s = s.replace(a, "<h3>JTBD + Personas</h3>")
        a = "keep the design process user-centric and outcome-driven.</p>"; assert a in s
        s = s.replace(a, a + "<p>We paired JTBD with personas, which is an unorthodox combination: JTBD usually sets the persona aside and looks only at the job. Here every set of job stories belongs to a specific person, a head of legal or a sales and HR manager. Personas kept the context of the role, job stories kept the design focused on the outcome. The names below are placeholders, not real people.</p>")
        a = "And finally, the design solution for the new editor. Its testing, refinement, and the metrics verification can be discussed in more detail during a personal interview.</p>"; assert a in s
        s = s.replace(a, "The new editor grew directly out of the five feedback groups. Formatting works the way people know from Word, the header became compact and gives the page back to the text, and the actions people use on every contract, such as comments, signing, versions and export, moved out of nested menus onto the surface.</p>"
                         "<p>I worked closely with engineers on editor behaviour and rendering constraints, so the design held up on real, long contracts and not only in mockups. Testing, refinement and metrics verification I am happy to walk through in a call.</p>")
        g = shots("juro", range(1, 13), "c3"); assert g in s
        return s.replace(g, "") + marquee("juro", range(1, 13), "min(24vh,calc(150*var(--u)))", "19vh")
    if slug == "sweed":
        old = nums([("−15%", "Support load", "Redesign of core operational workflows"), ("+25%", "Engagement with new admin workflows", "")])
        s = content_old("sweed").replace('<p class="lbl gray cap">Not every subsection is shown, only the representative ones</p>', "")
        assert old in s
        SHORT = {
 "These are the core operational": ["These are the core operational modules of the portal that store managers and back-office teams use every day. Dashboard shows at a glance how the store and its campaigns are performing. Reports is where analysts build and save their own views, such as gross sales by day. Money controls cash: shifts, cash drawers and the gap between expected and actual amounts. Inventory covers purchases, counts and transfers between locations.",
   "When I joined, these areas were already live and growing fast across several product streams. I refined and extended the existing UX and kept the modules consistent as new features arrived. Much of it came down to data hierarchy and edge cases: a report builder with metrics, intervals, filters and grouping side by side, a Shifts list where every difference between expected and actual cash is visible at a glance, and Purchases and Transfers with statuses that are easy to scan.",
   "Rather than designing one-off pages, I worked at the system level, so each change fit a cohesive logic shared across the portal."],
 "The Customers module": ["The Customers module is the foundation of the portal’s buyer management and patient verification. Dispensary staff start from the customer queue and open a profile with tabs for Info, Documents, Forms, Purchase history and Logs, to validate identities, maintain medical records, connect caregivers to patients and run compliance checks before a sale.",
   "I extended and matured the existing UX: flows for validation, documents and medical eligibility, clearer states and edge cases, simpler navigation for high-frequency tasks. Because the module affects checkout and compliance risk, it needed clarity and robustness more than visual novelty.",
   "A large part of the work was shaping the system rules behind customer states: when eligibility changes, which validations block, how caregiver relationships cascade. I defined edge scenarios with product and engineering to prevent loopholes that could lead to regulatory violations or checkout failure."],
 "E-commerce in the portal": ["E-commerce runs the online storefront operation: Active orders as a board and as a table, order packing with barcode verification, Dispatch on a map with drivers and alerts, and delivery shifts. Marketing sits right next to it with Events, Discounts, Segments and User Workflows: campaigns, promotions and loyalty mechanics. Together they are the growth layer of the platform.",
   "I refined the configuration flows, aligned delivery and assignment logic with store-level settings and improved tools for non-technical staff, and made marketing and e-commerce feel like one system. A big part of the work was reducing hidden states and clarifying cause and effect. Order packing, for example, shows which items are verified and which are missing before the final Verified or Not verified decision, so staff never have to guess whether an order is ready.",
   "A small UX ambiguity here can mean lost revenue or misaligned offers, so I unified the logic behind these controls and exposed key dependencies, making configuration predictable rather than accidental."],
 "Store Setup is the configuration": ["Store Setup is the configuration layer of the portal: Products, Prices, Attributes, Categories, Brands, Distributors, Locations, Employees, Hardware and more. It defines what the business looks like operationally before any sales happen.",
   "I evolved the UX for these foundational settings: navigation hierarchy, dependencies between settings, easier configuration without breaking store logic. A single wrong setting can change pricing, eligibility or fulfillment, so the UX had to reinforce safety and clarity. Category settings, for instance, decide which product fields are enabled (quality line, strain, scents, flavorings, potency), so they are grouped and labeled to be read before they are changed.",
   "Much of the work was modeling the logic behind settings: what is global vs store-level, how controls are grouped, what stays in advanced menus. I reduced cognitive load while keeping full configurability for power users through defaults and progressive disclosure."],
 "Settings is the infrastructure": ["Settings is the infrastructure layer of the portal: E-commerce rules such as auto-approving orders and how long pickup, curbside and drive-through orders are held, Integrations like SendGrid, the store Schedule and Store behavior around promos, prices and refunds, plus Delivery, Notifications, Payment Methods, Company Profile and Billing. I supported its growing complexity while keeping a clean, predictable UX model.",
   "I untangled technical concepts into understandable controls, grouped scattered toggles and made sensitive changes traceable and safe to edit. I set clear boundaries between organization-level and store-level logic, rethinking how inheritance, overrides and defaults are shown, so changes have a predictable scope.",
   "Design changes here have long-term architectural consequences, so the work required systems thinking: configuration that is auditable, reversible when possible and resistant to misconfiguration. The goal was to make platform-wide decisions safer, not just easier to click through."],
        }
        def three(m):
            ps = re.findall(r"<p>(.*?)</p>", m.group(1), re.S)
            for k,v in SHORT.items():
                if ps and ps[0].startswith(k): return '<div class="body ">' + "".join("<p>%s</p>" % x for x in v) + "</div>"
            while len(ps) > 3:
                k = min(range(len(ps) - 1), key=lambda j: len(ps[j]) + len(ps[j + 1]))
                ps[k:k + 2] = [ps[k] + " " + ps[k + 1]]
            return '<div class="body ">' + "".join("<p>%s</p>" % x for x in ps) + "</div>"
        s = re.sub(r'<div class="body ">((?:<p>(?:(?!</?div).)*?</p>)+)</div>', three, s, flags=re.S)
        def vid(n, label):
            return ('<div class="vshot"><video src="v/sweed-%s.mp4" poster="v/sweed-%s.jpg" muted loop playsinline preload="metadata" disablepictureinpicture aria-label="%s"></video></div>' % (n, n, label))
        for (a0, b0), n, lab in [((1, 7), "operations", "Walkthrough: Dashboard, Reports, Money and Inventory"), ((7, 13), "customers", "Walkthrough: Customers"),
                                  ((13, 19), "ecommerce", "Walkthrough: E-commerce and Marketing"), ((19, 25), "store-setup", "Walkthrough: Store Setup"), ((25, 31), "settings", "Walkthrough: Settings")]:
            g = shots("sweed", range(a0, b0)); assert g in s, n
            s = s.replace(g, vid(n, lab))
        chs = re.findall(r'  <section class="chap">.*?</section>\n', s, flags=re.S)
        assert len(chs) == 5 and "Dashboard / Reports" in chs[0], len(chs)
        start = s.index(chs[0]); end = s.index(chs[4]) + len(chs[4])
        new = [chs[2], chs[1], chs[3], chs[4], chs[0]]
        new = [re.sub(r'<p class="lbl gray">\d\d</p>', '<p class="lbl gray">%02d</p>' % (i + 1), c, count=1) for i, c in enumerate(new)]
        s = s[:start] + "".join(new) + s[end:]
        s = s.replace(old, nums([("2.8x", "Order-placed rate", ""), ("+$27", "Revenue per user", ""),
                  ("−15%", "Support load", ""), ("+25%", "Admin engagement", "")], "four"))
        # роль: акцент на A/B и Sweed AI
        a = "<p>I drove the redesign of core operational workflows"; assert a in s
        s = s.replace(a, "<p>My main focus was marketing automation: I designed A/B testing for Workflows, the campaign builder, and the Sweed AI tools inside it.</p>" + a, 1)
        # старый обзор платформы уходит в конец, перед ним новая история про A/B и AI
        st = s.index('  <section class="study">')
        s = s[:st] + AB_AI + s[st:].replace('<p class="lbl gray">Case study</p>', '<p class="lbl gray">Across the platform</p>', 1)
        n = [0]
        def ren(m):
            n[0] += 1; return '<p class="lbl gray">%02d</p>' % n[0]
        s = re.sub(r'(?<=<div class="ct">)<p class="lbl gray">\d\d</p>', ren, s)
        return s + study('<p class="state">Launched after I left</p>' + body(ps(
            "In August 2026, after I finished my work at Sweed, the A/B testing with Sweed AI went into open testing with customers, as part of Sweed's AI marketing launch.")) +
            ('<a class="lbl ul lk" href="https://finance.yahoo.com/technology/ai/articles/sweed-launches-ai-powered-smart-120000915.html" target="_blank" rel="noopener">Launch coverage on Yahoo Finance%s</a>' % ICO_OUT), "Launch")
    if slug == "microsoft-azure":
        nda = ('<div class="vshot"><video src="v/azure-feedback.mp4" poster="v/azure-feedback.jpg" muted loop playsinline preload="metadata" disablepictureinpicture '
               'aria-label="Walkthrough: filtering feedback, opening an item, print view and creating a feature" style="aspect-ratio:2000/1248"></video></div>')
        return (
          company(body(ps("Microsoft Azure is one of the world’s largest cloud platforms, used across enterprises and engineering teams globally. At this scale, even internal tools must meet strict reliability, governance and security standards, because small UX decisions impact thousands of users and downstream workflows."))) +
          role(body(ps("I worked with the Azure team on designing an internal feedback processing system used by product and engineering teams to collect, normalize and act on user insights at scale.",
                       "My role covered discovery, UX architecture, interaction design and collaboration with engineering to ensure the system integrated cleanly into Azure’s internal workflows."))) +
          results(nums([("2.7x", "Feedback processing<mbr>speed", ""), ("+170%", "Requests analyzed<mbr>per day", ""), ("~200", "Feedback items<mbr>a day", "")], "three")) +
          study('<p class="state">Turning feedback from a passive inbox into an actionable product signal</p>' +
                body(ps("The goal was to turn fragmented input from multiple sources into structured, decision-ready data, helping teams prioritize improvements and close the loop with users more effectively.",
                        "The tool later became the foundation for Microsoft’s whole feedback center: the same model of feedback items, statuses and linked features is live today across the public Feedback Portal."))) +
          chapter("Designed inside Fluent", body(ps("At Microsoft, I worked with their Fluent design system. The feedback base is built on it and follows its standards and documentation, which meant designing inside an existing corporate system rather than inventing a new visual language.")) +
              ('<a class="lbl ul lk" href="https://fluent2.microsoft.design/" target="_blank" rel="noopener">Fluent 2 design system%s</a>' % ICO_OUT)) +
          chapter("Less manual triage", body(ps("Most of the people working with feedback were engineers who sorted it by hand on top of their main work. Every item that arrived without a clear area, owner or status meant another round of questions before anyone could act on it.",
              "So the interface was built around fast triage: the fields that decide where an item goes are filled in up front, and the list shows at a glance what is new, what is waiting for an owner and what is already linked to a feature. Less time spent sorting means more time left for actually fixing things."))) +
          chapter("One model, from a single request to a feature", body(ps("I translated complex requirements from multiple stakeholder groups into a unified model of how feedback moves through the system."),
              ul("Captured: input from different sources lands in one list with a shared structure",
                 "Routed: every item has a product area and a domain owner",
                 "Enriched: status, type, priority and days in process are visible at a glance",
                 "Resolved: feedback is linked to features, so teams can close the loop with users"),
              ps("A feedback item is more than a message. Its page keeps the context, the discussion and the features it relates to, and a new feature can be created straight from it.")) + nda))
    if slug == "real-time-tech":
        return (
          company(body(ps("Real Time Technologies was developing a live-streaming platform Webka that combined Twitch-style interactivity with the structured format of MasterClass, built for teaching and professional sessions rather than entertainment. The product launched on desktop and mobile."))) +
          role(body(ps("I led the design of the platform’s core experience. My role covered both product definition and UX: translating live teaching workflows into a scalable interaction model, designing controls that work in real time, and ensuring low-friction engagement for different audience types."))) +
          study('<p class="state">A live platform where the interface has to work in real time</p>' +
                body(ps("The core experience covered five areas: streaming interfaces, viewer interaction models, discovery and session tools, onboarding for creators, and internal studio tools.",
                        "I conducted research with streamers and early adopters, validated participation mechanics, and helped evolve the interface through several iterations as new use cases emerged.",
                        "In parallel, I managed the design direction for the wider product team: aligning interaction patterns across desktop and mobile, mentoring designers, and working closely with engineering to ensure performance and usability in live conditions."))) +
          marquee("webka", range(1, 7), "min(32vh,calc(200*var(--u)))", "25vh"))
    if slug == "it-test":
        return (
          company(body(ps("IT Test is a mobile and software development studio. I joined as the sole UX/UI designer and later built and led the internal design team. The key product I worked on was Freezio, a 3D training and visualization app for figure skaters, used by athletes and coaches worldwide."))) +
          role(body(ps("My role covered the full product cycle: user research, translating domain-specific training workflows into interface logic, prototyping interaction models, creating UI, and supporting engineering during implementation.",
              "As the product grew, I was also shaping the long-term product direction: how onboarding should work for both athletes and coaches, what level of visual abstraction makes complex movements understandable on mobile, and how to balance consumer accessibility with professional detail.",
              "Over time, I formalized design practices inside the company, mentored new designers, and aligned multiple products around a consistent UX approach."))) +
          study('<p class="state">Making a jump readable on a phone screen</p>' +
                body(ps("Freezio shows figure skating elements as animated 3D models. You can rotate a model around its axes, zoom in and look at a jump from any angle. Freezio.Move adds video analysis on top: slow motion, side-by-side comparison of runs, measuring tools and markup over the frame.",
                        "I designed the interfaces for working with the 3D scene and the video: controls that stay out of the way of the model, gestures that feel natural on a small screen, and a balance between the detail a coach needs and what a beginner can take in. The app shipped on iOS and Android."))) +
          marquee("freezio", range(1, 6), "min(32vh,calc(210*var(--u)))", "27vh"))
    if slug == "inter-rao":
        return (
          company(body(ps("Inter RAO is one of the largest state-linked energy holdings in Eastern Europe and the CIS, operating across generation, trading and energy distribution. The company manages a wide network of subsidiaries, which makes internal coordination highly regulated and legally sensitive."))) +
          role(body(ps("My official title was Interface Designer, but in practice I was responsible for the full product design cycle: from research and prototyping to UI and implementation support.",
              "I designed a mobile document management system that allowed employees to review, approve and sign internal documents remotely."))) +
          study('<p class="state">Signing documents without being tied to a desk</p>' +
                body(ps("Before this project, approvals were tied to desktop access. Managers who traveled between branches held up the whole chain until they were back at their computer.",
                        "The app brought the queue of documents, their full text and the approve and sign actions into one simple flow on a phone. The documents were legally sensitive, so every step had to make clear what exactly is being signed and what status the document is in.",
                        "The product is still in use inside the company today, with only minor updates."))) +
          marquee("interrao", range(1, 11), "min(48vh,calc(315*var(--u)))", "40vh"))
    raise KeyError(slug)

def case(i):
    c = CASES[i]; nx = CASES[(i + 1) % len(CASES)]; pv = CASES[(i - 1) % len(CASES)]
    links = []
    if c.get("link"): links.append('<a class="lbl ul" href="%s" target="_blank" rel="noopener">%s%s</a>' % (c["link"][1], c["link"][0], ICO_OUT))
    for n, u in c.get("stores", []): links.append('<a class="lbl ul" href="%s" target="_blank" rel="noopener">%s%s</a>' % (u, n, ICO_OUT))
    main = phead("%s · %s" % (esc(c["title"]), esc(c["product"]))) + f'''  <header class="chead">
    <div>
      <h1>{esc(c["title"])}</h1>
      {('<div class="links">%s</div>' % "".join(links)) if links else ""}
      <p class="lbl rp">{esc(c["role"])}<br><span class="gray">{esc(c["period"])}</span></p>
    </div>
    <article class="item"><div class="asset"><video src="{c["video"]}" poster="{c["video"][:-4]}.jpg" muted loop playsinline autoplay preload="auto"></video></div></article>
  </header>
''' + content(c["slug"]) + f'''  <nav class="pn">
    <a class="pv" href="{pv["href"]}"><span class="lbl gray">Previous</span><span class="n">{ARROW}{esc(pv["title"])}</span></a>
    <a class="nx" href="{nx["href"]}"><span class="lbl gray">Next</span><span class="n">{esc(nx["title"])}{ARROW}</span></a>
  </nav>
'''
    return shell(c["slug"], "%s · Yuri Zavorotny" % c["title"], main, "<script>%s</script>\n<script>%s</script>\n" % (home_gl(), CASE_GL_HIDE), pre='<canvas id="gl" aria-hidden="true"></canvas>\n', body_cls="case")

os.makedirs(out, exist_ok=True)
def w(name, s):
    assert "—" not in re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S), name
    open(os.path.join(out, name), "w", encoding="utf-8").write(s)
w("index.html", home()); w("about.html", about()); w("contact.html", contact())
for i, c in enumerate(CASES): w(c["href"], case(i))
print("ok", out)
