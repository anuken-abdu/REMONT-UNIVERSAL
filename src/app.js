/* Ремонт техники, Алматы: меню, «назад/наверх», подбор неисправности, онлайн-помощник, учёт звонков и WhatsApp в Google Ads */
(function () {
  "use strict";
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var CFG = window.RT || {}, body = document.body;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var PH = CFG.phone || "", WAN = CFG.wa || "";
  function waLink(t) { return "https://wa.me/" + WAN + "?text=" + encodeURIComponent(t); }

  /* ---------- меню ---------- */
  var burger = $(".burger");
  function setNav(o) { body.classList.toggle("nav-open", o); if (burger) burger.setAttribute("aria-expanded", o ? "true" : "false"); }
  if (burger) burger.addEventListener("click", function () { setNav(!body.classList.contains("nav-open")); });
  $$(".nav a").forEach(function (a) { a.addEventListener("click", function () { setNav(false); }); });
  window.addEventListener("resize", function () { if (window.innerWidth >= 1100) setNav(false); });

  /* ---------- конверсии: звонок и WhatsApp ---------- */
  var ADS = CFG.ads || [], last = {};
  function conv(ev) {
    if (!window.gtag) return;
    var now = Date.now(); if (last[ev] && now - last[ev] < 1500) return; last[ev] = now;
    try {
      window.gtag("event", ev === "call" ? "phone_click" : "whatsapp_click");
      var label = ev === "call" ? ADS[1] : ADS[2];
      if (ADS[0] && label) window.gtag("event", "conversion", { send_to: ADS[0] + "/" + label });
    } catch (e) {}
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("[data-ev]"); if (a) conv(a.getAttribute("data-ev"));
  });

  /* ---------- назад / наверх ---------- */
  var bBack = $(".fl-back"), bTop = $(".fl-top");
  if (bBack) {
    bBack.hidden = location.pathname === "/";
    bBack.addEventListener("click", function () {
      var same = false; try { same = document.referrer && new URL(document.referrer).host === location.host; } catch (e) {}
      if (same && history.length > 1) { history.back(); return; }
      var cr = $$(".crumbs a"); location.href = cr.length ? cr[cr.length - 1].getAttribute("href") : "/";
    });
  }
  if (bTop) bTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });
  var tick = false;
  function onScroll() { tick = false; if (bTop) bTop.hidden = (window.pageYOffset || document.documentElement.scrollTop) < 500; }
  window.addEventListener("scroll", function () { if (!tick) { tick = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  /* ---------- подбор неисправности → сообщение в WhatsApp ---------- */
  var pk = $("#pk");
  if (pk) {
    var dSel = $("#pkD", pk), bIn = $("#pkB", pk);
    $$(".pk-t", pk).forEach(function (t) {
      t.addEventListener("click", function () {
        var k = t.getAttribute("data-dev");
        $$(".pk-t", pk).forEach(function (x) { var on = x === t; x.classList.toggle("on", on); x.setAttribute("aria-selected", on ? "true" : "false"); });
        $$(".pk-g", pk).forEach(function (g) { g.hidden = g.getAttribute("data-dev") !== k; });
      });
    });
    // текст собирается в момент нажатия — с учётом района и марки
    $$(".pk-c", pk).forEach(function (c) {
      c.addEventListener("click", function () {
        var g = c.closest(".pk-g"), acc = g.getAttribute("data-acc"), f = c.getAttribute("data-fault");
        var brand = (bIn.value || "").trim().slice(0, 40), dist = dSel.value;
        var t = "Здравствуйте! Нужен ремонт: " + acc + (brand ? " " + brand : "") + "." + (f ? " Проблема: " + f.toLowerCase() + "." : "") + (dist ? " Район: " + dist + "." : "");
        c.href = waLink(t);
      });
    });
  }

  /* ================= онлайн-помощник ================= */
  var chat = $("#chat"), fab = $(".fl-chat"), cb = $("#chatB"), cq = $("#chatQ"), cf = $("#chatF"), ci = $("#chatI"), waBtn = $("#chatWa");
  if (!chat) return;
  var hist = [], started = false, busy = false, apiOk = true;

  function openChat() {
    chat.hidden = false; body.classList.add("chat-open"); fab.setAttribute("aria-expanded", "true");
    if (!started) { started = true; say("Здравствуйте! Я онлайн-помощник мастера по ремонту техники в Алматы. Что сломалось — холодильник, стиральная машина или морозильник? Опишите, что происходит.", QUICK); }
    if (window.innerWidth > 767) setTimeout(function () { ci.focus(); }, 50);
  }
  function closeChat() { if (chat.hidden) return; chat.hidden = true; body.classList.remove("chat-open"); fab.setAttribute("aria-expanded", "false"); fab.focus(); }
  fab.addEventListener("click", function () { chat.hidden ? openChat() : closeChat(); });
  $(".chat-x").addEventListener("click", closeChat);
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { setNav(false); closeChat(); } });

  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  var phRe = new RegExp("(" + PH.replace(/[.*+?^${}()|[\]\\]/g, "\\$&").replace(/ /g, "\\s?") + "|\\+7 771 274 70 92)", "g");
  function linkify(s) {
    return esc(s).replace(/(\/(?:remont-[a-z\-]+|rayony|voprosy|kontakty)\/[a-z\-\/]*)/g, '<a href="$1">$1</a>')
      .replace(phRe, '<a href="tel:' + CFG.tel + '" data-ev="call">$1</a>');
  }
  function add(role, text) {
    var m = document.createElement("div"); m.className = "msg " + (role === "u" ? "msg-u" : "msg-b");
    m.innerHTML = role === "u" ? esc(text) : linkify(text); cb.appendChild(m); cb.scrollTop = cb.scrollHeight;
  }
  function dots() { var t = document.createElement("div"); t.className = "msg msg-b dots"; t.innerHTML = "<i></i><i></i><i></i>"; cb.appendChild(t); cb.scrollTop = cb.scrollHeight; return t; }
  function say(text, quick) {
    var t = dots();
    setTimeout(function () { t.remove(); add("b", text); hist.push({ role: "assistant", content: text }); setQuick(quick); updWa(); }, Math.min(1200, 350 + text.length * 4));
  }
  var QUICK = ["Холодильник не морозит", "Стиралка не сливает", "Сколько стоит?", "Приедете в мой район?", "Какие марки?"];
  function setQuick(list) {
    cq.innerHTML = "";
    (list || QUICK).forEach(function (q) { var b = document.createElement("button"); b.type = "button"; b.textContent = q; b.addEventListener("click", function () { ask(q); }); cq.appendChild(b); });
  }
  // кнопка WhatsApp в чате переносит суть разговора мастеру
  function updWa() {
    var u = hist.filter(function (h) { return h.role === "user"; }).map(function (h) { return h.content; }).join(". ");
    waBtn.href = waLink("Здравствуйте! Нужен ремонт техники." + (u ? " " + u.slice(0, 600) : ""));
  }
  function ask(text) {
    text = String(text || "").trim(); if (!text || busy) return;
    add("u", text); hist.push({ role: "user", content: text }); cq.innerHTML = ""; updWa();
    var local = kb(text);
    if (local && local.instant) return say(local.a, local.q);
    if (!apiOk) return say((local || FALLBACK).a, (local || FALLBACK).q);
    busy = true; var t = dots();
    var ctrl = window.AbortController ? new AbortController() : null, timer = setTimeout(function () { if (ctrl) ctrl.abort(); }, 12000);
    fetch("/api/chat", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ messages: hist.slice(-12), page: location.pathname }), signal: ctrl ? ctrl.signal : undefined })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (j) { if (!j.reply) throw new Error("empty"); clearTimeout(timer); t.remove(); add("b", j.reply); hist.push({ role: "assistant", content: j.reply }); setQuick(local && local.q); updWa(); busy = false; })
      .catch(function () { clearTimeout(timer); t.remove(); apiOk = false; busy = false; var r = local || FALLBACK; say(r.a, r.q); });
  }
  cf.addEventListener("submit", function (e) { e.preventDefault(); var v = ci.value; ci.value = ""; ask(v); });

  /* ---------- база ответов (работает и без ИИ) ---------- */
  var CALL = "Позвоните " + PH + " или нажмите «В WhatsApp» под чатом — согласуем время выезда.";
  var FALLBACK = { a: "Точно скажет мастер после диагностики. " + CALL + " Назовите технику, марку, что случилось и район.", q: ["Сколько стоит?", "Что сказать при звонке?"] };
  var DIST = (CFG.districts || []).join(", ");
  var KB = [
    { k: ["привет", "здравств", "добрый", "салем", "сәлем"], instant: 1, a: "Здравствуйте! Что случилось с техникой? Напишите, что сломалось и марку." },
    { k: ["спасибо", "рахмет"], instant: 1, a: "Пожалуйста! Если нужен мастер — " + CALL },
    { k: ["бот", "робот", "живой", "человек"], instant: 1, a: "Я онлайн-помощник сайта. Ремонт делает мастер — " + CALL },
    { pri: 2, k: ["холодильн", "не морозит", "не холодит", "плохо холод", "no frost", "ноу фрост", "шуба", "намерза", "лед ", "лёд"], a: "Ремонтируем холодильники на дому: не морозит, работает без остановки, намерзает лёд, течёт вода, шумит. Не размораживайте и не включайте-выключайте его много раз — позвоните " + PH + " или напишите марку и что происходит в WhatsApp. Подробнее — /remont-holodilnikov/.", q: ["Сколько стоит?", "Приедете в мой район?"] },
    { pri: 2, k: ["стирал", "стиралк", "не слива", "не отжима", "не греет", "барабан", "не набира", "люк", "дверца", "прыгает"], a: "Ремонтируем стиральные машины на дому: не сливает, не отжимает, не греет, не крутится барабан, течёт, ошибка на дисплее. Отключите машину от сети и не открывайте дверцу, если внутри вода. Позвоните " + PH + " — подробнее /remont-stiralnyh-mashin/.", q: ["Сколько стоит?", "Ошибка на дисплее"] },
    { pri: 2, k: ["морозильн", "морозилк", "ларь", "лари", "витрин", "камера"], a: "Ремонтируем морозильники для дома и бизнеса: шкафы, лари, витрины. Пока ждёте мастера, держите дверь закрытой — продукты дольше останутся замороженными. Звоните " + PH + ". Подробнее — /remont-morozilnikov/.", q: ["Сколько стоит?", "Для магазина"] },
    { k: ["стоим", "цена", "сколько стоит", "почем", "почём", "прайс", "тенге", "₸", "дорого", "диагностик"], a: "Стоимость зависит от неисправности и нужных запчастей. Мастер называет её после диагностики и до начала ремонта — без сюрпризов. Уточнить: " + PH + ".", q: ["Что сказать при звонке?", "Приедете в мой район?"] },
    { k: ["ошибк", "код", "дисплей", "мигает", "e1", "e2", "f0", "he", "oe", "ue"], a: "Сфотографируйте дисплей с кодом ошибки и отправьте в WhatsApp вместе с маркой техники — мастер подскажет, в чём может быть причина, и согласует выезд.", q: ["Сколько стоит?"] },
    { k: ["район", "приед", "выезж", "выезд", "адрес", "на дом", "алматы"].concat((CFG.districts || []).map(function (d) { return d.toLowerCase().slice(0, 6); })).concat(["аксай", "самал", "орбит", "шанырак", "алгабас", "мамыр", "таугуль", "коктем", "шугыла", "калкаман", "айнабулак"]), a: "Да, мастер выезжает на дом во все районы Алматы: " + DIST + ". Назовите адрес при звонке — согласуем время: " + PH + ". Список районов — /rayony/.", q: ["Сколько стоит?", "Как быстро приедете?"] },
    { k: ["быстро", "когда приед", "сегодня", "сейчас", "срочно", "завтра"], a: "Время выезда согласуем при звонке или в WhatsApp. Звоните: " + PH + ".", q: ["Сколько стоит?"] },
    { k: ["марк", "samsung", "самсунг", "lg", "bosch", "бош", "indesit", "индезит", "atlant", "атлант", "beko", "веко", "беко", "electrolux", "haier", "ariston", "аристон", "whirlpool", "candy", "siemens"], a: "Ремонтируем технику популярных марок: Samsung, LG, Bosch, Indesit, Atlant, Beko, Electrolux, Haier, Ariston, Whirlpool, Candy, Siemens и другие. Назовите модель при звонке: " + PH + "." },
    { k: ["магазин", "кафе", "бизнес", "офис", "ресторан", "торгов"], a: "Да, ремонтируем холодильники и морозильники для магазинов, кафе и офисов. Звоните " + PH + " — назовите тип оборудования и марку." },
    { k: ["гарант"], a: "Условия гарантии на ремонт уточните у мастера: " + PH + "." },
    { k: ["оплат", "kaspi", "каспи", "наличн", "перевод"], a: "Способ оплаты уточните у мастера при звонке: " + PH + "." },
    { k: ["что сказать", "что нужно", "какие данные", "что сообщить"], a: "Скажите три вещи: какая техника и марка (если есть — модель), что случилось и когда началось, и ваш район с адресом. Так мастер быстрее поймёт причину и возьмёт нужные запчасти." },
    { k: ["посудомо", "микроволн", "плит", "духов", "кондиционер", "телевиз", "пылесос", "бойлер", "водонагрев"], a: "На сайте — ремонт холодильников, стиральных машин и морозильников. Про другую технику уточните у мастера: " + PH + "." },
    { k: ["режим", "график", "выходн", "до скольки", "время работ"], a: "Режим работы уточните по телефону " + PH + " или в WhatsApp." },
    { k: ["номер", "телефон", "контакт", "whatsapp", "ватсап", "позвон"], instant: 1, a: "Телефон и WhatsApp: " + PH + ". Кнопки «Позвонить» и «В WhatsApp» — прямо под чатом." },
  ];
  function kb(text) {
    var t = " " + text.toLowerCase().replace(/ё/g, "е") + " ", best = null, sc = 0;
    KB.forEach(function (it) { var s = 0; it.k.forEach(function (k) { if (t.indexOf(k.replace(/ё/g, "е")) > -1) s += k.length; }); s *= it.pri || 1; if (s > sc) { sc = s; best = it; } });
    return best ? { a: best.a, q: best.q, instant: best.instant } : null;
  }
})();
