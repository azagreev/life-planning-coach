# Tester Task: v0.5.0 — Two-Track Diagnostic

## Контекст
Разработчик обновил diagnostic_methods.md и SKILL.md. Нужно проверить соответствие acceptance_criteria_v0.5.md.

## Тест-план

### Test Suite 1: Структурные тесты (Автоматизируемые)

```python
# tests/diagnostic/test_v0.5.0_structure.py

class TestTwoTrackArchitecture:
    def test_quick_track_section_exists(self):
        # diagnostic_methods.md содержит "## Track A: Quick Diagnostic"
        pass
    
    def test_deep_track_section_exists(self):
        # diagnostic_methods.md содержит "## Track B: Deep Diagnostic"
        pass
    
    def test_skill_refers_two_track(self):
        # SKILL.md содержит Two-Track в Stage 1
        pass

class TestValuesSimplified:
    def test_no_pairwise_comparison(self):
        # diagnostic_methods.md НЕ содержит "45 пар" в Values секции
        # Допустимо только в комментарии "устарело" или истории
        pass
    
    def test_top5_selection_exists(self):
        # Есть "Top-5 Selection" или аналог
        pass
    
    def test_top3_ranking_exists(self):
        # Есть "Top-3 Ranking" или аналог
        pass

class TestIkigaiFivePillars:
    def test_five_pillars_present(self):
        # Все 5 pillars упомянуты: Start Small, Releasing Yourself, 
        # Harmony, Joy of Little Things, Being in Here and Now
        pass

class TestLifeStoryOptional:
    def test_optional_flag_present(self):
        # Есть "опциональный" или "skip" в Life Story секции
        pass
    
    def test_life_story_lite_exists(self):
        # Есть Life Story Lite (3 вопроса)
        pass

class TestReadinessGates:
    def test_readiness_gate_after_each_phase(self):
        # После каждой из 5 фаз есть Readiness Gate
        pass

class TestWorkviewMicro:
    def test_workview_max_3_questions(self):
        # Workview блок содержит ≤ 3 вопросов
        pass
    
    def test_lifeview_max_3_questions(self):
        # Lifeview блок содержит ≤ 3 вопросов
        pass

class TestQuickTrackSize:
    def test_quick_questions_count(self):
        # Подсчитать вопросы в Quick track: должно быть ≤ 30
        pass
    
    def test_quick_time_estimate(self):
        # Quick track: время ≤ 30 мин
        pass

class TestSafetyPreserved:
    def test_warning_signs_present(self):
        # Safety & Ethics секция сохранена
        pass
    
    def test_skip_option_present(self):
        # Skip option для чувствительных тем
        pass

class TestLanguageRules:
    def test_no_forbidden_words(self):
        # Нет "надо", "должен", "провал", "отстой" в диагностических вопросах
        pass
```

### Test Suite 2: Интеграционные тесты

```python
# tests/release/test_skill_package.py (дополнение)

class TestV050Integration:
    def test_diagnostic_methods_in_zip(self):
        # ZIP содержит diagnostic_methods.md
        pass
    
    def test_research_in_zip(self):
        # ZIP содержит research_diagnostic_deep_dive.md
        pass
```

### Test Suite 3: Ручные проверки

- [ ] Прочитать diagnostic_methods.md целиком — логика последовательности верна?
- [ ] Прочитать SKILL.md целиком — стиль и тон сохранены?
- [ ] Wheel of Life: 8 сфер описаны понятно?
- [ ] Emotional Landing: все 5 состояний покрыты?

## Критерии приёмки
- [ ] Все P0 AC пройдены (AC-1..AC-8)
- [ ] Все P1 AC пройдены (AC-9..AC-12)
- [ ] Все 22 legacy теста проходят
- [ ] Новые тесты проходят
- [ ] ZIP билдится без ошибок
- [ ] SKILL.md < 5000 слов
