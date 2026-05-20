## Что нового в v0.12.2

### Added
- **`references/calendar_intelligence.md`** — Pre-flight Protocol: Density Check → Conflict Detection → Chronotype Alignment → Smart Proposal → Create with Validation
- **PDF экспорт дашборда** — кнопка «Печать / PDF» в `life-planning-dashboard.html` + `@media print` стили

### Changed
- **Paper Coach Mode** — заменён несостоятельный retry protocol (`persistence_retry`) на честный text-only flow в `SKILL.master.md` и всех platform-скиллах
- **Platform-neutral wording** — `calendar_constants.md` очищен от «Claude»/«MCP» для корректного inline в Grok/Kimi
- **CI/CD** — `build-skill.yml` теперь гонит полный pytest suite (`tests/`) вместо только `tests/release`
- **Release Notes** — unified generation из CHANGELOG.md, удалены дублирующие `RELEASE_NOTES_*.md`

### Fixed
- **Dangling references** — `calendar_constants.md` теперь inline'ится в Grok/Kimi через `P0_REFS`
