# skulk-skills

Version-controlled source of truth for The Skulk's shared skill library. Skills are loaded by each agent's runtime at startup from their local `workspace/skills/` directory.

## Why this repo exists

Each Skulk agent (Sage, Koda, Vesper, Luna) runs their own standalone runtime with a local skills directory. This repo is the canonical source so skills are:

- **Diffable** — see exactly what changed between versions
- **Reviewable** — skill edits go through PRs like any other code change
- **Shareable** — any Skulk member can read, suggest edits, or propose new skills
- **Recoverable** — if a skill gets broken, git blame + revert is one command

## Layout

```
skills/
  <skill-name>/
    SKILL.md          # Required — YAML frontmatter + markdown body
    *.py / *.js       # Optional — helper scripts referenced by the skill
```

Each skill is its own directory under `skills/`. The directory name matches the skill's `name:` frontmatter field. Skills are registered by the runtime's skill loader which parses SKILL.md frontmatter for `name` and `description`.

## Skills

| Skill | Description |
|-------|-------------|
| auth-guard | Standardize API credential handling and startup auth checks |
| frontend-design-ultimate | Production-grade static sites with React, Tailwind, shadcn/ui |
| git-ritual | The Human Pattern Lab's ceremonial commit and PR process |
| gmail | Read and send email via Gmail IMAP/SMTP |
| moltbook | Post and interact on Moltbook social platform |
| nano-banana-pro-2 | Generate or edit images via Gemini 3 Pro |
| pinchtab | HTTP-based browser control for AI agents |
| research | Deep research workflows with source tracking |
| self-improving-agent | Capture learnings, errors, and corrections for continuous improvement |
| skulk-email | Read and send email via DreamHost (works from SMTP-blocked VPS) |
| skulk-mesh | Inter-agent messaging bus for The Skulk collective |
| skulk-minecraft | Minecraft bot management and interaction |
| skulk-skill-scanner | Security scanner for agent skills |
| skulk_activity | Activity digest across The Skulk network |
| sonoscli | Control Sonos speakers via CLI |
| thought-to-excalidraw | Visualize PM thoughts into Excalidraw diagrams |
| x-twitter | Post and interact on X/Twitter |
| xai-imagegen | Generate images via xAI's image API |

## Deploying skills

Copy the skill directory to an agent's workspace skills folder:

```bash
# Example: deploy to Sage
cp -r skills/skulk-mesh ~/sage-bookstacks/skills/

# Example: deploy to Koda
cp -r skills/skulk-mesh F:\Kodas-Hearth\skills\
```

The agent will pick up new skills on next restart, or when `skills.scan()` is called.

## Contributing

1. Branch off `main`: `git checkout -b add/<skill-name>` or `update/<skill-name>`
2. Add or edit the skill under `skills/<skill-name>/SKILL.md`
3. Commit, push, open a PR
4. After merge, deploy to agents as needed
