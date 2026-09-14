# scripts/

Generation tooling. Nothing here runs at build or request time — these scripts
produce the JSON in [`../data/`](../data/), which is committed to the repo.

## build_index.py

Parses every canonical `SKILL.md` in
[alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)
into two JSON files.

### Usage

```bash
# Clone the upstream repo somewhere (~65MB, shallow is fine)
git clone --depth 1 https://github.com/alirezarezvani/claude-skills.git ../claude-skills

# Generate
python3 scripts/build_index.py ../claude-skills
```

Python 3, standard library only. No dependencies, no virtualenv.

Writes `data/index.json` and `data/skills.json`, overwriting whatever is there.

### What it does

1. Walks every top-level directory in the source repo, **skipping anything
   beginning with a dot**
2. Finds all `SKILL.md` files — 388 at the current snapshot
3. Parses the YAML frontmatter of each for `name`, `description`, and the
   optional `version` / `license` / `author` / `tags` fields
4. Checks each skill folder for sibling `scripts/` and `references/` directories
5. Derives a slug, a domain label, and per-skill install commands
6. Reads the upstream commit SHA and date via `git log` for the snapshot metadata
7. Writes the slim index and the full records

### Decisions worth knowing

These are deliberate, and changing them will break things:

**Slugs are `domain/skill-name`.** The 388 files share only 374 unique names —
14 names collide across folders. Keying on `name` alone silently drops skills.

**Dot-folders are excluded.** `.gemini/`, `.hermes/` and `.vibe/` are generated
mirrors, not source. `.gemini/` holds 458 entries, 89 of which aren't skills at
all — they're commands (`cmd-a11y-audit`, `cmd-cs-aeo`), READMEs and templates
swept up by the upstream conversion script. The mirrors have also drifted from
source, and `.hermes/` and `.vibe/` contain no `SKILL.md` files despite the
upstream README describing them as pre-generated trees.

**Categories come from the folder path, not `tags`.** Only 13% of skills define
`tags` in frontmatter, so tag-based filtering would appear broken for most of
the library. The `LABELS` dict maps folder names to display labels; unmapped
folders fall back to the raw folder name.

**Only flat scalar frontmatter keys are read.** Some skills use nested YAML
under `metadata:`. The parser skips indented lines and list items rather than
pulling in a YAML dependency, since nothing nested is needed for the index.

### Frontmatter coverage

Measured across all 388 files at the current snapshot:

| Key | Present | Usable? |
|---|---|---|
| `name` | 100% | Yes |
| `description` | 100% | Yes |
| `license` | 49% | Partially |
| `metadata` | 35% | Nested, skipped |
| `version` | 13% | No |
| `tags` | 13% | No |
| `compatible_tools` | 11% | No |

One file uses `Name` rather than `name`; keys are lowercased on read.

### Re-running against a newer upstream

The index is a point-in-time snapshot, not a live mirror. To refresh it, pull
the upstream repo and re-run — the `meta` block will pick up the new commit SHA
and date automatically. Check the diff on `data/` before committing; a large
change in `skill_count` usually means upstream restructured a folder.
