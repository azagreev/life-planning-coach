#!/usr/bin/env python3
"""Извлекает секцию релиза из CHANGELOG.md и сохраняет как RELEASE_NOTES.

Использование:
    python3 scripts/extract-release-notes.py 0.10.2
    python3 scripts/extract-release-notes.py v0.10.2
"""

import re
import sys
from pathlib import Path


def main() -> int:
    args = sys.argv[1:]
    stdout_mode = "--stdout" in args
    if stdout_mode:
        args.remove("--stdout")

    if len(args) < 1:
        print("Ошибка: не указана версия")
        print("Использование: python3 scripts/extract-release-notes.py 0.10.2")
        print("              python3 scripts/extract-release-notes.py --stdout 0.10.2")
        return 1

    version = args[0].lstrip("v")
    tag = f"v{version}"

    changelog_path = Path("CHANGELOG.md")
    if not changelog_path.exists():
        print("Ошибка: CHANGELOG.md не найден")
        return 1

    content = changelog_path.read_text(encoding="utf-8")

    # Находим секцию ## [VERSION] — с или без даты
    pattern = rf"## \[{re.escape(version)}\].*?(?=\n## \[|$)"
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        print(f"⚠️  Секция [{version}] не найдена в CHANGELOG.md")
        return 1

    section = match.group(0)

    # Заменяем заголовок секции на человекочитаемый
    section = re.sub(
        rf"^## \[{re.escape(version)}\].*",
        f"## Что нового в {tag}",
        section,
        count=1,
    )

    # Убираем trailing пустые строки и разделители ---
    section = section.rstrip()
    section = re.sub(r"\n---+\s*$", "", section)
    section = section.rstrip()

    # Убедимся, что есть пустая строка в конце
    if not section.endswith("\n"):
        section += "\n"

    if stdout_mode:
        print(section, end="")
        return 0

    # Output location moved from references/archive/ → docs/archive/ in v0.15.x
    output_dir = Path("docs/archive")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"RELEASE_NOTES_{tag}.md"

    output_path.write_text(section, encoding="utf-8")
    print(f"✅ Release notes сохранены: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
