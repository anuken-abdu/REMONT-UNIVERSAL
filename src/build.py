# -*- coding: utf-8 -*-
"""Генератор сайта ремонта техники: python3 src/build.py → dist/"""
import html, json, pathlib, shutil, datetime
from urllib.parse import quote
from data import *

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
VER = "2610261700"
TODAY = datetime.date.today().isoformat()
E = lambda s: html.escape(str(s), quote=True)
def WA_URL(t="Здравствуйте! Нужен ремонт техники."): return f"https://wa.me/{WA}?text=" + quote(t)

P = {
    "fridge": '<rect x="5" y="2.5" width="14" height="19" rx="2"/><path d="M5 9.5h14M8 5.5v2M8 12.5v3.5"/>',
    "washer": '<rect x="3.5" y="2.5" width="17" height="19" rx="2"/><path d="M3.5 7h17"/><circle cx="12" cy="14" r="4.5"/><path d="M6.5 4.8h1.5M16 4.8h1.5"/><path d="M9.5 14.5c1-1 2-.2 2.5.2s1.5.8 2.5-.2"/>',
    "freezer": '<rect x="2.5" y="8" width="19" height="12" rx="2"/><path d="M2.5 11.5h19M9 5h6M12 3v4"/><path d="M10 15.5h4"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
    "wa": '<path d="M20.5 11.7a8.5 8.5 0 0 1-12.6 7.4L3.5 20.5l1.4-4.3a8.5 8.5 0 1 1 15.6-4.5z"/><path d="M8.8 8.6c.2-.5.5-.5.8-.5h.5c.2 0 .4 0 .5.4l.7 1.6c0 .2 0 .4-.1.5l-.5.6c-.1.2-.1.3 0 .5.5.9 1.3 1.7 2.3 2.2.2.1.3.1.5-.1l.6-.7c.1-.2.3-.2.5-.1l1.6.8c.2.1.3.2.3.3 0 .7-.4 1.4-1 1.6-.7.3-1.6.3-3.4-.6a8.8 8.8 0 0 1-3.2-3.1c-.7-1.2-.8-2.2-.1-3.6z"/>',
    "pin": '<path d="M12 21s-7-6.1-7-11.5A7 7 0 0 1 19 9.5C19 14.9 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>', "back": '<path d="M19 12H5M11 6l-6 6 6 6"/>', "up": '<path d="M12 19V5M6 11l6-6 6 6"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>', "close": '<path d="M6 6l12 12M18 6L6 18"/>', "chev": '<path d="M6 9l6 6 6-6"/>',
    "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>', "send": '<path d="M4 12l16-8-6 16-3-7z"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>', "tool": '<path d="M14.5 6.5a4 4 0 0 0-5.3 5.3L3.5 17.5 6.5 20.5l5.7-5.7a4 4 0 0 0 5.3-5.3l-2.6 2.6-2.4-.6-.6-2.4z"/>',
}
def ic(n, cls="i"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{P[n]}</g></svg>'

MARK = '<svg class="logo-m" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="11" fill="#1446d8"/><g fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><rect x="11" y="7" width="18" height="26" rx="3"/><path d="M11 16h18M15 11v2M15 20v4"/></g><circle cx="31" cy="31" r="6.5" fill="#ffb020" stroke="#fff" stroke-width="2"/></svg>'
def logo(): return f'<a class="logo" href="/" aria-label="{BRAND} — на главную">{MARK}<span><b>Ремонт техники</b><small>Алматы · ремонт на дому</small></span></a>'
def bg(key): return f' style="--ph:url(/images/{key}.jpg?v={VER})"'

NAV = [("/remont-holodilnikov/", "Холодильники"), ("/remont-stiralnyh-mashin/", "Стиральные машины"), ("/remont-morozilnikov/", "Морозильники"),
       ("/rayony/", "Районы"), ("/voprosy/", "Вопросы"), ("/kontakty/", "Контакты")]

def cta(cls="", call_label=None, wa_text=None):
    return f'''<div class="cta {cls}"><a class="btn btn-p" href="tel:{TEL}" data-ev="call">{ic("phone")}<span>{call_label or PHONE_LOCAL}</span></a><a class="btn btn-wa" href="{WA_URL(wa_text) if wa_text else WA_URL()}" target="_blank" rel="noopener" data-ev="wa">{ic("wa")}<span>WhatsApp</span></a></div>'''

def picker(pre=None, district=None):
    """Подбор неисправности → готовое сообщение мастеру в WhatsApp. Работает и без JS (ссылки)."""
    tabs = "".join(f'<button type="button" role="tab" class="pk-t{" on" if (pre or DEVICES[0]["key"]) == d["key"] else ""}" data-dev="{d["key"]}" aria-selected="{"true" if (pre or DEVICES[0]["key"]) == d["key"] else "false"}">{ic(d["key"])}<span>{d["short"]}</span></button>' for d in DEVICES)
    groups = ""
    for d in DEVICES:
        on = (pre or DEVICES[0]["key"]) == d["key"]
        chips = "".join(f'<a class="pk-c" href="{WA_URL(f"Здравствуйте! Нужен ремонт: {d["acc"]}. Проблема: {f.lower()}.")}" target="_blank" rel="noopener" data-ev="wa" data-fault="{E(f)}">{E(f)}</a>' for f in d["faults"])
        groups += f'<div class="pk-g" data-dev="{d["key"]}" data-acc="{E(d["acc"])}"{"" if on else " hidden"}>{chips}<a class="pk-c pk-o" href="{WA_URL(f"Здравствуйте! Нужен ремонт: {d["acc"]}.")}" target="_blank" rel="noopener" data-ev="wa" data-fault="">Другое</a></div>'
    opts = "".join(f'<option{" selected" if district == n else ""}>{n}</option>' for _, n, _, _ in DISTRICTS)
    return f'''<div class="pk" id="pk"><div class="pk-h"><b>Что случилось?</b><small>Выберите неисправность — откроется WhatsApp с готовым сообщением мастеру</small></div>
<div class="pk-tabs" role="tablist">{tabs}</div>{groups}
<div class="pk-f"><label for="pkD">Район</label><select id="pkD"><option value="">Не выбран</option>{opts}</select><label for="pkB">Марка</label><input id="pkB" list="pkBL" placeholder="Например, Samsung" maxlength="40"><datalist id="pkBL">{"".join(f"<option>{b}</option>" for b in BRANDS)}</datalist></div></div>'''

def header(cur):
    items = "".join(f'<li><a href="{h}"{" aria-current=page" if h == cur else ""}>{n}</a></li>' for h, n in NAV)
    return f'''<a class="skip" href="#main">Перейти к содержанию</a>
<header class="hdr"><div class="wrap hdr-in">{logo()}
<nav class="nav" id="nav" aria-label="Основное меню"><ul>{items}</ul><div class="nav-cta">{cta()}</div></nav>
<a class="hdr-ph" href="tel:{TEL}" data-ev="call"><small>Звоните, Алматы</small>{PHONE_LOCAL}</a>
<a class="hdr-wa" href="{WA_URL()}" target="_blank" rel="noopener" data-ev="wa" aria-label="WhatsApp">{ic("wa")}</a>
<button class="burger" type="button" aria-label="Меню" aria-controls="nav" aria-expanded="false">{ic("menu", "i i-o")}{ic("close", "i i-c")}</button></div></header>'''

def footer():
    dv = "".join(f'<li><a href="/{d["slug"]}/">Ремонт {d["gen"]}</a></li>' for d in DEVICES)
    ds = "".join(f'<li><a href="/rayony/{s}/">{n} район</a></li>' for s, n, _, _ in DISTRICTS)
    pages = "".join(f'<li><a href="{h}">{n}</a></li>' for h, n in NAV[3:])
    ig = f'<li><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a></li>' if INSTAGRAM else ""
    return f'''<footer class="ftr"><div class="wrap">
<div class="ftr-g"><div class="ftr-a">{logo()}<p>{LEAD}</p><a class="ftr-tel" href="tel:{TEL}" data-ev="call">{PHONE_LOCAL}</a>{f'<p class="ftr-h">{HOURS}</p>' if HOURS else ""}</div>
<div><h4>Ремонт</h4><ul>{dv}</ul></div><div><h4>Районы Алматы</h4><ul class="ftr-2">{ds}</ul></div><div><h4>Сайт</h4><ul>{pages}<li><a href="{WA_URL()}" target="_blank" rel="noopener" data-ev="wa">WhatsApp</a></li>{ig}</ul></div></div>
<div class="ftr-b"><span>© {datetime.date.today().year} {BRAND}, Алматы</span><a href="/politika/">Политика конфиденциальности</a><a href="{DEV_URL}" target="_blank" rel="noopener">Разработка сайта — {DEV_NAME}</a></div></div></footer>
<div class="mbar">{cta(call_label="Позвонить")}</div>
<div class="fl"><button class="fl-b fl-back" type="button" aria-label="Назад" hidden>{ic("back")}</button><button class="fl-b fl-top" type="button" aria-label="Наверх" hidden>{ic("up")}</button><button class="fl-b fl-chat" type="button" aria-label="Задать вопрос в чате" aria-controls="chat" aria-expanded="false">{ic("chat")}<span>Спросить</span></button></div>
<section class="chat" id="chat" role="dialog" aria-label="Онлайн-помощник" hidden><div class="chat-h">{MARK}<div><b>Онлайн-помощник</b><small><i></i>Отвечает сразу</small></div><button class="chat-x" type="button" aria-label="Закрыть чат">{ic("close")}</button></div>
<div class="chat-b" id="chatB" aria-live="polite"></div><div class="chat-q" id="chatQ"></div>
<div class="chat-cta"><a href="tel:{TEL}" data-ev="call">{ic("phone")}Позвонить</a><a href="{WA_URL()}" target="_blank" rel="noopener" data-ev="wa" id="chatWa">{ic("wa")}В WhatsApp</a></div>
<form class="chat-f" id="chatF" autocomplete="off"><label class="sr" for="chatI">Ваш вопрос</label><input id="chatI" type="text" maxlength="500" placeholder="Например: холодильник не морозит"><button type="submit" aria-label="Отправить">{ic("send")}</button></form></section>'''

ORG = {"@context": "https://schema.org", "@type": ["LocalBusiness", "HomeAndConstructionBusiness"], "@id": SITE + "/#org", "name": BRAND, "url": SITE + "/",
       "telephone": PHONE, "image": SITE + "/assets/img/og/home.jpg", "logo": SITE + "/icon-512.png", "description": LEAD,
       "address": {"@type": "PostalAddress", "addressLocality": "Алматы", "addressCountry": "KZ"},
       "areaServed": [{"@type": "City", "name": "Алматы"}] + [{"@type": "AdministrativeArea", "name": f"{n} район, Алматы"} for _, n, _, _ in DISTRICTS],
       "knowsAbout": ["Ремонт холодильников", "Ремонт стиральных машин", "Ремонт морозильников"],
       "contactPoint": {"@type": "ContactPoint", "telephone": PHONE, "contactType": "customer service", "availableLanguage": ["ru", "kk"]},
       "sameAs": [f"https://wa.me/{WA}"] + ([INSTAGRAM] if INSTAGRAM else [])}
def ld_crumbs(items): return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + h} for i, (h, n) in enumerate(items)]}
def ld_faq(faq): return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
def ld_svc(name, desc, url, area=None):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "description": desc, "serviceType": name, "provider": {"@id": SITE + "/#org"}, "url": SITE + url,
            "areaServed": area or {"@type": "City", "name": "Алматы"}}

OG = {}
def page(url, title, desc, body, cur="", ld=(), crumbs=None, og_title=None):
    og = "home" if url == "/" else url.strip("/").replace("/", "-")
    if url != "/404/": OG[url] = (og, og_title or title.split(" — ")[0].split(" | ")[0])
    else: og = "home"
    lds = [ORG] + list(ld) + ([ld_crumbs([("/", "Главная")] + crumbs)] if crumbs else [])
    if url == "/": lds.append({"@context": "https://schema.org", "@type": "WebSite", "name": BRAND, "url": SITE + "/", "inLanguage": "ru"})
    tag = GA_ID or GADS_ID
    ga = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={tag}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());'
          + "".join(f'gtag("config","{x}");' for x in (GA_ID, GADS_ID) if x) + "</script>") if tag else ""
    cr = ""
    if crumbs:
        cr = '<nav class="crumbs" aria-label="Хлебные крошки"><ol><li><a href="/">Главная</a></li>' + "".join(
            f'<li><a href="{h}">{n}</a></li>' if i < len(crumbs) - 1 else f'<li aria-current="page">{n}</li>' for i, (h, n) in enumerate(crumbs)) + "</ol></nav>"
    body = body.replace("<!--CRUMBS-->", cr)
    cfg = json.dumps({"ads": [GADS_ID, GADS_CALL_LABEL, GADS_WA_LABEL], "tel": TEL, "phone": PHONE_LOCAL, "wa": WA,
                      "dev": [[d["key"], d["short"], d["acc"], d["slug"]] for d in DEVICES], "districts": [n for _, n, _, _ in DISTRICTS]}, ensure_ascii=False)
    full = SITE + url
    return f'''<!doctype html>
<html lang="ru"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
{ga}
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<link rel="canonical" href="{full}"><meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#1446d8"><meta name="geo.region" content="KZ-75"><meta name="geo.placename" content="Алматы"><meta name="geo.position" content="43.238949;76.889709"><meta name="ICBM" content="43.238949, 76.889709">
<meta property="og:type" content="website"><meta property="og:locale" content="ru_KZ"><meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{full}">
<meta property="og:image" content="{SITE}/assets/img/og/{og}.jpg?v={VER}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" href="/icon-192.png" type="image/png" sizes="192x192"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/commissioner-cyrillic-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/ibm-plex-sans-cyrillic-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/styles.css?v={VER}">
{"".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)}
</head><body>
{header(cur)}
<main id="main">
{body}
</main>
{footer()}
<script>window.RT={cfg};</script><script src="/assets/app.js?v={VER}" defer></script>
</body></html>'''

def write(url, content):
    p = DIST / "404.html" if url == "/404/" else (DIST / url.strip("/") / "index.html" if url != "/" else DIST / "index.html")
    p.parent.mkdir(parents=True, exist_ok=True); p.write_text(content, encoding="utf-8")

# ---------- блоки ----------
def sec(title, inner, sub="", alt=False, link=None, sid=""):
    lk = f'<a class="lnk" href="{link[1]}">{link[0]} {ic("arrow")}</a>' if link else ""
    return f'''<section class="sec{" sec-alt" if alt else ""}"{f' id="{sid}"' if sid else ""}><div class="wrap"><div class="sec-h"><div><h2>{title}</h2>{f"<p>{sub}</p>" if sub else ""}</div>{lk}</div>{inner}</div></section>'''
def dev_cards(exclude=None):
    out = ""
    for d in DEVICES:
        if d["slug"] == exclude: continue
        top = "".join(f"<li>{f}</li>" for f in d["faults"][:4])
        img = f'<img class="dc-ph" src="/images/{d["slug"]}.jpg?v={VER}" alt="Ремонт {d["gen"]} в Алматы" width="640" height="360" loading="lazy" decoding="async" onerror="this.remove()">' if (ROOT / "images" / f'{d["slug"]}.jpg').exists() else ""
        out += f'''<a class="dc" href="/{d["slug"]}/">{img}<span class="dc-ic">{ic(d["key"])}</span><span class="dc-l">Ремонт</span><b>{d["short"]}</b><ul>{top}</ul><span class="more">Все неисправности {ic("arrow")}</span></a>'''
    return f'<div class="dc-g">{out}</div>'
def faults_html(d):
    return '<ul class="ft">' + "".join(f'<li><a href="{WA_URL(f"Здравствуйте! Нужен ремонт: {d["acc"]}. Проблема: {f.lower()}.")}" target="_blank" rel="noopener" data-ev="wa"><span>{E(f)}</span><em>Вызвать мастера {ic("arrow")}</em></a></li>' for f in d["faults"]) + "</ul>"
def steps():
    return '<ol class="st">' + "".join(f'<li><span class="st-n">{i+1:02d}</span><b>{t}</b><p>{x}</p></li>' for i, (t, x) in enumerate(STEPS)) + "</ol>"
def call_info():
    return '<ul class="ci">' + "".join(f'<li><b>{t}</b><span>{x}</span></li>' for t, x in CALL_INFO) + "</ul>"
def faq_html(faq):
    return '<div class="faq">' + "".join(f'<details><summary>{q}{ic("chev")}</summary><p>{a}</p></details>' for q, a in faq) + "</div>"
def tags(items): return '<ul class="tg">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"
def districts_html(cur=None):
    return '<ul class="ds">' + "".join(f'<li><a href="/rayony/{s}/"{" aria-current=page" if s == cur else ""}>{ic("pin")}<span><b>{n}</b><small>{", ".join(m)}</small></span></a></li>' for s, n, _, m in DISTRICTS) + "</ul>"
def brands_html(): return '<p class="br">' + "".join(f"<span>{b}</span>" for b in BRANDS) + "<span>и другие</span></p>"
def band(title="Сломалась техника?", sub="Позвоните или напишите в WhatsApp — согласуем время выезда мастера."):
    return f'''<section class="band"><div class="wrap band-in"><div><h2>{title}</h2><p>{sub}</p></div>{cta()}</div></section>'''
def ph(h1, lead, key="ph", wa_text=None, pre=None, district=None):
    return f'''<section class="ph"><div class="wrap ph-in"><div class="ph-t"><!--CRUMBS--><h1>{h1.replace(" в ", " в&nbsp;").replace(" и ", " и&nbsp;")}</h1><p>{lead}</p>{cta(wa_text=wa_text)}</div>{picker(pre, district)}</div></section>'''

# ---------- страницы ----------
def build_home():
    body = f'''<section class="hero"><div class="wrap hero-in"><div class="hero-t">
<h1>Ремонт холодильников, стиральных машин и&nbsp;морозильников в&nbsp;Алматы</h1>
<p class="hero-s">Мастер приезжает на дом во все районы города. Диагностика и ремонт на месте, стоимость — до начала работ.</p>
<div class="hero-act"><a class="hero-ph" href="tel:{TEL}" data-ev="call"><small>Позвонить мастеру</small>{PHONE_LOCAL}</a>
<a class="hero-wa" href="{WA_URL()}" target="_blank" rel="noopener" data-ev="wa">{ic("wa")}Написать в WhatsApp</a></div>
<dl class="spec"><div><dt>Выезд</dt><dd>все 8 районов</dd></div><div><dt>Ремонт</dt><dd>на дому</dd></div><div><dt>Стоимость</dt><dd>до начала работ</dd></div></dl></div>
{picker()}</div></section>
{sec("Что ремонтируем", dev_cards(), "Выберите технику — там список частых неисправностей и вызов мастера в один клик.")}
{sec("Как проходит ремонт", steps(), "", alt=True)}
{sec("Мастер во всех районах Алматы", districts_html(), "Выезжаем по всему городу — выберите свой район.", link=("Все районы", "/rayony/"))}
{sec("Ремонтируем технику популярных марок", brands_html(), "", alt=True)}
{sec("Что сказать при звонке", call_info(), "Так мастер быстрее поймёт причину и возьмёт нужные запчасти.")}
{sec("Частые вопросы", faq_html(FAQ), "", alt=True, link=("Все вопросы", "/voprosy/"))}
{band()}'''
    write("/", page("/", "Ремонт холодильников и стиральных машин в Алматы на дому",
                    f"Ремонт холодильников, стиральных машин и морозильников на дому в Алматы. Выезд мастера во все районы. Тел. {PHONE_LOCAL}, WhatsApp.",
                    body, "/", [ld_faq(FAQ)], og_title="Ремонт холодильников и стиральных машин"))

def build_devices():
    for d in DEVICES:
        url = f'/{d["slug"]}/'
        faq = d["faq"] + FAQ[1:3]
        body = f'''{ph(d["h1"], d["lead"], wa_text=f"Здравствуйте! Нужен ремонт: {d['acc']}.", pre=d["key"])}
{sec("Частые неисправности", faults_html(d), "Нажмите на свою проблему — откроется WhatsApp с готовым сообщением мастеру.")}
{sec("Какие модели ремонтируем", tags(d["types"]) + brands_html(), "", alt=True)}
{sec("Как проходит ремонт", steps())}
{sec(f"Ремонт {d['gen']} по районам", districts_html(), "", alt=True)}
{sec("Вопросы", faq_html(faq))}
{sec("Другая техника", dev_cards(exclude=d["slug"]), "", alt=True)}
{band()}'''
        write(url, page(url, f'{d["h1"]} на дому — выезд мастера', f'{d["lead"]} Тел. {PHONE_LOCAL}.', body, url,
                        [ld_svc(d["h1"], d["lead"], url), ld_faq(faq)], crumbs=[(url, d["h1"].replace(" в Алматы", ""))], og_title=d["h1"]))

def build_districts():
    body = f'''{ph("Ремонт техники по районам Алматы", "Мастер выезжает во все районы города. Выберите свой — на странице частые неисправности и вызов мастера.")}
{sec("Районы", districts_html())}{sec("Что ремонтируем", dev_cards(), "", alt=True)}{band()}'''
    write("/rayony/", page("/rayony/", "Ремонт холодильников и стиральных машин по районам Алматы", f"Выезд мастера по ремонту холодильников, стиральных машин и морозильников во все районы Алматы. Тел. {PHONE_LOCAL}.", body, "/rayony/", crumbs=[("/rayony/", "Районы")], og_title="Ремонт техники по районам Алматы"))
    for s, n, inn, micro in DISTRICTS:
        url = f"/rayony/{s}/"
        mt = f" ({', '.join(micro)})" if micro else ""
        h1 = f"Ремонт холодильников и стиральных машин {inn}"
        lead = f"Мастер выезжает на дом {inn}{mt}: ремонт холодильников, стиральных машин и морозильников."
        fq = [(f"Вы выезжаете {inn}?", f"Да, мастер выезжает на дом {inn} Алматы{mt}."),
              ("Как вызвать мастера?", f"Позвоните {PHONE_LOCAL} или напишите в WhatsApp: техника, марка, что случилось и адрес."), FAQ[1]]
        body = f'''{ph(h1, lead, wa_text=f"Здравствуйте! Нужен ремонт техники. Район: {n}.", district=n)}
{sec(f"Что ремонтируем {inn}", dev_cards())}
{sec("Как проходит ремонт", steps(), "", alt=True)}
{sec("Вопросы", faq_html(fq))}
{sec("Другие районы", districts_html(cur=s), "", alt=True)}{band(f"Мастер {inn}")}'''
        write(url, page(url, f"Ремонт холодильников и стиральных машин {inn} Алматы", f"{lead} Тел. {PHONE_LOCAL}.", body, "/rayony/",
                        [ld_svc(h1, lead, url, {"@type": "AdministrativeArea", "name": f"{n} район, Алматы"}), ld_faq(fq)],
                        crumbs=[("/rayony/", "Районы"), (url, f"{n} район")], og_title=f"Ремонт техники: {n} район"))

def build_misc():
    allfaq = FAQ + [q for d in DEVICES for q in d["faq"]]
    body = f'''{ph("Вопросы о ремонте техники", "Ответы на частые вопросы о ремонте холодильников, стиральных машин и морозильников в Алматы.")}
{sec("Частые вопросы", faq_html(allfaq))}{sec("Что сказать при звонке", call_info(), "", alt=True)}{band()}'''
    write("/voprosy/", page("/voprosy/", "Вопросы о ремонте холодильников и стиральных машин — Алматы", "Как вызвать мастера, сколько стоит ремонт, что делать, если холодильник не морозит или стиральная машина не сливает воду.", body, "/voprosy/", [ld_faq(allfaq)], crumbs=[("/voprosy/", "Вопросы")], og_title="Вопросы о ремонте техники"))
    rows = f'<li><span>Телефон</span><a href="tel:{TEL}" data-ev="call">{PHONE_LOCAL}</a></li><li><span>WhatsApp</span><a href="{WA_URL()}" target="_blank" rel="noopener" data-ev="wa">{PHONE_LOCAL}</a></li>'
    if INSTAGRAM: rows += f'<li><span>Instagram</span><a href="{INSTAGRAM}" target="_blank" rel="noopener">{INSTAGRAM.rstrip("/").split("/")[-1]}</a></li>'
    if HOURS: rows += f"<li><span>Режим работы</span><b>{HOURS}</b></li>"
    rows += "<li><span>Где работаем</span><b>Все районы Алматы</b></li>"
    body = f'''{ph("Контакты", "Позвоните или напишите в WhatsApp — согласуем время выезда мастера.")}
{sec("Связь", f'<ul class="ct">{rows}</ul>')}{sec("Что сказать при звонке", call_info(), "", alt=True)}{sec("Районы выезда", districts_html())}'''
    write("/kontakty/", page("/kontakty/", f"Контакты — ремонт техники в Алматы, {PHONE_LOCAL}", f"Ремонт холодильников и стиральных машин в Алматы: {PHONE_LOCAL}, WhatsApp. Выезд во все районы.", body, "/kontakty/", crumbs=[("/kontakty/", "Контакты")], og_title="Контакты"))
    S = [("Какие данные мы получаем", "Сайт не собирает персональные данные через формы. Если вы звоните или пишете в WhatsApp, мы видим ваш номер и сообщения, которые вы отправляете."),
         ("Онлайн-помощник", "Вопросы, которые вы задаёте в чате, обрабатываются сервисом искусственного интеллекта, чтобы сформировать ответ. Не указывайте в чате лишних личных данных."),
         ("Зачем", "Чтобы связаться с вами, уточнить детали ремонта и выполнить заказ."),
         ("Аналитика", "Сайт может использовать сервисы веб-аналитики Google, которые собирают обезличенные данные о посещениях и нажатиях."),
         ("Передача третьим лицам", "Мы не передаём ваши данные третьим лицам, кроме случаев, предусмотренных законодательством Республики Казахстан."),
         ("Обращения", f"По вопросам обработки данных: {PHONE_LOCAL}.")]
    body = f'''<section class="ph ph-s"><div class="wrap"><!--CRUMBS--><h1>Политика конфиденциальности</h1></div></section>
<section class="sec"><div class="wrap prose">{"".join(f"<h2>{h}</h2><p>{t}</p>" for h, t in S)}</div></section>'''
    write("/politika/", page("/politika/", "Политика конфиденциальности", f"Политика обработки данных посетителей сайта {DOMAIN}.", body, crumbs=[("/politika/", "Политика конфиденциальности")]))
    body = f'''<section class="ph ph-s"><div class="wrap"><h1>Страница не найдена</h1><p class="ph-404">Возможно, она была перемещена. Выберите технику или позвоните мастеру.</p>{cta()}</div></section>{sec("Что ремонтируем", dev_cards())}'''
    write("/404/", page("/404/", "Страница не найдена", "Страница не найдена.", body).replace('content="index,follow,max-image-preview:large"', 'content="noindex"'))

def build_meta():
    urls = list(OG)
    sm = "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{'1.0' if u == '/' else '0.9' if u.startswith('/remont') else '0.7'}</priority></url>\n" for u in urls)
    (DIST / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}</urlset>\n', encoding="utf-8")
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "Bingbot", "YandexBot"]
    (DIST / "robots.txt").write_text("User-agent: *\nAllow: /\nDisallow: /api/\n\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"Sitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    ll = [f"# {BRAND} — Алматы", "", f"> {LEAD}", "", "## Главное", "- Город: Алматы, выезд мастера на дом во все районы",
          f"- Телефон и WhatsApp: {PHONE_LOCAL} ({PHONE}), https://wa.me/{WA}", "- Стоимость: зависит от неисправности; мастер называет её после диагностики, до начала ремонта", ""]
    for d in DEVICES:
        ll += [f"## [{d['h1']}]({SITE}/{d['slug']}/)", f"- {d['lead']}", "- Типы: " + ", ".join(d["types"]), "- Неисправности: " + "; ".join(d["faults"]), ""]
    ll += ["## Районы выезда"] + [f"- [{n} район]({SITE}/rayony/{s}/)" + (f": {', '.join(m)}" if m else "") for s, n, _, m in DISTRICTS]
    ll += ["", "## Марки", "- " + ", ".join(BRANDS) + " и другие", "", "## Частые вопросы"] + [f"- {q} {a}" for q, a in FAQ]
    (DIST / "llms.txt").write_text("\n".join(ll) + "\n", encoding="utf-8")
    (DIST / "site.webmanifest").write_text(json.dumps({"name": f"{BRAND} — Алматы", "short_name": BRAND, "start_url": "/", "display": "browser", "background_color": "#f3f6fb", "theme_color": "#1446d8",
        "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False), encoding="utf-8")
    (ROOT / "src" / "og_list.json").write_text(json.dumps(OG, ensure_ascii=False, indent=1), encoding="utf-8")

def build_assets():
    shutil.copytree(ROOT / "assets", DIST / "assets", dirs_exist_ok=True)
    shutil.copy(ROOT / "src" / "app.js", DIST / "assets" / "app.js")
    if (ROOT / "images").exists(): shutil.copytree(ROOT / "images", DIST / "images", dirs_exist_ok=True)
    for f in ("favicon.ico", "icon-192.png", "icon-512.png", "apple-touch-icon.png"):
        if (ROOT / "assets" / f).exists(): shutil.copy(ROOT / "assets" / f, DIST / f)

if __name__ == "__main__":
    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir()
    build_assets(); build_home(); build_devices(); build_districts(); build_misc(); build_meta()
    print("pages:", len(OG) + 1)
