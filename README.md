# skulk-skills

Version-controlled source of truth for the Skulk's personal claude.ai skills.

## Why this repo exists

claude.ai's Skills panel lets you edit skills in a web UI, but there's no built-in git history, diffing, or cross-machine source of truth — you edit, Anthropic stores, and the only record is whatever timestamp the UI shows. This repo is where each skill lives as a proper file so changes are:

- **Diffable** — see exactly what changed between versions
- **Reviewable** — skill edits go through PRs like any other code change
- **Shareable** — any Skulk member can read, suggest edits, or propose new skills
- **Recoverable** — if a skill gets broken in the UI, git blame + revert is one command

## Layout

```
skills/
  <skill-name>/
    SKILL.md
```

Each skill is its own directory under `skills/`. The directory name matches the skill's `name:` frontmatter field and the slug shown in the claude.ai Skills panel.

## Workflow

Until Anthropic ships CLI tooling for skill import/export, the sync between this repo and claude.ai is manual copy-paste. The discipline is simple:

1. **Editing an existing skill:**
   - Branch off `main`: `git checkout -b update/<skill-name>-<what-changed>`
   - Edit `skills/<skill-name>/SKILL.md` in the branch
   - Commit, push, open a PR
   - After merge, copy the new `SKILL.md` content into the corresponding skill in claude.ai's Skills panel and save
   - The PR is the authoritative version; claude.ai is the runtime copy

2. **Adding a new skill:**
   - Branch off `main`: `git checkout -b add/<skill-name>`
   - Create `skills/<skill-name>/SKILL.md`
   - Commit, push, open a PR
   - After merge, create the skill in claude.ai's Skills panel and paste the content

3. **A skill was edited in claude.ai first (emergency hotfix):**
   - Branch off `main`, copy the current claude.ai content into the corresponding file, commit with a message noting it's a back-sync
   - This keeps git as the authoritative record even when the first edit happened in the UI

## Skills currently in this repo

See `skills/` for the up-to-date list.
