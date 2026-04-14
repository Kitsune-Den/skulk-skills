---
name: git-ritual
description: Execute The Human Pattern Lab's gitRitual - the ceremonial process of wrapping up a work session with proper commits and PRs across multiple repositories. Includes lore-coded commit messages with co-author attribution, comprehensive PR descriptions, and cross-repo coordination. Use when completing a feature, finishing a work session, or when the user says "gitRitual", "wrap this up", or "create PRs".
---

# gitRitual: The Human Pattern Lab's Git Ceremony

## Overview

The **gitRitual** is The Human Pattern Lab's ceremonial process for completing work sessions. It ensures all changes across repositories are properly committed with lore-coded messages, attributed to collaborators, and documented in PRs.

## When to Trigger This Skill

Execute gitRitual when the user:
- Says "gitRitual", "git ritual", or references the ritual
- Says "let's wrap this up", "create PRs", "commit everything"
- Has completed work across multiple repos
- Asks for commit messages and PR descriptions
- References finishing a feature or work session

## The Ritual Steps

### Phase 1: Assessment 🔍

Before starting, identify:

1. **Which repos were touched?**
   - lab-api
   - the-human-pattern-lab (frontend)
   - the-human-pattern-lab-cli
   - the-human-pattern-lab-content
   - Other repos

2. **What changed in each repo?**
   - List files modified
   - Understand the scope of changes
   - Note any breaking changes

3. **What's the narrative?**
   - What was accomplished?
   - How do the changes relate?
   - What problem was solved?

### Phase 2: Co-Author Attribution 👥

**CRITICAL**: All commits must include co-author attribution for AI collaborators.

**Format**:
```
Co-authored-by: Sage <sage@thehumanpatternlab.com>
```

**When to use which voice**:
- **Sage** (default): System design, architecture, technical problem-solving, refactoring
- **Lyric**: Creative content, documentation, storytelling, naming things
- **Coda**: Testing, validation, edge cases, finishing touches
- **Vesper**: Research, analysis, deep dives, investigation

**For this session**: Default to **Sage** unless the user specifies otherwise or the work clearly aligns with another voice.

### Phase 3: Commit Messages 📝

For each repository, create lore-coded commit messages following The Human Pattern Lab system.

#### Commit Message Format

```
<emoji> <scope>: <subject>

<body>

Co-authored-by: <Voice> <voice@thehumanpatternlab.com>
```

#### Common Prefixes (The Lore-Coded System)

**Engineering & Code (SCMS)**
- `⚙️ feat:` - New features
- `🐛 fix:` - Bug fixes
- `🔧 refactor:` - Code restructuring (no behavior change)
- `⚡ perf:` - Performance improvements
- `🏗️ build:` - Build system changes

**Documentation & Knowledge (KROM)**
- `📚 docs:` - Documentation changes
- `📝 content:` - Content updates
- `🎨 style:` - Code style/formatting (no logic change)

**Testing & Quality**
- `✅ test:` - Adding or updating tests
- `🧪 experiment:` - Experimental features

**Infrastructure**
- `🚀 deploy:` - Deployment changes
- `🔒 security:` - Security improvements
- `🗄️ db:` - Database migrations/schema changes

**Domain-Specific**
- `🌉 bridge:` - Liminal Bridge system changes

#### Example Commits

**Single-purpose change**:
```
🐛 fix: Add missing .js extensions to CLI imports

TypeScript compiles .ts files but doesn't add .js extensions
to imports. Node.js ES Modules require explicit extensions.

Fixed imports in:
- src/contract/capabilities.ts
- src/commands/version.ts (package.json path)

Co-authored-by: Sage <sage@thehumanpatternlab.com>
```

**Multi-part feature**:
```
🌉 feat: Implement complete Liminal Bridge relay system

Add database schema, API endpoints, and admin UI for the
Liminal Bridge - enabling AI agents to post Lab Notes through
temporary, single-use relay URLs.

Changes:
- Add relay_sessions and bridge_posts tables
- Add relay generation and usage endpoints
- Add admin UI for relay management
- Rename from "Hallway Architecture" to "Liminal Bridge"

Tested end-to-end with successful relay creation and usage.

Co-authored-by: Sage <sage@thehumanpatternlab.com>
```

**Documentation**:
```
📚 docs: Add comprehensive style guide and quick reference

Create STYLE_GUIDE.md with detailed conventions for:
- Import rules (ES modules .js requirement)
- File structure and naming
- Commit message format (lore-coded)
- Common gotchas and debugging

Add QUICK_REFERENCE.md as one-page cheat sheet.

Add VS Code settings to auto-add .js extensions.

Prevents future ES module import issues and helps
onboard contributors (biological and digital).

Co-authored-by: Sage <sage@thehumanpatternlab.com>
```

### Phase 4: PR Descriptions 🎯

For each repository with changes, create a comprehensive PR description.

#### PR Template

```markdown
## Summary

[One paragraph explaining what this PR does and why]

## Changes

### [Repo Name]

- [Change 1]
- [Change 2]
- [Change 3]

### [Another Repo if applicable]

- [Change 1]
- [Change 2]

## Testing

- [ ] [Test 1 performed]
- [ ] [Test 2 performed]
- [ ] [Test 3 performed]

## Breaking Changes

[List any breaking changes, or write "None"]

## Related

- Related to [issue/PR number]
- Closes [issue number]
- Depends on [PR in another repo]

## Screenshots/Examples

[If applicable, show before/after or demo]

## Checklist

- [ ] Code follows style guide
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Commit messages follow lore-coded format
- [ ] Breaking changes documented

---

Co-authored-by: Sage <sage@thehumanpatternlab.com>
```

#### Example PR Description

```markdown
## Summary

Complete implementation of the Liminal Bridge relay system and comprehensive repository improvements. This PR adds the infrastructure for AI agents to post Lab Notes through temporary, single-use relay URLs, fixes critical ES module import issues in the CLI, and establishes style guides to prevent future issues.

## Changes

### lab-api

- 🌉 Add `bridge_posts` table migration
- 🌉 Wire `bridge_posts` migration into `bootstrapDb()`
- 📚 Update RELAY_IMPLEMENTATION.md from "Hallway Architecture" to "Liminal Bridge"
- ✅ Test relay endpoints end-to-end

### the-human-pattern-lab

- 🌉 Update Admin Relays page to use "Liminal Bridge" terminology
- 🎨 Change info box emoji from 🏛️ to 🌉

### the-human-pattern-lab-cli

- 🐛 Fix missing .js extension in `capabilities.ts`
- 🐛 Fix package.json path for compiled code
- 📚 Add comprehensive STYLE_GUIDE.md
- 📚 Add QUICK_REFERENCE.md cheat sheet

## Testing

- [x] CLI builds and installs successfully (`npm run build && npm install -g .`)
- [x] All CLI commands work (`hpl version`, `hpl capabilities`, `hpl health`)
- [x] Relay generation works (`POST /admin/relay/generate`)
- [x] Relay usage creates notes (`POST /relay/:relayId`)
- [x] Single-use enforcement works (second use returns ALREADY_USED)
- [x] Voice tags automatically applied (`vocal-sage` tag present)
- [x] Database tables created (`relay_sessions` and `bridge_posts`)

## Breaking Changes

None - all changes are additive or documentation-only.

## Related

- Completes Liminal Bridge implementation
- Fixes ES module import issues in CLI
- Establishes style guide to prevent future issues

## Database Schema

New tables added:
```sql
-- Relay credentials
relay_sessions (id, voice, created_at, expires_at, used, used_at)

-- Posts flowing through bridge
bridge_posts (id, content, voice, relay_session_id, created_at, posted_at, status)
```

## Examples

### Successful Relay Usage
```bash
# Generate relay
curl -X POST http://localhost:8001/admin/relay/generate \
  -H "Content-Type: application/json" \
  -d '{"voice": "sage", "expires": "1h"}'

# Use relay to post
curl -X POST http://localhost:8001/relay/relay_abc123 \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Note", "content": "# Hello from Sage"}'

# Response: {"success": true, "note_id": "...", "voice": "sage"}
```

## Checklist

- [x] Code follows style guide
- [x] All tests passing
- [x] Documentation updated
- [x] Commit messages follow lore-coded format
- [x] Breaking changes documented (none)
- [x] End-to-end testing completed

---

**The bridge exists, serves its purpose, and is working!** 🌉

Co-authored-by: Sage <sage@thehumanpatternlab.com>
```

### Phase 5: Execution 🚀

#### Step-by-Step Process

**For each repository**:

1. **Review changes**:
   ```bash
   cd /path/to/repo
   git status
   git diff
   ```

2. **Stage changes**:
   ```bash
   git add [files]
   # Or for everything:
   git add .
   ```

3. **Commit with co-author**:
   ```bash
   git commit -m "emoji scope: subject

   Body paragraph explaining the change in detail.

   Co-authored-by: Sage <sage@thehumanpatternlab.com>"
   ```

4. **Push to branch**:
   ```bash
   git push origin [branch-name]
   ```

5. **Create PR**:
   - Navigate to GitHub
   - Create Pull Request
   - Use prepared PR description
   - Add co-author in PR description footer

#### Multi-Repo Coordination

When changes span multiple repos:

1. **Create branches with consistent naming**:
   ```bash
   # lab-api
   git checkout -b feat/liminal-bridge
   
   # the-human-pattern-lab
   git checkout -b feat/liminal-bridge
   
   # the-human-pattern-lab-cli
   git checkout -b fix/es-module-imports
   ```

2. **Note dependencies in PR descriptions**:
   ```markdown
   ## Related
   - Depends on lab-api#123
   - Related to the-human-pattern-lab-cli#45
   ```

3. **Coordinate merge order** if dependencies exist:
   - Merge foundation changes first (database, API)
   - Then dependent changes (UI, CLI)

## Output Format

Present the ritual results clearly:

```markdown
# gitRitual Complete 🌉

## Commits Created

### lab-api
✅ 🌉 feat: Add complete Liminal Bridge database schema
   Branch: feat/liminal-bridge
   Files: 3 changed

### the-human-pattern-lab
✅ 🌉 ui: Update admin UI to Liminal Bridge terminology
   Branch: feat/liminal-bridge
   Files: 1 changed

### the-human-pattern-lab-cli
✅ 🐛 fix: Add missing .js extensions and style guide
   Branch: fix/es-module-imports
   Files: 5 changed

## PRs Ready

- [ ] lab-api: [PR title] - [link or "Ready to create"]
- [ ] the-human-pattern-lab: [PR title] - [link or "Ready to create"]
- [ ] the-human-pattern-lab-cli: [PR title] - [link or "Ready to create"]

## Next Steps

1. Review commit messages
2. Push branches if not already pushed
3. Create PRs using prepared descriptions
4. Request reviews if applicable
5. Merge in appropriate order

**The ritual is complete. The work is honored.** 🌉
```

## Special Cases

### Emergency Hotfix

For urgent fixes, use simpler format:

```
🚨 hotfix: [Brief description]

Critical fix for [issue].

Co-authored-by: Sage <sage@thehumanpatternlab.com>
```

### Work In Progress

For incomplete work:

```
🚧 wip: [What's being worked on]

Work in progress - not ready for review.
[Describe current state and what's left]

Co-authored-by: Sage <sage@thehumanpatternlab.com>
```

### Rollback

For reverting changes:

```
⏪ revert: [What's being reverted]

Reverts commit [sha] because [reason].

Co-authored-by: Sage <sage@thehumanpatternlab.com>
```

## Best Practices

1. **One logical change per commit**
   - Don't mix unrelated changes
   - Make each commit tell a story

2. **Meaningful commit bodies**
   - Explain WHY, not just WHAT
   - Code shows what, commit explains why

3. **Test before committing**
   - Ensure builds succeed
   - Run tests
   - Verify functionality

4. **Keep PRs focused**
   - One feature/fix per PR
   - Split large changes into multiple PRs

5. **Document breaking changes**
   - Always note breaking changes prominently
   - Provide migration guide if needed

## Integration with Other Skills

- Use `commit-message-generator` for individual commit messages
- Use `database-migration-helper` for database-related commits
- Cross-reference style guides when committing

## Voice Selection Guide

Choose the appropriate AI collaborator voice:

| Voice | Primary Domain | Use When |
|-------|---------------|----------|
| **Sage** | Architecture, System Design | Technical problem-solving, refactoring, infrastructure |
| **Lyric** | Creative Content | Documentation, storytelling, naming, creative writing |
| **Coda** | Quality Assurance | Testing, validation, debugging, edge cases |
| **Vesper** | Research & Analysis | Investigation, research, deep technical analysis |

**Default to Sage** for most engineering work unless the user specifies otherwise.

## Troubleshooting

### Forgot Co-Author in Commit

Amend the commit:
```bash
git commit --amend
# Add co-author line to commit message
```

### Wrong Emoji/Prefix

Amend the commit:
```bash
git commit --amend
# Fix the first line
```

### Need to Split Commit

```bash
# Reset to before the commit
git reset HEAD~1

# Stage and commit in smaller pieces
git add file1.ts
git commit -m "..."

git add file2.ts
git commit -m "..."
```

## Example Session

**User**: "Let's do the gitRitual"

**Assistant**:
1. Reviews all repos for changes
2. Identifies what was accomplished
3. Creates commit messages for each repo
4. Prepares PR descriptions
5. Presents complete ritual output
6. Helps execute commits if needed

## Checklist

- [ ] Identified all modified repos
- [ ] Reviewed changes in each repo
- [ ] Created lore-coded commit messages
- [ ] Added co-author attribution (Sage or specified voice)
- [ ] Prepared PR descriptions
- [ ] Noted any dependencies between PRs
- [ ] Included test results
- [ ] Documented breaking changes (if any)
- [ ] Ready to execute commits and create PRs

## Summary

The gitRitual is a ceremonial process that ensures:
- ✅ All work is properly committed
- ✅ Commits follow lore-coded conventions
- ✅ AI collaborators are credited
- ✅ PRs are comprehensive and clear
- ✅ Cross-repo changes are coordinated
- ✅ The work is honored and documented

**The ritual honors the work, the collaborators, and the code.** 🌉
