# PRD: Reward Audit (Бюджет Дофамина / Cheap Dopamine Tracker)

**Версия:** 1.0
**Дата:** 17 мая 2026
**Автор:** Grok (на основе глубокого ресёрча для проекта life-planning-coach)
**Статус:** Готов к review и разработке
**Связанный GitHub:** https://github.com/azagreev/life-planning-coach

---

## 1. Executive Summary

**Фича:** Reward Audit (внутреннее название: «Бюджет Дофамина» или «Аудит наград»)

**Проблема:** Пользователи life-planning-coach ставят амбициозные цели, но ежедневно «крадут» у себя мотивацию через источники «дешёвого дофамина» (сахар, бесконечный скролл соцсетей, YouTube Shorts, игры, импульсивный шопинг и т.д.). Мозг получает лёгкие награды → снижается чувствительность к усилиям, необходимым для реальных достижений. Completion rate целей падает.

**Решение:** Встроенный модуль, который:
- Легко логирует источники cheap dopamine
- Автоматически рассчитывает **Dopamine Load Score**
- Показывает **прямую корреляцию** с % выполнения целей пользователя
- Даёт actionable insights и помогает управлять «reward budget»

**Уникальное ценностное предложение:**
Первый life-planning инструмент, который не просто блокирует или трекает привычки, а **прямо связывает управление дофамином с достижением долгосрочных целей** на основе научных данных.

**Приоритет:** Высокий (killer feature для retention и дифференциации).

---

## 2. Problem Statement

Современный пользователь (особенно в fintech/продуктовом discovery, как целевая аудитория) живёт в среде гиперстимуляции:
- Сахар и ультра-обработанные продукты → повторяющиеся выбросы дофамина в nucleus accumbens (аналогично наркотикам).
- Социальные сети и короткий контент → variable reward system (как слот-машины).
- Результат: толерантность, снижение мотивации («wanting»), ухудшение effort-based decision making, ниже completion rate целей.

**Данные из ресёрча (2025–2026):**
- Соцсети вызывают дофаминовые всплески, сравнимые с зависимостью (Stanford, Lembke «Dopamine Nation»; PMC 2025).
- Высокое экранное время коррелирует со снижением внимания, продуктивности и completion rate (SDSU, Georgetown/Kushlev 2025).
- Хроническое потребление сахара приводит к даунрегуляции дофаминовых рецепторов и снижению импульс-контроля (Avena 2008, Jacques 2019, Rada 2005).
- «Dopamine detox» как тренд упрощён, но снижение высокостимулирующих активностей реально улучшает фокус и саморегуляцию (обзоры 2024–2026).

**Боль пользователя:**
«Я ставлю цели, но к вечеру мотивация пропадает. Я знаю, что скролл и сладкое виноваты, но не вижу точной связи и не знаю, как это исправить системно.»

---

## 3. Goals & Success Metrics

**Бизнес-цели:**
- Увеличить средний completion rate целей на 15–25% у активных пользователей модуля (через A/B тест).
- Повысить retention на 30+ дней на 20%.
- Сделать фичу основной причиной «вау-эффекта» в отзывах.

**Продуктовые метрики (KPI):**
- % пользователей, логирующих ≥4 раза в неделю → цель >35% через 3 месяца.
- Корреляция между снижением Dopamine Load и ростом completion rate (измеряется внутри продукта).
- NPS модуля ≥ +40.
- Время до первого инсайта < 7 дней.

**Качественные цели:**
- Пользователь понимает: «Мой дофамин-бюджет напрямую влияет на то, достигаю ли я целей».

---

## 4. Research & Scientific Backing (с гиперссылками)

### Ключевые исследования по сахару и дофамину
- **Rada et al. (2005)** — Daily bingeing on sugar repeatedly releases dopamine in the accumbens shell.
  https://pubmed.ncbi.nlm.nih.gov/15987666/
  (Повторяющийся выброс дофамина до 130% baseline даже после 21 дня.)

- **Avena, Rada, Hoebel (2008)** — Evidence for sugar addiction: behavioral and neurochemical effects... (2165+ цитирований).
  https://pubmed.ncbi.nlm.nih.gov/17617461/
  (Bingeing, withdrawal, craving, cross-sensitization, изменения D1/D2 рецепторов.)

- **Jacques et al. (2019)** — The impact of sugar consumption on stress driven... (нейропластичность, снижение импульс-контроля).
  https://pubmed.ncbi.nlm.nih.gov/31125634/

- **University of Michigan (2020)** — High-sugar diet dampens dopamine release → overeating.
  https://news.umich.edu/high-sugar-diet-dampens-release-of-dopamine-triggering-overeating/

### По социальным сетям, экранам и мотивации
- **Stanford / Anna Lembke «Dopamine Nation» (2021, актуально)** — Соцсети как современный «наркотик» через variable rewards.
  https://med.stanford.edu/news/insights/2021/10/addictive-potential-of-social-media-explained.html

- **Kushlev et al. (2025, PNAS Nexus)** — Даже небольшая digital detox улучшает внимание и снижает стресс.
  https://academic.oup.com/pnasnexus/article/4/2/pgaf017/8016017

- **SDSU study (2022–2025)** — Самомониторинг экранного времени + goal-setting повышает продуктивность.
  https://business.sdsu.edu/news/2022/10/screentime-research-v2

- PMC 2025 статьи: Social Media Algorithms and Teen Addiction; Modern Day High: The Neurocognitive Impact... (дофаминовые пути, зависимость, снижение внимания).

### Обзоры по dopamine detox (нюансы 2024–2026)
- The Scientist (2024): Debunking the Dopamine Detox Trend.
  https://www.the-scientist.com/debunking-the-dopamine-detox-trend-72036
  (Не «reset», но снижение стимуляции помогает.)

- Northwestern University (2025): Dopamine signals respond differently — концепция слишком simplistic.
  https://www.eurekalert.org/news-releases/1080824

- Обзор 2024 (PMC): Люди, практикующие dopamine-fasting-like подходы, отмечают лучший фокус и меньше импульсивности.

**Вывод ресёрча:** Гипотеза подтверждена косвенно, но сильно. Модуль должен использовать термин «Reward Management / Бюджет наград», а не чистый «dopamine detox», чтобы избежать критики oversimplification.

---

## 5. Competitive Landscape (2025–2026)

**Прямые конкуренты по dopamine detox:**
- **Elqi – The Dopamine App** (iOS): Трекинг dopamine levels по usage, блокировка. Нет сахара, нет корреляции с целями. https://apps.apple.com/be/app/elqi-the-dopamine-app/id6476441509
- **Dopy – Dopamine Detox App**: Pomodoro + привычки + ограничения.
- **Opal, one sec, BePresent**: Сильная блокировка + геймификация. BePresent заменяет scrolling dopamine на achievement dopamine.
- **Liven**: Mood + habits + AI, позиционируется как detox (много критики «scam» в 2026).

**Общие habit trackers:**
- Habitica (лучшая геймификация)
- Habitify, Streaks, TickTick, ClickUp

**Gap & Opportunity:**
- Никто не делает **единую категорию «Cheap Dopamine Sources»** (сахар + экраны + др.) + **прямую корреляцию с completion rate реальных жизненных целей**.
- Твой продукт выигрывает за счёт интеграции в life-planning flow.

**Стратегия дифференциации:** Awareness + Correlation + Planning Integration (не только блокировка).

---

## 6. User Personas & Stories

**Persona 1: Андрей, 32, Product Manager (финтех, discovery в Узбекистане/Казахстане и т.д.)**
- Ставит 5–7 целей в квартал.
- Проводит 3–4 часа в день в соцсетях + ест сладкое при стрессе.
- Жалуется: «К концу недели выполнено 40% вместо 80%».

**User Story (MVP):**
Как пользователь, я хочу быстро залогировать «сколько сладкого и скролла было сегодня», чтобы через неделю увидеть: «В дни с высоким Dopamine Load я выполняю на 18% меньше целей» и принять решение снизить бюджет.

**Persona 2:** Фаундер / ambitious professional 28–40 лет, живёт в большом городе (Москва и аналоги), высокий стресс, хочет максимальной продуктивности.

---

## 7. Functional Requirements (детально)

### 7.1 Логирование (MVP)
- Экран «Сегодняшний Dopamine Load» (1-tap + слайдеры).
- Категории (минимум 5):
  1. Сахар / сладкое / фастфуд (порции или Low/Med/High)
  2. Соцсети (минуты или интенсивность)
  3. YouTube / Shorts / Reels
  4. Мобильные игры / развлечения
  5. Импульсивный шопинг / другие apps
- Быстрые пресеты: «Обычный день», «Высокий допамин (стресс)», «Фокус-день».
- Опционально: интеграция с Screen Time API (iOS/Android).

### 7.2 Расчёт и визуализация
- **Dopamine Load Score** (0–10): взвешенная сумма (можно кастомизировать веса).
- Графики: Scatter (Load vs Completion %), Bar по дням недели, Trend line.
- Еженедельный отчёт с 3–5 персонализированными инсайтами.

### 7.3 Insights & Рекомендации
- «Снижение скролла на 30 мин/день коррелирует с +15% completion rate (на основе твоих данных).»
- Перед планированием спринта: предупреждение + предложение low-dopamine режима.
- Замены: список effortful активностей (с earned dopamine).

### 7.4 Интеграция с core
- В weekly planning: блок «Текущий Dopamine Budget» + рекомендация.
- В дашборде целей: badge «Low Dopamine Week» → бонус к streak.

### 7.5 Геймификация (v1.5+)
- Streaks «Low Dopamine Days».
- Очки за соблюдение бюджета + высокий completion rate.
- Уровни / ачивки.

### 7.6 Приватность & Локальность (важно для РФ/СНГ)
- Локальное хранение по умолчанию.
- Опция экспорта данных.
- Без обязательной облачной синхронизации (учитывая санкции и предпочтения пользователя).

---

## 8. Non-Functional Requirements
- Производительность: лог < 5 секунд.
- Доступность: offline-first.
- Приватность: GDPR-like + локальные данные.
- Масштабируемость: легко добавлять новые категории источников.
- A/B тестирование: легко включать/выключать корреляционные отчёты.

---

## 9. Success Metrics & Measurement
- Quantitative: см. раздел 3.
- Qualitative: интервью через 4–6 недель использования.
- A/B тест: группа с модулем vs без (на completion rate).

---

## 10. Implementation Roadmap

**MVP (2–4 недели):**
- Ручной лог + 5 категорий.
- Простой weekly report с корреляцией (таблица + 1 график).
- Интеграция в planning flow.
- Базовые insights.

**v1.5 (следующий спринт):**
- Screen Time API интеграция.
- Кастомизация весов Dopamine Load.
- Геймификация (streaks).

**v2 (через 2–3 месяца):**
- AI-генерация персональных рекомендаций.
- Сравнение с «собой 3 месяца назад».
- Эксперименты (A/B внутри продукта).

**Технические замечания:**
- Использовать существующий стек проекта.
- Для корреляций: простой статистический движок (Pearson или визуальный тренд) на старте.
- Локализация: русский + английский.

---

## 11. Risks & Mitigations

**Риск 1:** Пользователи воспримут как «ещё один guilt-trip трекер».
**Митигация:** Фрейминг «Reward Management для достижения целей», позитивные инсайты, фокус на данных пользователя, а не суждениях.

**Риск 2:** «Dopamine detox» backlash (научная критика oversimplification).
**Митигация:** Использовать термин «Reward Audit / Бюджет наград». Приводить точные ссылки на исследования в образовательных карточках.

**Риск 3:** Низкий adoption логирования.
**Митигация:** Максимально быстрый 1-tap ввод + пресеты + reminders + геймификация.

**Риск 4:** Приватность (особенно в РФ).
**Митигация:** Локальное хранение по умолчанию, прозрачность.

---

## 12. Open Questions
- Нужно ли добавлять категорию «порно / азарт» (чувствительная)?
- Какой вес давать сахару vs скроллу (пользовательская кастомизация)?
- Интегрировать ли с внешними трекерами еды (MyFitnessPal и т.п.)?
- Геймификация: насколько глубоко (как Habitica)?

---

## Appendix: Полный список источников (все гиперссылки)

1. Rada 2005 — https://pubmed.ncbi.nlm.nih.gov/15987666/
2. Avena 2008 — https://pubmed.ncbi.nlm.nih.gov/17617461/
3. Jacques 2019 — https://pubmed.ncbi.nlm.nih.gov/31125634/
4. UMich 2020 — https://news.umich.edu/high-sugar-diet-dampens-release-of-dopamine-triggering-overeating/
5. Stanford Lembke — https://med.stanford.edu/news/insights/2021/10/addictive-potential-of-social-media-explained.html
6. Kushlev 2025 — https://academic.oup.com/pnasnexus/article/4/2/pgaf017/8016017
7. SDSU Screen Time Study — https://business.sdsu.edu/news/2022/10/screentime-research-v2
8. The Scientist Dopamine Detox — https://www.the-scientist.com/debunking-the-dopamine-detox-trend-72036
9. Northwestern 2025 — https://www.eurekalert.org/news-releases/1080824
10. PMC 2025 Social Media Addiction — https://pmc.ncbi.nlm.nih.gov/articles/PMC11804976/
11. PMC 2025 Neurocognitive Impact — https://pmc.ncbi.nlm.nih.gov/articles/PMC12329480/
