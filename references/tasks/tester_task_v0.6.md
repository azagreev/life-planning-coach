# Tester Task: v0.6.0 — Authentic Goals + Portfolio + Adaptive Style

## Контекст
Разработчик создал authentic_goal_filter.md, communication_style.md и обновил SKILL.md + diagnostic_methods.md. Нужно проверить соответствие acceptance_criteria_v0.6.md.

**AC:** `references/acceptance_criteria_v0.6.md`

---

## Тест-план

### Test Suite 1: Структурные тесты (Автоматизируемые)

```python
# tests/v0.6.0/test_structure.py

class TestStage15Exists:
    def test_stage_15_in_skill_md(self):
        # SKILL.md содержит "Stage 1.5" или "Authentic Goal Filter"
        pass
    
    def test_authentic_goal_filter_reference(self):
        # SKILL.md ссылается на references/authentic_goal_filter.md
        pass

class TestAuthenticGoalFilterFile:
    def test_file_exists(self):
        # references/authentic_goal_filter.md существует
        pass
    
    def test_red_flag_detector(self):
        # 6+1 red flags присутствуют
        pass
    
    def test_whose_voice_questions(self):
        # "Чей голос" или "Чей это голос" присутствует
        pass
    
    def test_radar_chart(self):
        # 5 осей радара упомянуты
        pass
    
    def test_no_formula(self):
        # Нет weighted formula (values * 2 + energy + ...)
        pass
    
    def test_goal_portfolio(self):
        # "Active" + "On Pause" + "Pattern Analysis" присутствуют
        pass
    
    def test_not_discarded(self):
        # НЕТ слова "отсеянные" или "discarded"
        pass

class TestCommunicationStyleFile:
    def test_file_exists(self):
        # references/communication_style.md существует
        pass
    
    def test_four_quadrants(self):
        # 4 квадранта присутствуют
        pass
    
    def test_ttm_overlay(self):
        # 5 stages TTM присутствуют
        pass
    
    def test_oars_framework(self):
        # OARS компоненты присутствуют
        pass

class TestWheelOfLifeDomains:
    def test_eleven_domains(self):
        # Wheel of Life содержит 11 доменов
        pass
    
    def test_family_separate_from_social(self):
        # Family и Social — разные домены
        pass
    
    def test_contribution_exists(self):
        # Contribution / Вклад присутствует
        pass
    
    def test_meaning_mandatory(self):
        # Meaning / Смысл не помечен как опциональный
        pass

class TestSkillMdVersion:
    def test_version_060(self):
        # version: 0.6.0
        pass
    
    def test_word_count_under_5000(self):
        # wc -w SKILL.md < 5000
        pass
```

### Test Suite 2: Контентные тесты

```python
# tests/v0.6.0/test_content.py

class TestSocietalPressureTest:
    def test_four_questions(self):
        # 4 вопроса Societal Pressure Test
        pass

class TestDeepWhy:
    def test_three_levels(self):
        # 3 уровня Deep Why
        pass
    
    def test_no_five_levels(self):
        # НЕТ 5 уровней
        pass

class TestEnergyCheck:
    def test_somatic_framing(self):
        # "лёгкость" или "тяжесть" присутствует
        pass
    
    def test_optional_flag(self):
        # "опционально" или "по желанию"
        pass

class TestLanguageRules:
    def test_no_forbidden_words(self):
        # Нет "надо", "должен", "провал", "отстой"
        pass
    
    def test_goal_ownership_rules(self):
        # Goal Ownership Language Rules присутствуют
        pass

class TestHardGoals:
    def test_real_hard_definition(self):
        # Heartfelt, Animated, Required, Difficult (Mark Murphy)
        pass
    
    def test_no_fake_hard(self):
        # НЕТ "High Arousal Reactive Desire"
        pass
```

### Test Suite 3: Интеграционные тесты

```python
# tests/v0.6.0/test_integration.py

class TestV060Integration:
    def test_authentic_goal_filter_in_zip(self):
        # ZIP содержит authentic_goal_filter.md
        pass
    
    def test_communication_style_in_zip(self):
        # ZIP содержит communication_style.md
        pass
    
    def test_legacy_tests_pass(self):
        # Все legacy тесты проходят (version updated)
        pass
```

### Test Suite 4: Ручные проверки

- [ ] Прочитать authentic_goal_filter.md целиком — логика последовательности верна?
- [ ] Прочитать communication_style.md целиком — все 4 квадранта описаны понятно?
- [ ] Прочитать SKILL.md — Stage 1.5 не ломает поток Stage 1→Stage 2?
- [ ] Проверить тон: мягкий, не осуждающий, с emoji?
- [ ] Pattern Analysis: 2+ цели с одним flag → реально даёт инсайт?
- [ ] Radar patterns: 5 паттернов интерпретации — логичны?

---

## Критерии приёмки
- [ ] Все P0 AC пройдены (AC-1..AC-7)
- [ ] Все P1 AC пройдены (AC-8..AC-12)
- [ ] Все legacy тесты проходят (version updated to 0.6.0)
- [ ] Новые тесты проходят
- [ ] ZIP билдится без ошибок
- [ ] SKILL.md < 5000 слов
