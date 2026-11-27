# Картинки превью ссылок (og/home.jpg, og/profi.jpg), 1200x630.
# npm i @fontsource/instrument-serif @fontsource/inter-tight @fontsource/ibm-plex-mono
# python3 og.py <путь к node_modules>      (запускать из _src)
import sys, pathlib, base64
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
NM = pathlib.Path(sys.argv[1]).resolve() / "@fontsource"

def b64(p): return base64.b64encode(p.read_bytes()).decode()
def face(fam, pkg, w):
    return "@font-face{font-family:'%s';font-weight:%d;src:url(data:font/woff2;base64,%s)}" % (
        fam, w, b64(NM / pkg / "files" / ("%s-latin-%d-normal.woff2" % (pkg, w))))

CSS = (face("S", "instrument-serif", 400) + face("G", "inter-tight", 700) + face("M", "ibm-plex-mono", 500) +
 "body{margin:0;width:1200px;height:630px;background:#ecebe8;color:#000;position:relative;overflow:hidden}"
 "div,h1,img{position:absolute;margin:0}"
 ".l{font:500 18px/1 M;letter-spacing:.04em;text-transform:uppercase;top:57px;left:64px}"
 ".r{left:auto;right:64px;color:#86857f}"
 "h1{font:400 76.5px/.93 S;text-transform:uppercase;letter-spacing:-.005em}"
 "b{font-family:G;font-weight:700;font-size:.93em;letter-spacing:-.022em}"
 ".home{left:64px;bottom:96px;white-space:nowrap}"
 ".case{left:64px;bottom:150px;font-size:92px}"
 ".s{top:541px;bottom:auto}"
 "img{left:576px;top:130px;width:560px;height:350px;object-fit:cover}")

def page(tag, body):
    return "<meta charset=utf-8><style>%s</style><div class=l>Yuri Zavorotny</div><div class='l r'>%s</div>%s" % (CSS, tag, body)

PAGES = {
 "home": page("Portfolio", "<h1 class=home><b>Product designer</b> with 13 years<br>in web &amp; apps. <b>AI features</b>, code<br>prototypes, measurable impact</h1>"),
 "profi": page("Case study", "<img src='data:image/jpeg;base64,%s'><h1 class=case>Profi</h1><div class='l s'>AI tutor matching, service marketplace</div>" % b64(ROOT / "v/profi.jpg")),
}

with sync_playwright() as p:
    br = p.chromium.launch(channel="chrome")
    pg = br.new_page(viewport={"width": 1200, "height": 630})
    for name, html in PAGES.items():
        pg.set_content(html); pg.evaluate("document.fonts.ready")
        pg.screenshot(path=str(ROOT / "og" / (name + ".jpg")), type="jpeg", quality=92)
    br.close()
