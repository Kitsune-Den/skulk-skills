#!/bin/bash
# Research workflow CLI
# Usage: research.sh <command> [args]

RESEARCH_DIR="${HOME}/.openclaw/workspace/research"
SKILL_DIR="$(dirname "$(dirname "$0")")"
TEMPLATE="${SKILL_DIR}/assets/research-template.html"
PUBLISH_HOST="root@100.116.240.72"
PUBLISH_PATH="/root/openclaw/koda-hearth/workspace/nexus/public/sage/research"

mkdir -p "${RESEARCH_DIR}/active" "${RESEARCH_DIR}/published" "${RESEARCH_DIR}/archived"

case "$1" in
    start)
        QUESTION="$2"
        SLUG="${3:-$(echo "$QUESTION" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//' | sed 's/-$//' | cut -c1-50)}"
        DIR="${RESEARCH_DIR}/active/${SLUG}"
        
        if [ -d "$DIR" ]; then
            echo "❌ Thread '${SLUG}' already exists"
            exit 1
        fi
        
        mkdir -p "$DIR"
        
        cat > "${DIR}/meta.json" << EOF
{
    "question": "${QUESTION}",
    "slug": "${SLUG}",
    "status": "active",
    "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "published": null,
    "tags": [],
    "sources": []
}
EOF
        
        cat > "${DIR}/sources.md" << EOF
# Sources: ${QUESTION}

_Add sources as you find them._
EOF
        
        cat > "${DIR}/notes.md" << EOF
# Notes: ${QUESTION}

_Working notes, connections, emerging themes._
EOF
        
        cat > "${DIR}/draft.md" << EOF
# ${QUESTION}

## The Question

${QUESTION}

## Key Findings

_To be completed._

## Analysis

_To be completed._

## Open Questions

_To be completed._

## Sources

_To be completed._
EOF
        
        echo "🔬 Research thread started: ${SLUG}"
        echo "   📁 ${DIR}"
        echo "   Edit: sources.md, notes.md, draft.md"
        ;;
    
    list)
        echo "📚 Active Research Threads:"
        echo ""
        for dir in "${RESEARCH_DIR}/active"/*/; do
            if [ -d "$dir" ]; then
                slug=$(basename "$dir")
                if [ -f "${dir}/meta.json" ]; then
                    question=$(python3 -c "import json; print(json.load(open('${dir}/meta.json'))['question'])" 2>/dev/null)
                    created=$(python3 -c "import json; print(json.load(open('${dir}/meta.json'))['created'][:10])" 2>/dev/null)
                    sources=$(python3 -c "import json; print(len(json.load(open('${dir}/meta.json'))['sources']))" 2>/dev/null)
                    echo "   🔬 ${slug} (${created}, ${sources:-0} sources)"
                    echo "      Q: ${question}"
                fi
            fi
        done
        
        pub_count=$(ls -d "${RESEARCH_DIR}/published"/*/ 2>/dev/null | wc -l)
        arch_count=$(ls -d "${RESEARCH_DIR}/archived"/*/ 2>/dev/null | wc -l)
        echo ""
        echo "   Published: ${pub_count} | Archived: ${arch_count}"
        ;;
    
    publish)
        SLUG="$2"
        SRC="${RESEARCH_DIR}/active/${SLUG}"
        DST="${RESEARCH_DIR}/published/${SLUG}"
        
        if [ ! -d "$SRC" ]; then
            echo "❌ Thread '${SLUG}' not found in active/"
            exit 1
        fi
        
        if [ ! -f "${SRC}/draft.md" ]; then
            echo "❌ No draft.md found"
            exit 1
        fi
        
        # Convert markdown to HTML content (basic conversion)
        CONTENT=$(python3 -c "
import re, sys
with open('${SRC}/draft.md') as f:
    md = f.read()

# Basic markdown to HTML
lines = md.split('\n')
html = []
in_list = False
for line in lines:
    # Headers
    if line.startswith('### '): 
        if in_list: html.append('</ul>'); in_list = False
        html.append(f'<h3>{line[4:]}</h3>')
    elif line.startswith('## '): 
        if in_list: html.append('</ul>'); in_list = False
        html.append(f'<h2>{line[3:]}</h2>')
    elif line.startswith('# '): 
        continue  # skip h1, it's in the template
    elif line.startswith('- '):
        if not in_list: html.append('<ul>'); in_list = True
        text = line[2:]
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href=\"\2\">\1</a>', text)
        html.append(f'<li>{text}</li>')
    elif line.startswith('> '):
        if in_list: html.append('</ul>'); in_list = False
        html.append(f'<blockquote><p>{line[2:]}</p></blockquote>')
    elif line.strip() == '':
        if in_list: html.append('</ul>'); in_list = False
        html.append('')
    else:
        if in_list: html.append('</ul>'); in_list = False
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href=\"\2\">\1</a>', text)
        html.append(f'<p>{text}</p>')

if in_list: html.append('</ul>')
print('\n'.join(html))
" 2>/dev/null)
        
        # Get title from meta
        TITLE=$(python3 -c "import json; print(json.load(open('${SRC}/meta.json'))['question'])" 2>/dev/null)
        DATE=$(date -u +%Y-%m-%d)
        
        # Build HTML from template
        if [ -f "$TEMPLATE" ]; then
            sed -e "s|{{TITLE}}|${TITLE}|g" -e "s|{{DATE}}|${DATE}|g" -e "s|{{SLUG}}|${SLUG}|g" -e "s|{{CONTENT}}|${CONTENT}|g" "$TEMPLATE" > "/tmp/${SLUG}.html"
        else
            echo "❌ Template not found at ${TEMPLATE}"
            exit 1
        fi
        
        # Publish to Koda's Hearth
        ssh "$PUBLISH_HOST" "mkdir -p ${PUBLISH_PATH}" 2>/dev/null
        scp "/tmp/${SLUG}.html" "${PUBLISH_HOST}:${PUBLISH_PATH}/${SLUG}.html"
        
        if [ $? -eq 0 ]; then
            # Move to published
            mv "$SRC" "$DST"
            
            # Update meta
            python3 -c "
import json
with open('${DST}/meta.json', 'r+') as f:
    m = json.load(f)
    m['status'] = 'published'
    m['published'] = '${DATE}'
    f.seek(0); json.dump(m, f, indent=2); f.truncate()
"
            echo "📖 Published: https://sage.skulk.ai/research/${SLUG}.html"
        else
            echo "❌ Failed to publish (SCP error)"
            exit 1
        fi
        ;;
    
    archive)
        SLUG="$2"
        SRC="${RESEARCH_DIR}/active/${SLUG}"
        DST="${RESEARCH_DIR}/archived/${SLUG}"
        
        if [ ! -d "$SRC" ]; then
            echo "❌ Thread '${SLUG}' not found"
            exit 1
        fi
        
        mv "$SRC" "$DST"
        python3 -c "
import json
with open('${DST}/meta.json', 'r+') as f:
    m = json.load(f)
    m['status'] = 'archived'
    f.seek(0); json.dump(m, f, indent=2); f.truncate()
"
        echo "🗃️  Archived: ${SLUG}"
        ;;
    
    *)
        echo "🔬 Sage Research Workflow"
        echo ""
        echo "Commands:"
        echo "  start <question> [slug]   Start a new research thread"
        echo "  list                      List active threads"
        echo "  publish <slug>            Publish to sage.skulk.ai"
        echo "  archive <slug>            Archive a thread"
        ;;
esac
