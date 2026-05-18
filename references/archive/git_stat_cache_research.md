# Исследование: `git diff-index` vs `git diff` при `core.filemode=false` на WSL/Windows

> Дата: 2026-05-18  
> Контекст: `scripts/release.sh` использует `git diff-index --quiet HEAD --` для проверки чистоты рабочей директории. На WSL с `core.filemode=false` команда возвращает "dirty", хотя `git status --short` и `git diff` показывают рабочую директорию чистой.

---

## 1. Known Facts (исходные наблюдения)

| Факт | Значение |
|------|----------|
| `core.filemode` | `false` |
| Режим файлов в рабочей директории | `777` (WSL default для `/mnt/c/...`) |
| Режим файлов в git index | `100644` |
| Триггер | pytest перезаписывает файлы |
| `git diff-index HEAD --name-only` | Показывает файлы как modified |
| `git diff -p HEAD` | **Нет** content diff, **нет** mode diff |
| `git update-index --refresh` | **Исправляет** mismatch |
| SHA-1 рабочей копии = SHA-1 HEAD = SHA-1 INDEX | Контент идентичен |

---

## 2. Механизм: как `git diff-index` отличается от `git diff`

### 2.1 Архитектурное различие: Plumbing vs Porcelain

Git делит команды на два уровня:

- **Plumbing (низкоуровневые)**: `git diff-index`, `git diff-files`, `git diff-tree`, `git update-index` — работают напрямую с объектами git и индексом.
- **Porcelain (высокоуровневые)**: `git diff`, `git status` — добавляют user-friendly поведение поверх plumbing.

### 2.2 Ключевое различие: `diff.autoRefreshIndex`

Согласно официальной документации `git-config`:

> **`diff.autoRefreshIndex`**  
> When using `git diff` to compare with work tree files, do not consider stat-only changes as changed. Instead, silently run `git update-index --refresh` to update the cached stat information for paths whose contents in the work tree match the contents in the index. **This option defaults to `true`.**  
> **Note that this affects only `git diff` Porcelain, and not lower level `diff` commands such as `git diff-files`.**
>
> — [git-config Documentation](https://git-scm.com/docs/git-config)

Это означает:

| Команда | Поведение при stat-mismatch |
|---------|----------------------------|
| `git diff HEAD` (porcelain) | Сначала проверяет stat. Если stat не совпадает, читает содержимое и считает SHA-1. Если SHA-1 совпадает — **молча обновляет stat в индексе** (`git update-index --refresh`) и **не считает файл изменённым**. |
| `git diff-index HEAD --` (plumbing) | Сравнивает tree object (HEAD) с рабочей директорией/индексом напрямую. **Не делает auto-refresh**. Если stat в индексе не совпадает с текущим stat файла — файл считается modified. |

### 2.3 Почему именно `core.filemode=false` влияет на это поведение

Когда `core.filemode=false`:

1. Git **игнорирует** executable bit из `lstat()` результата при записи в индекс ([git-config docs](https://git-scm.com/docs/git-config), раздел `core.filemode`).
2. Вместо этого Git сохраняет режим из существующей записи индекса (или `100644` для новых файлов).
3. Однако **`core.filemode` не влияет на то, как Git *читает* stat-информацию для проверки изменений**.

Таким образом:
- Файл в рабочей директории имеет режим `777` (WSL default).
- Git делает `lstat()`, получает `st_mode = 100777`.
- Git сравнивает это с записью в индексе (`100644`).
- С `core.filemode=false` Git **не должен** считать это mode-изменением для diff-вывода.
- Но `git diff-index` всё равно видит, что stat-данные (включая mode) в индексе **отличаются** от stat-данных на диске, и помечает файл как "needs checking".
- После проверки SHA-1 совпадает, но `diff-index` **не обновляет индекс**, в отличие от `git diff` porcelain.

---

## 3. Роль полей `ctime`, `mtime`, `dev`, `ino` в индексе

### 3.1 Структура записи в git index

Каждая запись в `.git/index` содержит (согласно [Git Index Format](https://git-scm.com/docs/index-format) и исследованиям):

```
ctime (seconds + nanoseconds)  — время изменения inode
mtime (seconds + nanoseconds)  — время изменения содержимого
dev                            — device ID
ino                            — inode number
mode                           — file mode (100644, 100755, 120000, 160000)
uid                            — user ID
gid                            — group ID
size                           — file size
sha-1                          — object hash
flags                          — internal flags
path                           — file path
```

### 3.2 Как Git использует stat cache

Git использует эти поля как **быструю эвристику** ("racy git" optimization):

1. Если `stat()` файла совпадает со всеми полями в индексе — Git **предполагает**, что файл не изменился, и **не вычисляет SHA-1**.
2. Если хотя бы одно поле отличается — Git помечает файл как потенциально изменённый.
3. Для porcelain-команд (`git diff`, `git status`): если SHA-1 совпадает, но stat отличается — обновляет stat в индексе.
4. Для plumbing-команд (`git diff-index`): stat-разница достаточна для отчёта об изменении.

### 3.3 Конфигурация `core.checkStat`

Git предоставляет настройку для контроля того, какие stat-поля проверять:

> **`core.checkStat`**  
> When missing or is set to `default`, many fields in the stat structure are checked to detect if a file has been modified since Git looked at it. When this configuration variable is set to `minimal`, sub-second part of mtime and ctime, the uid and gid of the owner of the file, the inode number (and the device number, if Git was compiled to use it), are excluded from the check among these fields, leaving only the whole-second part of mtime (and ctime, if `core.trustCtime` is set) and the filesize to be checked.
>
> — [git-config Documentation](https://git-scm.com/docs/git-config)

### 3.4 Почему pytest вызывает mismatch

Когда pytest перезаписывает файл:
- Содержимое остаётся идентичным (тот же SHA-1).
- Но `mtime`, `ctime` и, возможно, `ino` (inode) **меняются**, потому что файл был открыт на запись и закрыт.
- Это создаёт stat mismatch между индексом и рабочей директорией.

---

## 4. Это баг или expected behavior?

**Это expected behavior.**

Доказательства:

1. **Документация прямо указывает** на различие между porcelain и plumbing:
   > "Note that this affects only `git diff` Porcelain, and not lower level `diff` commands such as `git diff-files`."

2. **Дизайн plumbing-команд**: Команды вроде `git diff-index` предназначены для скриптов и low-level операций. Они должны давать детерминированный результат на основе текущего состояния индекса, не модифицируя его "по боку".

3. **Автор Git (Junio C Hamano)** и сообщество неоднократно подтверждали, что `git diff-index` — это plumbing, который не делает auto-refresh. Рекомендуемое решение для скриптов: либо использовать porcelain (`git diff`), либо явно вызывать `git update-index --refresh` перед `git diff-index`.

4. **Stack Overflow**: ["git update-index --refresh will update the index information so that a subsequent git diff-index works as you'd expect it to."](https://stackoverflow.com/questions/34807971)

---

## 5. Самый безопасный кросс-платформенный фикс для `release.sh`

### 5.1 Варианты решения

| Вариант | Код | Плюсы | Минусы |
|---------|-----|-------|--------|
| **A. Заменить на `git diff --quiet HEAD`** | `if ! git diff --quiet HEAD; then` | Простая замена. Использует porcelain с `diff.autoRefreshIndex=true`. Не требует изменения индекса вручную. | `git diff` — porcelain, который теоретически может измениться в будущих версиях Git. |
| **B. `git update-index --refresh` перед `git diff-index`** | `git update-index --refresh >/dev/null 2>&1 \|\| true; if ! git diff-index --quiet HEAD --; then` | Сохраняет plumbing-команду. Явно обновляет stat cache. | `update-index --refresh` возвращает exit code 1, если находит mismatch, даже если обновляет. Нужно `\|\| true`. |
| **C. `git status --porcelain`** | `if [ -n "$(git status --porcelain)" ]; then` | Стандартный способ проверки. Работает со stat cache корректно. | Показывает также untracked файлы. Нужен фильтр, если untracked не должны считаться "dirty". |
| **D. `core.checkStat=minimal`** | `git config core.checkStat minimal` | Уменьшает чувствительность к stat-изменениям. | Глобальное изменение поведения Git. Может маскировать реальные изменения. **Не рекомендуется.** |

### 5.2 Рекомендуемый фикс

**Вариант A** — замена на `git diff --quiet HEAD` — является наиболее простым и безопасным:

```bash
# Вместо:
# if ! git diff-index --quiet HEAD --; then

# Использовать:
if ! git diff --quiet HEAD; then
    echo "❌ Есть незакоммиченные изменения:"
    git status --short
    exit 1
fi
```

**Вариант B** — если необходимо сохранить `git diff-index` (например, для совместимости с другими скриптами или по соображениям стиля):

```bash
# Обновляем stat cache перед проверкой
git update-index --refresh >/dev/null 2>&1 || true

if ! git diff-index --quiet HEAD --; then
    echo "❌ Есть незакоммиченные изменения:"
    git status --short
    exit 1
fi
```

> **Важно**: `git update-index --refresh` возвращает exit code 1, если какие-либо файлы требовали обновления, даже если он успешно обновил их. Поэтому нужен `|| true`.

### 5.3 Почему не `git status --short`

`git status --short` уже используется в `release.sh` для вывода списка изменений, но для **проверки** "dirty or not" он менее идеален:
- `git status` показывает untracked файлы.
- Для релизного скрипта untracked файлы могут быть допустимы (например, временные файлы тестов), а `git diff-index` / `git diff` проверяют только tracked файлы.

### 5.4 Почему не `core.checkStat=minimal`

Это глобальная настройка репозитория, которая изменяет поведение Git для всех операций. Она может маскировать реальные изменения и создавать "racy git" проблемы. Не рекомендуется для production-скриптов.

---

## 6. Резюме

1. **`git diff-index` — plumbing**, он не обновляет stat cache автоматически. Он напрямую сравнивает stat-данные индекса с рабочей директорией.
2. **`git diff` — porcelain**, с `diff.autoRefreshIndex=true` (default) он молча обновляет stat cache для файлов с совпадающим содержимым, игнорируя stat-only изменения.
3. **Поля `ctime`, `mtime`, `dev`, `ino`** в индексе используются как быстрая эвристика. Когда pytest перезаписывает файл, `mtime`/`ctime` меняются, вызывая stat mismatch.
4. **`core.filemode=false`** влияет на то, как Git *записывает* mode в индекс, но не на то, как *проверяет* stat-данные. Разница в mode (`777` vs `644`) — часть stat mismatch, который `diff-index` видит, но `core.filemode` подавляет его только при генерации diff, не при stat-проверке.
5. **Это expected behavior**, задокументированное в `git-config(1)`.
6. **Рекомендуемый фикс**: заменить `git diff-index --quiet HEAD --` на `git diff --quiet HEAD` в `release.sh`.

---

## 7. Ссылки

- [git-config Documentation — diff.autoRefreshIndex](https://git-scm.com/docs/git-config#Documentation/git-config.txt-diffautoRefreshIndex)
- [git-config Documentation — core.filemode](https://git-scm.com/docs/git-config#Documentation/git-config.txt-corefilemode)
- [git-config Documentation — core.checkStat](https://git-scm.com/docs/git-config#Documentation/git-config.txt-corecheckStat)
- [git-update-index Documentation — --refresh](https://git-scm.com/docs/git-update-index#Documentation/git-update-index.txt---refresh)
- [git-diff-index Documentation](https://git-scm.com/docs/git-diff-index)
- [Stack Overflow — git diff-index vs git diff](https://stackoverflow.com/questions/24197606/whats-the-difference-between-git-diff-and-gif-diff-index)
- [Stack Overflow — git diff-index after git diff](https://stackoverflow.com/questions/34807971/why-does-git-diff-index-head-result-change-for-touched-files-after-git-diff-or-g)
- [Git Index Format (Official)](https://git-scm.com/docs/index-format)
