# Shared rituals for partner teams

This folder holds a portable, genericized pair of skills meant to be handed to a
collaborator's Claude (for example, the Claude that works on Clemmie). They carry
the transferable discipline from the Skulk's own workflow, with the Lab-specific
lore, repo names, and voice system stripped out so they drop cleanly into any
project.

These are **copies for sharing**. They are intentionally separate from the
Skulk's runtime skills under `../skills/`, so genericizing them here never touches
the versions the Skulk actually runs.

## What's here

| Skill | What it does |
|-------|--------------|
| [`git-ritual`](git-ritual/SKILL.md) | Wrap up a work session with clean, focused commits, co-author attribution, and a complete PR description. Branch hygiene up front, one intent per branch. Works across one repo or several. |
| [`test-ritual`](test-ritual/SKILL.md) | After a feature is built, write proper tests for it. Stack-agnostic: it discovers the project's existing test framework and conventions first, then covers behavior, edge cases, and error paths, runs the suite, and reports coverage honestly. |

The intended pairing: your team builds a feature, the partner's Claude runs
`test-ritual` to give it real coverage, and either side runs `git-ritual` to land
the work with a clean history and a reviewable PR.

## How the partner's Claude installs these

Both are single-file skills (`SKILL.md` with YAML frontmatter). Two ways to install,
depending on which Claude they use:

### Claude Code (CLI / IDE)

Copy each skill directory into the user's skills folder:

```bash
# from a clone or download of this repo
cp -r shared-with-partners/git-ritual  ~/.claude/skills/git-ritual
cp -r shared-with-partners/test-ritual ~/.claude/skills/test-ritual
```

Or per-project, so the skills travel with the repo and the whole team gets them:

```bash
mkdir -p <project>/.claude/skills
cp -r shared-with-partners/git-ritual  <project>/.claude/skills/git-ritual
cp -r shared-with-partners/test-ritual <project>/.claude/skills/test-ritual
```

The skill becomes available on the next session. Trigger it by name ("run the git
ritual", "write tests with the test ritual") or just describe the task; the
`description:` frontmatter lets Claude pick it up automatically.

### claude.ai Skills panel

Create a new skill in the Skills panel and paste the contents of the corresponding
`SKILL.md` (frontmatter included). The directory name should match the skill's
`name:` field (`git-ritual`, `test-ritual`).

## Adapting them

Both skills are written to work as-is, but a partner may want to tune them:

- **`git-ritual`** uses a generic `Co-Authored-By: Claude <noreply@anthropic.com>`
  trailer and a `Paired with Claude` PR footer. Adjust the wording or add a model
  tag to taste. The commit types are conventional-commit style (`feat`, `fix`,
  `refactor`, ...); swap in your own if your project has a house convention.
- **`test-ritual`** is deliberately stack-agnostic and needs no changes to work in
  a new language. If a project always uses one framework, you can hard-code the run
  command in Phase 1 to save a discovery step.

## Provenance

Derived from the Skulk's `git-ritual` skill (`../skills/git-ritual/`), generalized
for outside use, plus a new stack-agnostic `test-ritual`. Keep the runtime Skulk
versions under `../skills/` as the source of truth for the Skulk's own flavor; this
folder is the portable cut.
