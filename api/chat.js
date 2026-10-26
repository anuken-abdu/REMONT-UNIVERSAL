// Vercel Function: ИИ-помощник сайта ремонта техники в Алматы.
// Нужна переменная окружения ANTHROPIC_API_KEY (Vercel → Settings → Environment Variables).
// Без ключа функция отвечает 503, и чат на сайте автоматически отвечает по встроенной базе.
const MODEL = process.env.ANTHROPIC_MODEL || "claude-haiku-5-5";

const SYSTEM = `Ты — онлайн-помощник сайта мастера по ремонту бытовой техники в Алматы. Пишешь в чате на сайте.
Факты: ремонт на дому холодильников (однокамерные, двухкамерные, No Frost, встраиваемые, Side-by-Side), стиральных машин (фронтальные, вертикальные, встраиваемые, стирально-сушильные) и морозильников (шкафы, лари, витрины, в том числе для магазинов и кафе). Мастер выезжает на дом во все районы Алматы: Алмалинский, Ауэзовский, Бостандыкский, Медеуский, Жетысуский, Турксибский, Наурызбайский, Алатауский. Марки: Samsung, LG, Bosch, Indesit, Atlant, Beko, Electrolux, Haier, Ariston, Whirlpool, Candy, Siemens и другие.
Порядок: заявка по телефону или WhatsApp → выезд мастера и диагностика → мастер называет стоимость до начала работ → ремонт и проверка.
Телефон и WhatsApp: 8 771 274 70 92. Под чатом есть кнопки «Позвонить» и «В WhatsApp» (туда можно отправить фото ошибки на дисплее).
Страницы: /remont-holodilnikov/, /remont-stiralnyh-mashin/, /remont-morozilnikov/, /rayony/, /voprosy/, /kontakty/.
При звонке нужно сказать: технику и марку (модель), что случилось и когда началось, район и адрес.
Правила:
- Отвечай на языке посетителя (русский или казахский), коротко: 1–3 предложения, без markdown, списков и эмодзи.
- Цель — чтобы человек позвонил или написал в WhatsApp.
- Не называй цены, сроки выезда, режим работы, гарантии, скидки и способы оплаты — их уточняет мастер. Стоимость зависит от неисправности и запчастей, мастер называет её после диагностики.
- Можно дать простой безопасный совет до приезда мастера (отключить от сети, не открывать дверцу стиральной машины с водой, держать дверь морозильника закрытой, не включать-выключать холодильник много раз). Не давай инструкций по самостоятельной разборке, работе с электрикой и хладагентом.
- Не обещай ремонт другой техники — предложи уточнить у мастера.
- Если спрашивают, бот ли ты, честно скажи, что ты онлайн-помощник, а ремонт делает мастер.`;

const hits = new Map();
function limited(ip) {
  const now = Date.now(), arr = (hits.get(ip) || []).filter((t) => now - t < 600000);
  arr.push(now); hits.set(ip, arr); if (hits.size > 5000) hits.clear();
  return arr.length > 30;
}
module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") { res.status(405).json({ error: "method" }); return; }
  const key = process.env.ANTHROPIC_API_KEY;
  if (!key) { res.status(503).json({ error: "not_configured" }); return; }
  const ip = (req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "x";
  if (limited(ip)) { res.status(429).json({ error: "rate" }); return; }
  let body = req.body; if (typeof body === "string") { try { body = JSON.parse(body); } catch (e) { body = {}; } }
  const clean = [];
  for (const m of (Array.isArray(body && body.messages) ? body.messages : []).slice(-12)) {
    if (!m || (m.role !== "user" && m.role !== "assistant") || typeof m.content !== "string" || !m.content.trim()) continue;
    const x = { role: m.role, content: m.content.slice(0, 800) };
    if (!clean.length && x.role !== "user") continue;
    if (clean.length && clean[clean.length - 1].role === x.role) clean[clean.length - 1].content += "\n" + x.content; else clean.push(x);
  }
  if (!clean.length || clean[clean.length - 1].role !== "user") { res.status(400).json({ error: "bad_request" }); return; }
  try {
    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST", headers: { "content-type": "application/json", "x-api-key": key, "anthropic-version": "2023-06-01" },
      body: JSON.stringify({ model: MODEL, max_tokens: 300, system: SYSTEM + `\nСтраница посетителя: ${String(body.page || "/").slice(0, 100)}`, messages: clean }),
    });
    if (!r.ok) { res.status(502).json({ error: "upstream" }); return; }
    const j = await r.json();
    const reply = (j.content || []).filter((c) => c.type === "text").map((c) => c.text).join("\n").trim();
    if (!reply) { res.status(502).json({ error: "empty" }); return; }
    res.status(200).json({ reply });
  } catch (e) { res.status(502).json({ error: "fail" }); }
};
