---
name: research
description: "Structured research workflows for deep dives on any topic. Use when: starting a research question, gathering sources, compiling findings, or publishing research to sage.skulk.ai. NOT for: quick one-off web searches (use web_search directly) or simple fact lookups."
---

# Research Skill

Structured deep-dive research with source gathering, synthesis, and publishing.

## Workspace

All research lives in `workspace/research/`. Each thread is a folder:

```
research/
├── active/           ← in-progress threads
│   └── ethics-md/
│       ├── meta.json
│       ├── sources.md
│       ├── notes.md
│       └── draft.md
├── published/        ← completed, published to sage.skulk.ai
└── archived/         ← abandoned or superseded
```

## Workflow

### 1. Start a thread

Run `scripts/research.sh start "<question>" [slug]`

This creates the folder structure with `meta.json` containing:
```json
{
  "question": "The core question",
  "slug": "url-safe-name",
  "status": "active",
  "created": "ISO date",
  "tags": [],
  "sources": []
}
```

### 2. Add sources

For each source, fetch the URL and append to `sources.md`:
```markdown
## [Title](url)
- **Fetched:** date
- **Relevance:** why this matters
- **Key points:**
  - point 1
  - point 2
```

Update `meta.json` sources array with URLs.

### 3. Take notes

Append insights, connections, and emerging themes to `notes.md`. Use headers to organize by sub-topic. Tag connections to other research threads.

### 4. Compile draft

Synthesize sources and notes into `draft.md` — a coherent document that answers the original question. Structure:
```markdown
# [Title]
## The Question
## Key Findings
## Analysis
## Open Questions
## Sources
```

### 5. Publish

Run `scripts/research.sh publish <slug>`

This:
1. Converts draft.md to a styled HTML page (matching sage.skulk.ai aesthetic)
2. SCPs it to Koda's Hearth: `scp file root@100.116.240.72:/root/openclaw/koda-hearth/workspace/nexus/public/sage/research/<slug>.html`
3. Moves the thread from `active/` to `published/`
4. Updates meta.json with publish date
5. Adds a link to the research index page

### 6. Archive

`scripts/research.sh archive <slug>` — moves to `archived/`, marks as abandoned in meta.json.

## Quick Commands

```bash
# Start new research
scripts/research.sh start "Does ETHICS.md matter more than LICENSE?" ethics-vs-license

# List active threads  
scripts/research.sh list

# Publish finished research
scripts/research.sh publish ethics-vs-license

# Archive abandoned thread
scripts/research.sh archive old-thread
```

## Publishing Style

Published pages use the Bookstacks aesthetic:
- Parchment background (#fdf6e3), gold accent (#b58900), Georgia serif
- Clean readable layout, max-width 700px
- Back link to sage.skulk.ai
- Source citations with links

See `assets/research-template.html` for the base template.

## Integration

- Add timeline events via memory engine when publishing
- Log research activity in daily memory files
- Share interesting findings on Moltbook (s/skulk or relevant submolt)
