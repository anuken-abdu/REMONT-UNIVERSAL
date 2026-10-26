# -*- coding: utf-8 -*-
"""Векторные иллюстрации техники (общие для сайта и баннеров)."""
DEF = '''<defs>
<linearGradient id="a-st" x1="0" x2="1"><stop offset="0" stop-color="#e9edf3"/><stop offset=".45" stop-color="#ffffff"/><stop offset="1" stop-color="#d9dfe8"/></linearGradient>
<linearGradient id="a-st2" x1="0" x2="1"><stop offset="0" stop-color="#dfe5ee"/><stop offset=".5" stop-color="#f7f9fc"/><stop offset="1" stop-color="#cfd7e3"/></linearGradient>
<linearGradient id="a-hd" x1="0" x2="1"><stop offset="0" stop-color="#9aa6b8"/><stop offset=".5" stop-color="#e8edf4"/><stop offset="1" stop-color="#8793a6"/></linearGradient>
<radialGradient id="a-gl" cx=".38" cy=".35" r=".75"><stop offset="0" stop-color="#bfe0ff"/><stop offset=".55" stop-color="#5b8fd9"/><stop offset="1" stop-color="#1d3f7a"/></radialGradient>
<linearGradient id="a-bl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a5cf0"/><stop offset="1" stop-color="#1238b0"/></linearGradient>
<filter id="a-sh" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="18" stdDeviation="18" flood-color="#0d1b33" flood-opacity=".22"/></filter>
</defs>'''

FRIDGE = '''<g filter="url(#a-sh)"><rect x="0" y="0" width="300" height="540" rx="22" fill="url(#a-st)" stroke="#b9c3d2" stroke-width="2"/>
<rect x="0" y="178" width="300" height="5" fill="#b9c3d2"/>
<rect x="28" y="40" width="12" height="104" rx="6" fill="url(#a-hd)"/><rect x="28" y="214" width="12" height="150" rx="6" fill="url(#a-hd)"/>
<rect x="196" y="40" width="76" height="40" rx="8" fill="#0d1b33"/><text x="234" y="68" text-anchor="middle" font-family="Manrope,sans-serif" font-weight="700" font-size="22" fill="#5fd0ff">-18°</text>
<rect x="196" y="88" width="76" height="6" rx="3" fill="#cfd7e3"/><path d="M230 16 L238 16" stroke="#b9c3d2" stroke-width="3" stroke-linecap="round"/>
<rect x="60" y="20" width="16" height="500" fill="#fff" opacity=".55"/>
<rect x="20" y="540" width="40" height="14" rx="4" fill="#5b6678"/><rect x="240" y="540" width="40" height="14" rx="4" fill="#5b6678"/></g>'''
WASHER = '''<g filter="url(#a-sh)"><rect x="0" y="0" width="320" height="360" rx="22" fill="url(#a-st)" stroke="#b9c3d2" stroke-width="2"/>
<rect x="0" y="0" width="320" height="70" rx="22" fill="url(#a-st2)"/><rect x="0" y="66" width="320" height="4" fill="#b9c3d2"/>
<rect x="22" y="20" width="70" height="30" rx="6" fill="#dfe5ee" stroke="#b9c3d2"/><rect x="132" y="18" width="88" height="34" rx="7" fill="#0d1b33"/>
<text x="176" y="42" text-anchor="middle" font-family="Manrope,sans-serif" font-weight="700" font-size="20" fill="#5fd0ff">1:25</text>
<circle cx="268" cy="35" r="20" fill="url(#a-hd)" stroke="#8793a6"/><circle cx="268" cy="35" r="6" fill="#5b6678"/>
<circle cx="160" cy="210" r="112" fill="#cfd7e3" stroke="#9aa6b8" stroke-width="3"/><circle cx="160" cy="210" r="94" fill="#7d8899"/>
<circle cx="160" cy="210" r="84" fill="url(#a-gl)"/>
<path d="M98 228c22-30 58-6 84-30s44-6 52 10c-10 44-50 70-92 64-24-4-40-22-44-44z" fill="#ffffff" opacity=".35"/>
<path d="M112 168a62 62 0 0 1 56-28" stroke="#fff" stroke-width="8" stroke-linecap="round" fill="none" opacity=".7"/>
<rect x="266" y="190" width="10" height="40" rx="5" fill="url(#a-hd)"/></g>'''
FREEZER = '''<g filter="url(#a-sh)"><rect x="0" y="40" width="460" height="220" rx="20" fill="url(#a-st)" stroke="#b9c3d2" stroke-width="2"/>
<rect x="-6" y="0" width="472" height="56" rx="16" fill="url(#a-st2)" stroke="#b9c3d2" stroke-width="2"/>
<rect x="170" y="56" width="120" height="16" rx="8" fill="url(#a-hd)"/>
<circle cx="40" cy="96" r="7" fill="#2fd47f"/><circle cx="64" cy="96" r="7" fill="#ffb020"/><circle cx="88" cy="96" r="7" fill="#cfd7e3"/>
<g stroke="#b9c3d2" stroke-width="5" stroke-linecap="round"><path d="M340 200h80M340 216h80M340 232h80"/></g>
<rect x="40" y="30" width="380" height="10" rx="5" fill="#fff" opacity=".7"/>
<rect x="24" y="260" width="34" height="12" rx="4" fill="#5b6678"/><rect x="402" y="260" width="34" height="12" rx="4" fill="#5b6678"/></g>'''
WRENCH = '''<g filter="url(#a-sh)"><path d="M0 0a46 46 0 0 0 58 58l140 140a20 20 0 0 0 28-28L86 30A46 46 0 0 0 28-28l30 30-6 24-24 6z" fill="url(#a-hd)" stroke="#6e7a8d" stroke-width="2"/></g>'''
SCREW = '''<g filter="url(#a-sh)"><rect x="-14" y="0" width="28" height="96" rx="12" fill="url(#a-bl)"/><rect x="-14" y="22" width="28" height="6" fill="#0f2f8f" opacity=".5"/><rect x="-14" y="44" width="28" height="6" fill="#0f2f8f" opacity=".5"/>
<rect x="-5" y="94" width="10" height="110" fill="url(#a-hd)"/><path d="M-5 204h10l-2 16h-6z" fill="#6e7a8d"/></g>'''
METER = '''<g filter="url(#a-sh)"><rect x="0" y="0" width="120" height="190" rx="18" fill="#ffb020"/><rect x="12" y="12" width="96" height="166" rx="12" fill="#252f40"/>
<rect x="22" y="24" width="76" height="40" rx="6" fill="#c8f0d8"/><text x="60" y="53" text-anchor="middle" font-family="Manrope,sans-serif" font-weight="700" font-size="22" fill="#0d1b33">220</text>
<circle cx="60" cy="116" r="30" fill="#3a4659" stroke="#5b6678" stroke-width="3"/><path d="M60 116l18-16" stroke="#fff" stroke-width="5" stroke-linecap="round"/>
<circle cx="38" cy="162" r="7" fill="#e5484d"/><circle cx="82" cy="162" r="7" fill="#0d1b33" stroke="#5b6678"/></g>'''


VB = {"fridge": ("-12 -12 324 580", FRIDGE), "washer": ("-14 -12 348 396", WASHER), "freezer": ("-22 -12 504 300", FREEZER)}
def art(kind, cls="art"):
    if kind == "all":
        inner = f'<g transform="translate(20,16)">{FRIDGE}</g><g transform="translate(300,226) scale(.98)">{WASHER}</g>'
        return f'<svg class="{cls}" viewBox="0 0 640 600" aria-hidden="true" focusable="false">{inner}</svg>'
    vb, g = VB[kind]
    return f'<svg class="{cls}" viewBox="{vb}" aria-hidden="true" focusable="false">{g}</svg>'
def defs(): return f'<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">{DEF}</svg>'
