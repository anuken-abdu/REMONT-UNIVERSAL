"""Favicon и баннеры превью (assets/img/og/*.jpg) в стиле сайта. Запуск после build.py, затем build.py ещё раз."""
import base64, hashlib, json, pathlib, html
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent; A = ROOT / "assets"; OUT = A / "img" / "og"; OUT.mkdir(parents=True, exist_ok=True)
b64 = lambda p: base64.b64encode(p.read_bytes()).decode()
F = "".join(f'@font-face{{font-family:{n};font-weight:{w};src:url(data:font/woff2;base64,{b64(A/"fonts"/f)})}}' for n, w, f in [
    ("H", 800, "commissioner-cyrillic-800-normal.woff2"), ("HL", 800, "commissioner-latin-800-normal.woff2"),
    ("M", 500, "jetbrains-mono-cyrillic-500-normal.woff2"), ("ML", 500, "jetbrains-mono-latin-500-normal.woff2")])
MARK = '<svg viewBox="0 0 40 40" width="{s}" height="{s}"><rect width="40" height="40" rx="11" fill="#1446d8"/><g fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><rect x="11" y="7" width="18" height="26" rx="3"/><path d="M11 16h18M15 11v2M15 20v4"/></g><circle cx="31" cy="31" r="6.5" fill="#ffb020" stroke="#fff" stroke-width="2"/></svg>'
def og_html(t):
    size = 84 if len(t) <= 26 else 70 if len(t) <= 40 else 58
    return f'''<html><head><style>{F}body{{margin:0}}.b{{width:1200px;height:630px;position:relative;background:#f3f6fb;color:#0d1b33;font-family:H,HL;overflow:hidden}}
.b::before{{content:"";position:absolute;inset:0;background-image:linear-gradient(#d6deeb 1px,transparent 1px),linear-gradient(90deg,#d6deeb 1px,transparent 1px);background-size:40px 40px;opacity:.7}}
.p{{position:absolute;left:56px;right:56px;top:56px;bottom:56px;background:#fff;border:2px solid #c3cee0;border-radius:28px;padding:52px 60px;box-shadow:0 20px 50px -20px rgba(13,27,51,.25)}}
.r{{position:absolute;top:20px;width:12px;height:12px;border-radius:50%;background:#c3cee0}}
.l{{display:flex;align-items:center;gap:16px;font-size:30px}}.l small{{display:block;font-family:M,ML;font-size:16px;color:#6b7790;text-transform:uppercase;letter-spacing:.05em}}
h1{{margin:44px 0 0;font-size:{size}px;line-height:1.05;letter-spacing:-.02em;max-width:980px}}
.s{{position:absolute;left:60px;right:60px;bottom:44px;display:flex;justify-content:space-between;align-items:center;font-family:M,ML;font-size:24px;color:#46536b;border-top:2px dashed #c3cee0;padding-top:26px}}
.s b{{font-family:H,HL;font-size:40px;color:#1446d8;letter-spacing:-.01em}}
</style></head><body><div class="b"><div class="p"><i class="r" style="left:20px"></i><i class="r" style="right:20px"></i>
<div class="l">{MARK.format(s=64)}<div>Ремонт техники<small>Алматы · все районы</small></div></div>
<h1>{html.escape(t)}</h1><div class="s"><span>ВЫЕЗД МАСТЕРА НА ДОМ</span><b>8 771 274 70 92</b></div></div></div></body></html>'''
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
        key = hashlib.md5(("v1" + title).encode()).hexdigest()
        if man.get(slug) == key and (OUT / f"{slug}.jpg").exists(): continue
        pg2.set_content(og_html(title)); pg2.wait_for_timeout(120); pg2.screenshot(path=str(OUT / f"{slug}.jpg"), type="jpeg", quality=86); man[slug] = key; n += 1
    man_p.write_text(json.dumps(man, ensure_ascii=False, indent=1)); b.close()
print("og rendered", n)
