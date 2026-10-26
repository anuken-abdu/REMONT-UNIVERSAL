"""Favicon и баннеры превью (assets/img/og/*.jpg) в стиле сайта. Запуск после build.py, затем build.py ещё раз."""
import base64, hashlib, json, pathlib, html
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent; A = ROOT / "assets"; OUT = A / "img" / "og"; OUT.mkdir(parents=True, exist_ok=True)
b64 = lambda p: base64.b64encode(p.read_bytes()).decode()
F = "".join(f'@font-face{{font-family:{n};font-weight:{w};src:url(data:font/woff2;base64,{b64(ROOT/"src"/"fonts"/f)})}}' for n, w, f in [
    ("H", 800, "manrope-cyrillic-800-normal.woff2"), ("HL", 800, "manrope-latin-800-normal.woff2"),
    ("M", 500, "manrope-cyrillic-500-normal.woff2"), ("ML", 500, "manrope-latin-500-normal.woff2"), ("Manrope", 700, "manrope-latin-700-normal.woff2")])
MARK = '<svg viewBox="0 0 40 40" width="{s}" height="{s}"><rect width="40" height="40" rx="12" fill="#1f5eff"/><g fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><rect x="11" y="7" width="18" height="26" rx="3"/><path d="M11 16h18M15 11v2M15 20v4"/></g><circle cx="31" cy="31" r="6.5" fill="#ffb020" stroke="#fff" stroke-width="2"/></svg>'
import sys; sys.path.insert(0, str(ROOT / "src")); from art import art, DEF
def og_html(t):
    size = 76 if len(t) <= 26 else 64 if len(t) <= 40 else 54
    return f'''<html><head><style>{F}body{{margin:0}}.b{{width:1200px;height:630px;position:relative;overflow:hidden;color:#fff;font-family:H,HL;
background:radial-gradient(600px 400px at 85% 30%,rgba(124,212,255,.32),transparent 60%),radial-gradient(600px 500px at 0% 100%,rgba(31,94,255,.4),transparent 60%),linear-gradient(160deg,#0b1838,#13285c)}}
.l{{position:absolute;left:64px;top:56px;display:flex;align-items:center;gap:16px;font-size:30px}}.l small{{display:block;font-family:M,ML;font-size:19px;color:#9fb0d3}}
h1{{position:absolute;left:64px;width:640px;top:190px;margin:0;font-size:{size}px;line-height:1.06;letter-spacing:-.025em}}
.p{{position:absolute;left:64px;bottom:60px;font-size:40px;letter-spacing:-.01em}}.p small{{display:block;font-family:M,ML;font-size:20px;color:#9fb0d3;letter-spacing:0;margin-bottom:4px}}
.a{{position:absolute;right:40px;bottom:-20px;width:430px}}.a svg{{width:100%;height:auto}}</style></head><body>
<svg width="0" height="0" style="position:absolute">{DEF}</svg><div class="b"><div class="l">{MARK.format(s=64)}<div>Ремонт техники<small>Алматы, на дому</small></div></div>
<h1>{html.escape(t)}</h1><div class="p"><small>Выезд мастера во все районы</small>8 771 274 70 92</div><div class="a">{art("all")}</div></div></body></html>'''
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 512, "height": 512})
    pg.set_content(f'<html><body style="margin:0;background:#1446d8">{MARK.format(s=512).replace("rx=\"11\"", "rx=\"0\"")}</body></html>')
    pg.wait_for_timeout(150); pg.screenshot(path=str(A / "icon-512.png"))
    im = Image.open(A / "icon-512.png").convert("RGB")
    im.resize((192, 192), Image.LANCZOS).save(A / "icon-192.png"); im.resize((180, 180), Image.LANCZOS).save(A / "apple-touch-icon.png")
    pg.set_content(f'<html><body style="margin:0;background:transparent">{MARK.format(s=512)}</body></html>')
    pg.screenshot(path=str(A / "fav.png"), omit_background=True)
    Image.open(A / "fav.png").save(A / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)]); (A / "fav.png").unlink()
    OG = json.loads((ROOT / "src" / "og_list.json").read_text()); man_p = OUT / "manifest.json"
    man = json.loads(man_p.read_text()) if man_p.exists() else {}
    pg2 = b.new_page(viewport={"width": 1200, "height": 630}); n = 0
    for url, (slug, title) in OG.items():
        key = hashlib.md5(("v2" + title).encode()).hexdigest()
        if man.get(slug) == key and (OUT / f"{slug}.jpg").exists(): continue
        pg2.set_content(og_html(title)); pg2.wait_for_timeout(120); pg2.screenshot(path=str(OUT / f"{slug}.jpg"), type="jpeg", quality=86); man[slug] = key; n += 1
    man_p.write_text(json.dumps(man, ensure_ascii=False, indent=1)); b.close()
print("og rendered", n)
