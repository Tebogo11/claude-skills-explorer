# Claude Skills Index

A browsable, searchable index of the 388 agent skills in
[alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills).

The upstream repo is excellent but hard to navigate — 388 skills across 20 domains,
documented in a single very long README with no search and no per-skill install
instructions. This project parses every `SKILL.md` into structured JSON and puts a
UI on top of it, so you can find a skill and get the exact command to install it.

**[Live site →](https://example.com)** <!-- replace -->

> Skill content is by [Alireza Rezvani](https://github.com/alirezarezvani), MIT licensed.
> This project **indexes** those skills — it does not redistribute them. Every entry links
> back to the source repo for the actual files. See [ATTRIBUTION.md](./ATTRIBUTION.md).

## Snapshot

The index is a point-in-time snapshot, not a live mirror.

| | |
|---|---|
| Source commit | [`19392f7`](https://github.com/alirezarezvani/claude-skills/commit/19392f7a08264ed00486a251f5b2098321771f94) |
| Commit date | 26 August 2026 |
| Skills indexed | 388 (374 unique names) |
| Domains | 20 |

## Data

Two generated files, both committed to the repo — there's no database.

- `data/index.json` (258KB) — slim records for search and filtering: slug, name,
  domain, description, whether the skill ships Python scripts.
- `data/skills.json` (565KB) — full records: file paths, source URLs, script
  filenames, per-skill install commands, and `version` / `license` / `author`
  where the upstream frontmatter provides them.

Both carry a `meta` block with the snapshot commit, counts per domain, and the
attribution string.

### Notes on the parse

A few things about the upstream data worth knowing if you use these files:

- **Slugs are `domain/skill-name`.** 388 files share only 374 unique names, so
  14 names collide across folders. Keying on name alone silently drops skills.
- **Categories come from the folder path, not `tags`.** Only 13% of skills
  define `tags` in frontmatter, so tag-based filtering would look broken.
- **Dot-folders are excluded.** `.gemini/`, `.hermes/` and `.vibe/` are generated
  mirrors. `.gemini/` contains 458 entries, 89 of which aren't skills at all
  (commands, READMEs, templates), and the mirrors have drifted from source.
- **Descriptions are long.** Upstream writes them as agent trigger prompts, often
  500+ characters. Truncate for cards, show in full on detail pages.

## Run it yourself

```bash
# 1. Clone this repo
git clone https://github.com/<you>/claude-skills-index.git
cd claude-skills-index

# 2. Clone the upstream skills repo alongside it (~65MB)
git clone --depth 1 https://github.com/alirezarezvani/claude-skills.git ../claude-skills

# 3. Regenerate the JSON (Python 3, standard library only)
python3 scripts/build_index.py

# 4. Install and run the site
npm install
npm run dev
```

The parser writes to `data/`. It reads only the canonical top-level folders and
skips anything beginning with a dot.

## Stack

<!-- adjust to what you actually used -->
Next.js · TypeScript · Tailwind · deployed on Vercel. The index is static JSON,
so search and filtering run client-side with no query layer.

## License

The code in this repo is MIT — see [LICENSE](./LICENSE).

The indexed skill metadata (names and descriptions) originates from
[alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills),
also MIT. Its copyright notice is reproduced in [ATTRIBUTION.md](./ATTRIBUTION.md).
