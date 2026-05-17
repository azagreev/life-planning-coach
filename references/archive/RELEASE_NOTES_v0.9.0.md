# Release Notes v0.9.0

## Мобильная адаптация + Habit Tracker + Reward Audit

**Дата релиза:** 2026-05-18

---

### 🎯 Главное

- **Habit Tracker / Dashboard Streaks** — визуализация цепочек выполнения привычек прямо в дашборде (4 категории: Привычки, Экраны, Сахар, Фокус).
- **Mobile Dashboard** — адаптивная вёрстка дашборда для мобильных устройств (375px+), touch-friendly интерфейс.
- **Reward Audit (Grayscale Guide)** — killer feature на основе научных исследований: рекомендация включить grayscale-режим на телефоне для снижения screen time на 20–38 минут в день (Holte 2021, NYT 2025).
- **5-Minute Micro-Sessions** — быстрые чек-ины для режима нехватки времени (эмоция → 1 действие ≤30 сек).
- **Quick Decision Protocol** — 2–3 вопроса для принятия решения «здесь и сейчас» с адаптацией под Communication Style.

---

### 📊 Статистика релиза

- **Новых reference-файлов:** 3 (`micro_sessions.md`, `quick_decision.md`, `reward_audit.md`)
- **Изменённых файлов:** `life-planning-dashboard.html`, `SKILL.md`, `README.md`, `CHANGELOG.md`
- **Новых тестов:** 26 (всего 121 тест, 3 skipped)
- **Размер ZIP:** 570K

---

### 🔬 Научная база новых фич

- **Grayscale mode:** Holte & Ferraro (2021) –37.9 мин/день; Wickord (2023) репликация; Myers (2022) уменьшение allure + улучшение сна; NYT (2025) –40%.
- **Reward Audit:** Rada (2005), Avena (2008), Lembke (Stanford, 2021), Kushlev (2025).
- **Micro-Sessions:** Tiny Habits (Fogg, 2019) — действия ≤30 секунд.

---

### ⚠️ Известные ограничения

- Dashboard streaks используют sample data (inline JS). Персистентность данных между сессиями — через Google Drive wiki (opt-in).
- Mobile responsive CSS покрывает breakpoint ≤768px. Планшеты (768–1024px) используют desktop layout.
- Reward Audit — conversational-only, не требует daily tracking (в отличие от standalone app PRD).
