"""Баннеры для Google Ads: изображения без текста (поиск, PMax), логотипы, баннеры с текстом (КМС/PMax). → google-ads/banners/"""
import base64, pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent; A = ROOT / "assets"
OUT = ROOT / "google-ads" / "banners"; OUT.mkdir(parents=True, exist_ok=True)
b64 = lambda p: base64.b64encode(p.read_bytes()).decode()
F = "".join(f'@font-face{{font-family:{n};src:url(data:font/woff2;base64,{b64(ROOT/"src"/"fonts"/f)})}}' for n, f in [
    ("H", "manrope-cyrillic-800-normal.woff2"), ("HL", "manrope-latin-800-normal.woff2"),
    ("B", "manrope-cyrillic-700-normal.woff2"), ("BL", "manrope-latin-700-normal.woff2"), ("Manrope", "manrope-latin-700-normal.woff2")])

DEF = '''<defs>
<linearGradient id="st" x1="0" x2="1"><stop offset="0" stop-color="#e9edf3"/><stop offset=".45" stop-color="#ffffff"/><stop offset="1" stop-color="#d9dfe8"/></linearGradient>
<linearGradient id="st2" x1="0" x2="1"><stop offset="0" stop-color="#dfe5ee"/><stop offset=".5" stop-color="#f7f9fc"/><stop offset="1" stop-color="#cfd7e3"/></linearGradient>
<linearGradient id="hd" x1="0" x2="1"><stop offset="0" stop-color="#9aa6b8"/><stop offset=".5" stop-color="#e8edf4"/><stop offset="1" stop-color="#8793a6"/></linearGradient>
<radialGradient id="gl" cx=".38" cy=".35" r=".75"><stop offset="0" stop-color="#bfe0ff"/><stop offset=".55" stop-color="#5b8fd9"/><stop offset="1" stop-color="#1d3f7a"/></radialGradient>
<linearGradient id="bl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a5cf0"/><stop offset="1" stop-color="#1238b0"/></linearGradient>
<filter id="sh" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="18" stdDeviation="18" flood-color="#0d1b33" flood-opacity=".22"/></filter>
</defs>'''

FRIDGE = '''<g filter="url(#sh)"><rect x="0" y="0" width="300" height="540" rx="22" fill="url(#st)" stroke="#b9c3d2" stroke-width="2"/>
<rect x="0" y="178" width="300" height="5" fill="#b9c3d2"/>
<rect x="28" y="40" width="12" height="104" rx="6" fill="url(#hd)"/><rect x="28" y="214" width="12" height="150" rx="6" fill="url(#hd)"/>
<rect x="196" y="40" width="76" height="40" rx="8" fill="#0d1b33"/><text x="234" y="68" text-anchor="middle" font-family="BL" font-size="22" fill="#5fd0ff">-18°</text>
<rect x="196" y="88" width="76" height="6" rx="3" fill="#cfd7e3"/><path d="M230 16 L238 16" stroke="#b9c3d2" stroke-width="3" stroke-linecap="round"/>
<rect x="60" y="20" width="16" height="500" fill="#fff" opacity=".55"/>
<rect x="20" y="540" width="40" height="14" rx="4" fill="#5b6678"/><rect x="240" y="540" width="40" height="14" rx="4" fill="#5b6678"/></g>'''
WASHER = '''<g filter="url(#sh)"><rect x="0" y="0" width="320" height="360" rx="22" fill="url(#st)" stroke="#b9c3d2" stroke-width="2"/>
<rect x="0" y="0" width="320" height="70" rx="22" fill="url(#st2)"/><rect x="0" y="66" width="320" height="4" fill="#b9c3d2"/>
<rect x="22" y="20" width="70" height="30" rx="6" fill="#dfe5ee" stroke="#b9c3d2"/><rect x="132" y="18" width="88" height="34" rx="7" fill="#0d1b33"/>
<text x="176" y="42" text-anchor="middle" font-family="BL" font-size="20" fill="#5fd0ff">1:25</text>
<circle cx="268" cy="35" r="20" fill="url(#hd)" stroke="#8793a6"/><circle cx="268" cy="35" r="6" fill="#5b6678"/>
<circle cx="160" cy="210" r="112" fill="#cfd7e3" stroke="#9aa6b8" stroke-width="3"/><circle cx="160" cy="210" r="94" fill="#7d8899"/>
<circle cx="160" cy="210" r="84" fill="url(#gl)"/>
<path d="M98 228c22-30 58-6 84-30s44-6 52 10c-10 44-50 70-92 64-24-4-40-22-44-44z" fill="#ffffff" opacity=".35"/>
<path d="M112 168a62 62 0 0 1 56-28" stroke="#fff" stroke-width="8" stroke-linecap="round" fill="none" opacity=".7"/>
<rect x="266" y="190" width="10" height="40" rx="5" fill="url(#hd)"/></g>'''
FREEZER = '''<g filter="url(#sh)"><rect x="0" y="40" width="460" height="220" rx="20" fill="url(#st)" stroke="#b9c3d2" stroke-width="2"/>
<rect x="-6" y="0" width="472" height="56" rx="16" fill="url(#st2)" stroke="#b9c3d2" stroke-width="2"/>
<rect x="170" y="56" width="120" height="16" rx="8" fill="url(#hd)"/>
<circle cx="40" cy="96" r="7" fill="#2fd47f"/><circle cx="64" cy="96" r="7" fill="#ffb020"/><circle cx="88" cy="96" r="7" fill="#cfd7e3"/>
<g stroke="#b9c3d2" stroke-width="5" stroke-linecap="round"><path d="M340 200h80M340 216h80M340 232h80"/></g>
<rect x="40" y="30" width="380" height="10" rx="5" fill="#fff" opacity=".7"/>
<rect x="24" y="260" width="34" height="12" rx="4" fill="#5b6678"/><rect x="402" y="260" width="34" height="12" rx="4" fill="#5b6678"/></g>'''
WRENCH = '''<g filter="url(#sh)"><path d="M0 0a46 46 0 0 0 58 58l140 140a20 20 0 0 0 28-28L86 30A46 46 0 0 0 28-28l30 30-6 24-24 6z" fill="url(#hd)" stroke="#6e7a8d" stroke-width="2"/></g>'''
SCREW = '''<g filter="url(#sh)"><rect x="-14" y="0" width="28" height="96" rx="12" fill="url(#bl)"/><rect x="-14" y="22" width="28" height="6" fill="#0f2f8f" opacity=".5"/><rect x="-14" y="44" width="28" height="6" fill="#0f2f8f" opacity=".5"/>
<rect x="-5" y="94" width="10" height="110" fill="url(#hd)"/><path d="M-5 204h10l-2 16h-6z" fill="#6e7a8d"/></g>'''
METER = '''<g filter="url(#sh)"><rect x="0" y="0" width="120" height="190" rx="18" fill="#ffb020"/><rect x="12" y="12" width="96" height="166" rx="12" fill="#252f40"/>
<rect x="22" y="24" width="76" height="40" rx="6" fill="#c8f0d8"/><text x="60" y="53" text-anchor="middle" font-family="BL" font-size="22" fill="#0d1b33">220</text>
<circle cx="60" cy="116" r="30" fill="#3a4659" stroke="#5b6678" stroke-width="3"/><path d="M60 116l18-16" stroke="#fff" stroke-width="5" stroke-linecap="round"/>
<circle cx="38" cy="162" r="7" fill="#e5484d"/><circle cx="82" cy="162" r="7" fill="#0d1b33" stroke="#5b6678"/></g>'''

def scene(kind, w, h):
    """Сцена-иллюстрация без текста; техника стоит на «полу» (низ = floor)."""
    s = min(w / 900, h / 700)
    FL = .9
    items = {   # (svg, центр x, низ y, масштаб)
        "fridge": [(FRIDGE, .5, FL, .9), (METER, .76, FL, .75), (WRENCH, .24, FL, .7)],
        "washer": [(WASHER, .5, FL, 1.25), (SCREW, .2, FL, .95), (METER, .8, FL, .8)],
        "freezer": [(FREEZER, .5, FL, 1.2), (WRENCH, .14, FL, .7), (METER, .86, FL, .7)],
        "all": [(FRIDGE, .36, FL, .85), (WASHER, .64, FL, .9), (WRENCH, .12, FL, .6), (METER, .88, FL, .62)],
    }[kind]
    DIM = {id(FRIDGE): (300, 554), id(WASHER): (320, 360), id(FREEZER): (460, 272), id(METER): (120, 190), id(WRENCH): (230, 120), id(SCREW): (200, 120)}
    g = ""
    for svg, cx, by, k in items:
        k *= s; bw, bh = DIM[id(svg)]
        x = cx * w - bw * k / 2; y = by * h - bh * k
        if svg is WRENCH: g += f'<g transform="translate({x + 20*k},{y + 40*k}) scale({k}) rotate(-12)">{svg}</g>'
        elif svg is SCREW: g += f'<g transform="translate({x + 10*k},{y + 104*k}) scale({k}) rotate(-75)">{svg}</g>'
        else: g += f'<g transform="translate({x},{y}) scale({k})">{svg}</g>'
    return g

def page(w, h, inner, dark=False):
    bgc = ("radial-gradient(60% 70% at 85% 30%,rgba(124,212,255,.32),transparent 60%),radial-gradient(60% 60% at 0% 100%,rgba(31,94,255,.4),transparent 60%),linear-gradient(160deg,#0b1838,#13285c)"
           if dark else "radial-gradient(60% 60% at 50% 95%,rgba(124,212,255,.45),transparent 70%),linear-gradient(180deg,#f2f6ff,#dfe9fb)")
    return f'''<html><head><style>{F}body{{margin:0}}.c{{width:{w}px;height:{h}px;position:relative;overflow:hidden;background:{bgc}}}
svg.s{{position:absolute;inset:0}}</style></head><body><div class="c">{inner}</div></body></html>'''

def img_only(kind, w, h):
    # для изображений без текста сцена занимает центр, края — фон (Google кадрирует)
    return page(w, h, f'<svg class="s" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEF}<ellipse cx="{w/2}" cy="{h*.905}" rx="{w*.4}" ry="{h*.035}" fill="#9fb4d8" opacity=".35"/>{scene(kind, w, h)}</svg>')

def text_banner(kind, w, h, title, sub):
    land = w / h > 1.5
    if land:
        tw, sw = 0.5, 0.5
        txt = f'''<div style="position:absolute;left:{w*.06}px;top:0;bottom:0;width:{w*.48}px;display:flex;flex-direction:column;justify-content:center;font-family:H,HL;color:#fff">
<div style="font-size:{h*.105}px;line-height:1.02;letter-spacing:-.02em">{title}</div>
<div style="font-family:B,BL;font-size:{h*.05}px;color:#c8d4ee;margin-top:{h*.045}px">{sub}</div>
<div style="align-self:flex-start;margin-top:{h*.06}px;background:#fff;color:#0b1838;font-family:B,BL;font-size:{h*.048}px;padding:{h*.03}px {h*.055}px;border-radius:{h*.03}px">Вызвать мастера</div></div>'''
        sc = f'<svg class="s" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEF}<g transform="translate({w*.5},{h*.02})">{scene(kind, w*.5, h*.96)}</g></svg>'
    else:
        txt = f'''<div style="position:absolute;left:{w*.08}px;right:{w*.08}px;top:{h*.07}px;font-family:H,HL;color:#fff;text-align:center">
<div style="font-size:{w*.092}px;line-height:1.03;letter-spacing:-.02em">{title}</div>
<div style="font-family:B,BL;font-size:{w*.042}px;color:#c8d4ee;margin-top:{w*.03}px">{sub}</div></div>
<div style="position:absolute;left:50%;transform:translateX(-50%);bottom:{h*.06}px;background:#fff;color:#0b1838;font-family:B,BL;font-size:{w*.045}px;padding:{w*.03}px {w*.06}px;border-radius:{w*.03}px;white-space:nowrap">Вызвать мастера</div>'''
        top = h * (.36 if h > w else .33); sh = h * (.48 if h > w else .5)
        sc = f'<svg class="s" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEF}<g transform="translate({w*.1},{top})">{scene(kind, w*.8, sh)}</g></svg>'
    return page(w, h, sc + txt, dark=True)

MARK = '<svg viewBox="0 0 40 40" width="{s}" height="{s}"><rect width="40" height="40" rx="12" fill="#1f5eff"/><g fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><rect x="11" y="7" width="18" height="26" rx="3"/><path d="M11 16h18M15 11v2M15 20v4"/></g><circle cx="31" cy="31" r="6.5" fill="#ffb020" stroke="#fff" stroke-width="2"/></svg>'
SETS = [("holodilniki", "fridge", "Ремонт холодильников на&nbsp;дому"), ("stiralnye-mashiny", "washer", "Ремонт стиральных машин на&nbsp;дому"),
        ("morozilniki", "freezer", "Ремонт морозильников на&nbsp;дому"), ("obshchiy", "all", "Ремонт холодильников и&nbsp;стиральных машин")]
SUB = "Алматы · выезд во все районы"

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    def shot(html_, w, h, name):
        pg.set_viewport_size({"width": w, "height": h}); pg.set_content(html_); pg.wait_for_timeout(150)
        pg.screenshot(path=str(OUT / name), type="jpeg", quality=90)
    for slug, kind, title in SETS:
        shot(img_only(kind, 1200, 628), 1200, 628, f"bez-teksta-{slug}-1200x628.jpg")
        shot(img_only(kind, 1200, 1200), 1200, 1200, f"bez-teksta-{slug}-1200x1200.jpg")
        shot(text_banner(kind, 1200, 628, title, SUB), 1200, 628, f"s-tekstom-{slug}-1200x628.jpg")
        shot(text_banner(kind, 1200, 1200, title, SUB), 1200, 1200, f"s-tekstom-{slug}-1200x1200.jpg")
        shot(text_banner(kind, 960, 1200, title, SUB), 960, 1200, f"s-tekstom-{slug}-960x1200.jpg")
    pg.set_viewport_size({"width": 1200, "height": 1200})
    pg.set_content(f'<html><body style="margin:0;width:1200px;height:1200px;background:#fff;display:grid;place-items:center">{MARK.format(s=820)}</body></html>')
    pg.screenshot(path=str(OUT / "logo-1200x1200.png"))
    pg.set_viewport_size({"width": 1200, "height": 300})
    pg.set_content(f'<html><head><style>{F}</style></head><body style="margin:0;width:1200px;height:300px;background:#fff;display:flex;align-items:center;justify-content:center;gap:44px;font-family:H,HL;font-size:112px;color:#0d1b33;letter-spacing:-.02em">{MARK.format(s=190)}Ремонт техники</body></html>')
    pg.wait_for_timeout(150); pg.screenshot(path=str(OUT / "logo-1200x300.png"))
    b.close()
print(len(list(OUT.iterdir())), "файлов")
