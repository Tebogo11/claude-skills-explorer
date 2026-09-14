# data/

Generated JSON. **Do not edit by hand** — regenerate with
[`../scripts/build_index.py`](../scripts/README.md) instead.

Both files are committed to the repo. There's no database: at 388 records the
whole index ships to the client, so search and filtering run with no query layer.

| File | Size | Use |
|---|---|---|
| `index.json` | 258 KB | Browse, search, filter views |
| `skills.json` | 565 KB | Detail pages |

## Snapshot

| | |
|---|---|
| Source | [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) |
| Commit | [`19392f7`](https://github.com/alirezarezvani/claude-skills/commit/19392f7a08264ed00486a251f5b2098321771f94) |
| Commit date | 26 August 2026 |
| Skills | 388 (374 unique names) |
| Domains | 20 |

Point-in-time, not a live mirror. See [`../ATTRIBUTION.md`](../ATTRIBUTION.md) —
the `name` and `description` fields are reproduced from the source repo under MIT.

## Shape

Both files are `{ meta, skills }`.

### meta

```json
{
  "source_repo": "alirezarezvani/claude-skills",
  "source_url": "https://github.com/alirezarezvani/claude-skills",
  "license": "MIT",
  "attribution": "Skills by Alireza Rezvani, MIT licensed...",
  "snapshot_commit": "19392f7a08264ed00486a251f5b2098321771f94",
  "snapshot_commit_short": "19392f7",
  "snapshot_commit_date": "2026-08-26T15:53:02+02:00",
  "indexed_at": "2026-09-14T01:32:14+00:00",
  "skill_count": 388,
  "unique_names": 374,
  "domain_count": 20,
  "domains": [{ "domain": "engineering", "label": "Engineering — Advanced", "count": 93 }]
}
```

`domains` is sorted by count descending — usable directly for sidebar ordering.

### index.json — skills[]

Six fields, kept slim because this file ships to the browser.

| Field | Type | Notes |
|---|---|---|
| `slug` | string | `domain/skill-name`. Unique. Use as the route param |
| `name` | string | From upstream frontmatter. **Not unique** — 14 collisions |
| `domain` | string | Top-level folder |
| `domain_label` | string | Display label |
| `description` | string | From upstream. Often 500+ chars — see below |
| `has_scripts` | boolean | Whether the skill ships Python tools |

### skills.json — skills[]

Everything above, plus:

| Field | Type | Notes |
|---|---|---|
| `path` | string | Folder path within the source repo |
| `source_url` | string | Deep link to the skill on GitHub |
| `version` | string \| null | Present on 13% |
| `license` | string \| null | Present on 49% |
| `author` | string \| null | Present on 13% |
| `tags` | string[] | Usually empty — present on 13% |
| `scripts` | string[] | Python filenames in the skill's `scripts/` dir |
| `has_references` | boolean | Whether a `references/` dir exists |
| `install` | object | See below |
| `body_chars` | number | Length of the SKILL.md body, a rough depth proxy |

`install`:

```json
{
  "claude_code_marketplace": "/plugin marketplace add alirezarezvani/claude-skills",
  "manual": "cp -r engineering/rag-architect ~/.claude/skills/",
  "codex_manual": "cp -r engineering/rag-architect ~/.codex/skills/",
  "script_example": "python3 engineering/rag-architect/scripts/x.py --help"
}
```

`script_example` is `null` when the skill ships no Python tools.

## Gotchas

**Key on `slug`, never `name`.** 388 records, 374 names.

**Descriptions are long.** Upstream writes them as agent trigger prompts, not
human summaries — many run past 500 characters and include quoted example
phrases. Truncate at the first sentence for cards; show in full on detail pages.

**Don't full-text search descriptions.** At that length almost any query matches
almost everything. Index `name` + `domain` + the first sentence only.

**`tags` is effectively unusable.** Empty for 87% of skills. Filter on `domain`.

**Nested frontmatter is dropped.** 35% of skills have a nested `metadata:` block
that the parser skips. If you ever need it, that's where to look first.
