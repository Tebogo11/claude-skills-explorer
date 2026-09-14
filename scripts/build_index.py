#!/usr/bin/env python3
"""Parse canonical SKILL.md files from alirezarezvani/claude-skills into JSON."""
import os, re, json, subprocess, datetime

REPO = "/home/claude/claude-skills"
OUT = "/mnt/user-data/outputs"

# Top-level folder -> human label. Dot-folders are mirrors and are excluded.
LABELS = {
    "engineering": "Engineering — Advanced",
    "engineering-team": "Engineering — Core",
    "marketing-skill": "Marketing",
    "marketing": "Marketing (top-level)",
    "c-level-advisor": "C-Level Advisory",
    "c-level-agents": "C-Level Agents",
    "ra-qm-team": "Regulatory & Quality",
    "product-team": "Product",
    "productivity": "Productivity",
    "research": "Research (academic)",
    "research-ops": "Research Operations",
    "project-management": "Project Management",
    "compliance-os": "Compliance OS",
    "commercial": "Commercial",
    "business-operations": "Business Operations",
    "business-growth": "Business & Growth",
    "finance": "Finance",
    "markdown-html": "Markdown to HTML",
    "loop-library": "Loop Library",
    "agent-launcher": "Agent Launcher",
}


def parse_frontmatter(text):
    """Return (dict, body). Only flat top-level scalar keys are read."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not m:
        return {}, text
    fm, body = {}, m.group(2)
    for line in m.group(1).split("\n"):
        if line.startswith((" ", "\t", "-")) or ":" not in line:
            continue  # nested value or list item; not needed for the index
        k, _, v = line.partition(":")
        k = k.strip()
        v = v.strip().strip("'\"")
        if re.fullmatch(r"[A-Za-z0-9_-]+", k) and v:
            fm[k.lower()] = v
    return fm, body


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def collect():
    roots = sorted(
        d for d in os.listdir(REPO)
        if os.path.isdir(os.path.join(REPO, d)) and not d.startswith(".")
    )
    skills = []
    for root in roots:
        for dirpath, _, filenames in os.walk(os.path.join(REPO, root)):
            for fn in filenames:
                if fn.lower() != "skill.md":
                    continue
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, REPO)
                skill_dir = os.path.dirname(full)
                folder_name = os.path.basename(skill_dir)

                fm, body = parse_frontmatter(
                    open(full, encoding="utf-8", errors="replace").read()
                )
                name = fm.get("name") or folder_name

                # Scripts that ship alongside the skill.
                scripts_dir = os.path.join(skill_dir, "scripts")
                scripts = sorted(
                    f for f in os.listdir(scripts_dir)
                    if f.endswith(".py")
                ) if os.path.isdir(scripts_dir) else []

                has_refs = os.path.isdir(os.path.join(skill_dir, "references"))

                # Slug on folder + skill name: 14 names collide across folders.
                slug = f"{slugify(root)}/{slugify(folder_name)}"

                skills.append({
                    "slug": slug,
                    "name": name,
                    "domain": root,
                    "domain_label": LABELS.get(root, root),
                    "description": fm.get("description", ""),
                    "path": os.path.dirname(rel),
                    "source_url": f"https://github.com/alirezarezvani/claude-skills/tree/main/{os.path.dirname(rel)}",
                    "version": fm.get("version"),
                    "license": fm.get("license"),
                    "author": fm.get("author"),
                    "tags": [t.strip() for t in fm.get("tags", "").strip("[]").split(",") if t.strip()],
                    "has_scripts": bool(scripts),
                    "scripts": scripts,
                    "has_references": has_refs,
                    "install": {
                        "claude_code_marketplace": "/plugin marketplace add alirezarezvani/claude-skills",
                        "manual": f"cp -r {os.path.dirname(rel)} ~/.claude/skills/",
                        "codex_manual": f"cp -r {os.path.dirname(rel)} ~/.codex/skills/",
                        "script_example": (
                            f"python3 {os.path.dirname(rel)}/scripts/{scripts[0]} --help"
                            if scripts else None
                        ),
                    },
                    "body_chars": len(body),
                })
    skills.sort(key=lambda s: s["slug"])
    return skills


def main():
    skills = collect()
    sha = subprocess.check_output(["git", "-C", REPO, "log", "-1", "--format=%H"]).decode().strip()
    date = subprocess.check_output(["git", "-C", REPO, "log", "-1", "--format=%cI"]).decode().strip()

    domains = {}
    for s in skills:
        d = domains.setdefault(s["domain"], {"domain": s["domain"], "label": s["domain_label"], "count": 0})
        d["count"] += 1

    meta = {
        "source_repo": "alirezarezvani/claude-skills",
        "source_url": "https://github.com/alirezarezvani/claude-skills",
        "license": "MIT",
        "attribution": "Skills by Alireza Rezvani, MIT licensed. This project indexes them; it does not redistribute them.",
        "snapshot_commit": sha,
        "snapshot_commit_short": sha[:7],
        "snapshot_commit_date": date,
        "indexed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "skill_count": len(skills),
        "unique_names": len({s["name"] for s in skills}),
        "domain_count": len(domains),
        "domains": sorted(domains.values(), key=lambda d: -d["count"]),
    }

    os.makedirs(OUT, exist_ok=True)
    # Slim payload for the browse/search view.
    index = [
        {k: s[k] for k in ("slug", "name", "domain", "domain_label", "description", "has_scripts")}
        for s in skills
    ]
    json.dump({"meta": meta, "skills": index}, open(f"{OUT}/index.json", "w"), indent=2)
    json.dump({"meta": meta, "skills": skills}, open(f"{OUT}/skills.json", "w"), indent=2)

    print(f"{len(skills)} skills, {meta['unique_names']} unique names, {len(domains)} domains")
    print(f"index.json  {os.path.getsize(f'{OUT}/index.json')/1024:.0f} KB")
    print(f"skills.json {os.path.getsize(f'{OUT}/skills.json')/1024:.0f} KB")
    missing = sum(1 for s in skills if not s["description"])
    print(f"missing description: {missing}")


if __name__ == "__main__":
    main()
