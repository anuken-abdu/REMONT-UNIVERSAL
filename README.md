# Ремонт техники — Алматы (сайт)

Статический сайт: генератор `src/build.py` → папка `dist/` (уже собрана). Хостинг — Vercel.

## Деплой
1. Залить весь проект в репозиторий GitHub → импортировать в Vercel (настройки уже в `vercel.json`).
2. Vercel → Settings → Environment Variables: `ANTHROPIC_API_KEY` — для умного ИИ-чата. Без ключа чат работает по встроенной базе ответов.
3. Подключить домен (с www) и указать его в `src/data.py` → `SITE`, пересобрать.

## Что поменять в `src/data.py` и пересобрать (`python3 src/build.py`)
- `BRAND`, `SITE` — название и домен (сейчас нейтральные).
- `HOURS` — режим работы (пусто = не выводится).
- `INSTAGRAM` — ссылка, если есть.
- `GA_ID`, `GADS_ID`, `GADS_CALL_LABEL`, `GADS_WA_LABEL` — теги Google и метки конверсий «Звонок» и «WhatsApp».
- `BRANDS` — марки техники.
После смены названия: `python3 src/render_brand.py`, затем снова `python3 src/build.py`.

## Фото
См. `images/README.txt`. Фото появятся в карточках после пересборки.
