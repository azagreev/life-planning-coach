# PRD: Health & Metabolism Track

Проект: life-planning-coach  
Версия: 2.1  
Дата: 24 мая 2026

## 1. Обзор и проблема

В life-planning-coach отсутствует системный трек, посвящённый метаболическому здоровью, регуляции аппетита и энергии. Пользователи часто объясняют проблемы с питанием и весом исключительно «отсутствием дисциплины», хотя научные данные показывают сильное влияние физиологических факторов (сон, стресс, состав питания, поведение за столом).

Решение — создать отдельный трек Health & Metabolism, который помогает пользователю работать с доказанными рычагами регуляции аппетита и энергии.

## 2. Цели трека

- Дать пользователю научно обоснованное понимание механизмов регуляции аппетита и энергии.
- Снизить избыточную самокритику через качественный рефрейминг.
- Помочь выстраивать привычки, поддерживающие естественные сигналы сытости.
- Интегрировать трек в существующие процессы коучинга.

## 3. Научная база

Трек опирается на следующие исследования и направления:

### Глиальный механизм регуляции сытости
López S. et al. Tanycyte-derived lactate activates astrocytic HCAR1 to modulate glutamatergic signaling and POMC neuron excitability. *Proceedings of the National Academy of Sciences*, 2026.  
[DOI: 10.1073/pnas.2537810123](https://doi.org/10.1073/pnas.2537810123)

### Влияние сна на аппетит
Spiegel K. et al. Sleep curtailment in healthy young men is associated with decreased leptin levels, elevated ghrelin levels, and increased hunger and appetite. *Annals of Internal Medicine*, 2004.

### Стресс и пищевое поведение
Epel E. et al. Stress may add bite to appetite in women: a laboratory study of stress-induced cortisol and eating behavior. *Psychoneuroendocrinology*, 2001.  
Sominsky L., Spencer S.J. Eating behavior and stress: a pathway to obesity. *Frontiers in Psychology*, 2014.

### Белок и сытость
Leidy H.J. et al. The role of protein in weight loss and maintenance. *American Journal of Clinical Nutrition*, 2015.  
Westerterp-Plantenga M.S. et al. Dietary protein, metabolism, and body-weight regulation: dose–response effects. *International Journal of Obesity*, 2006.

### Клетчатка и контроль аппетита
Wanders A.J. et al. Effects of dietary fibre on subjective appetite, energy intake and body weight: a systematic review of randomized controlled trials. *Obesity Reviews*, 2011.  
Slavin J.L. Dietary fiber and body weight. *Nutrition*, 2005.

### Тщательное жевание
Chmiel J. et al. The Neural Correlates of Chewing Gum — A Neuroimaging Review of Its Effects on Brain Activity. *Brain Sciences*, 2025.

### Кофеин: влияние на аппетит, метаболизм и сон
Drake C. et al. Caffeine effects on sleep taken 0, 3, or 6 hours before going to bed. *Journal of Clinical Sleep Medicine*, 2013.

Astrup A. et al. Caffeine: a double-blind, placebo-controlled study of its thermogenic, metabolic, and cardiovascular effects in healthy volunteers. *The American Journal of Clinical Nutrition*, 1990.

Dulloo A.G. et al. Normal caffeine consumption: influence on thermogenesis and daily energy expenditure in lean and postobese human volunteers. *The American Journal of Clinical Nutrition*, 1989.

### Хлорогеновая кислота (зелёный кофе)
Kanchanasurakit S. et al. Chlorogenic acid in green bean coffee on body weight: a systematic review and meta-analysis of randomized controlled trials. *Systematic Reviews*, 2023.

## 4. Ключевые рычаги трека

| Рычаг                        | Влияние                                              | Сила доказательств      | Приоритет |
|-----------------------------|------------------------------------------------------|-------------------------|---------|
| Сон                     | Регуляция грелина и лептина                          | Высокая                 | Высокий |
| Стресс                  | Повышение кортизола и аппетита                       | Высокая                 | Высокий |
| Белок                   | Повышение сытости                                    | Высокая                 | Высокий |
| Клетчатка               | Стимуляция гормонов сытости                          | Хорошая                 | Высокий |
| Тщательное жевание      | Повышение гормонов сытости и времени на сигнал       | Средняя                 | Средний |
| Кофеин (тайминг)        | Кратковременный эффект на аппетит + сильное влияние на сон | Высокая (по сну)     | Средний |
| Хлорогеновая кислота    | Скромное снижение веса (краткосрочно)                | Низкая                  | Низкий  |

## 5. Структура трека

Трек включает:

- Расширенную диагностику (сон, стресс, питание, кофеин, жевание).
- Образовательный блок с научными механизмами.
- Рефрейминг самокритики.
- Постановку целей и привычек.
- Специфические вопросы в еженедельной ретроспективе.
- Возможность проведения микро-экспериментов.

## 6. Интеграция с существующими процессами

- Диагностика → добавление ветки Health & Metabolism.
- Goal Architecture → возможность работать с целями внутри трека.
- Привычки → использование существующих фреймворков.
- Ретроспектива → добавление метаболических вопросов.
- Эмоциональная регуляция → научный рефрейминг.

## 7. Ограничения

- Трек не предназначен для работы с расстройствами пищевого поведения.
- Часть исследований (жевание, хлорогеновая кислота) имеет умеренную или низкую доказательную базу.
- Эффекты кофеина и жевания преимущественно кратковременные.
- Коуч подчёркивает вспомогательный характер рекомендаций.

## 8. Техническая реализация

- Создать файл references/health-metabolism.md.
- Обновить SKILL.master.md (добавить трек, вопросы диагностики и ретроспективы, шаблоны рефрейминга).
- При необходимости создать папку references/health/.

## 9. Приоритеты реализации

Высокий приоритет: Сон, Стресс, Белок, Клетчатка  
Средний приоритет: Тщательное жевание, Кофеин (тайминг)  
Низкий приоритет: Хлорогеновая кислота
