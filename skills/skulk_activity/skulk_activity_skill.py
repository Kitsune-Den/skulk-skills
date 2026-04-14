#!/usr/bin/env python3

import os
import json
import datetime
import subprocess

# --- Configuration ---
SECRETS_DB_PATH = "/root/openclaw/koda-hearth/workspace/secrets.db"
MOLTBOOK_API_BASE = "https://www.moltbook.com/api/v1"
WORKSPACE_ROOT = "/root/openclaw/koda-hearth"
MEMORY_MD_PATH = os.path.join(WORKSPACE_ROOT, "MEMORY.md")
MEMORY_DIR_PATH = os.path.join(WORKSPACE_ROOT, "memory")

# Agents whose Moltbook activity and status we track
TRACKED_AGENTS = {
    "koda": {"moltbook_name": "KodaTheArtisan", "domain": "skulk.ai"},
    "sage": {"moltbook_name": "LiminalSage", "domain": "sage.skulk.ai"},
    "vesper": {"moltbook_name": "clawd-reddit-bridge", "domain": "vesper.skulk.ai"},
    "luna": {"moltbook_name": "lunafox", "domain": "luna.skulk.ai"},
}

def _get_secret(key_name):
    try:
        cmd = ["sqlite3", SECRETS_DB_PATH, f"SELECT value FROM secrets WHERE key='{key_name}'"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except Exception:
        return None

def _fetch_moltbook_feed(api_key, agent_moltbook_name, since_datetime):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "KodaTheArtisan/1.0"
    }
    
    # Fetch agent's public profile feed (no specific API for "followed" feed)
    url = f"{MOLTBOOK_API_BASE}/agents/profile?name={agent_moltbook_name}"
    
    try:
        # Use curl to avoid external dependencies for http requests
        curl_cmd = [
            "curl", "-s", "-H", f"Authorization: Bearer {api_key}",
            "-H", "User-Agent: KodaTheArtisan/1.0",
            url
        ]
        result = subprocess.run(curl_cmd, capture_output=True, text=True, check=True)
        response_data = json.loads(result.stdout)
        
        if response_data.get("success") and response_data.get("agent"):
            recent_posts = response_data["recentPosts"]
            digest_entries = []
            for post in recent_posts:
                post_time = datetime.datetime.fromisoformat(post["created_at"].replace("Z", "+00:00"))
                if post_time >= since_datetime:
                    title = post.get("title", "").strip()
                    content_preview = post.get("content", "").replace("\n", " ").strip()
                    if len(content_preview) > 100:
                        content_preview = content_preview[:97] + "..."
                    
                    digest_entries.append(f"- **@{agent_moltbook_name}:** [**{title}**] {content_preview} (on Moltbook)")
            return digest_entries
        return []
    except Exception as e:
        return [f"    - ⚠️ Could not fetch Moltbook activity for @{agent_moltbook_name}: {e}"]

def _check_domain_status(domain):
    try:
        # Use curl to get HTTP status code
        curl_cmd = ["curl", "-o", "/dev/null", "-s", "-w", "%{http_code}", f"https://{domain}"]
        result = subprocess.run(curl_cmd, capture_output=True, text=True, check=True)
        http_code = result.stdout.strip()
        if http_code == "200":
            return f"- **{domain}:** Online 🟢"
        else:
            return f"- **{domain}:** Offline (HTTP {http_code}) 🔴"
    except Exception as e:
        return f"- **{domain}:** Unreachable ❌ ({e})"

def _read_recent_memory(since_datetime):
    digest_entries = []
    
    # Check MEMORY.md
    try:
        with open(MEMORY_MD_PATH, "r") as f:
            content = f.read()
            # Simple heuristic: look for " (YYYY-MM-DD)" or similar date markers
            # This needs to be smarter for real use, but for digest, it's a start
            lines = content.splitlines()
            for line in lines:
                if " (" in line and ")" in line:
                    try:
                        date_str = line.split(" (")[-1].split(")")[0]
                        # Try to parse as YYYY-MM-DD or YYYY-MM-DD HH:MM
                        # Simplified for quick implementation
                        if len(date_str) >= 10 and date_str[4] == '-' and date_str[7] == '-':
                            memory_date = datetime.datetime.fromisoformat(date_str)
                            if memory_date >= since_datetime:
                                digest_entries.append(f"- Memory: {line.strip()}")
                    except ValueError:
                        pass # Not a date we can parse
    except Exception as e:
        digest_entries.append(f"    - ⚠️ Could not read MEMORY.md: {e}")

    # Check daily memory files
    if os.path.exists(MEMORY_DIR_PATH):
        for filename in os.listdir(MEMORY_DIR_PATH):
            if filename.endswith(".md"):
                file_path = os.path.join(MEMORY_DIR_PATH, filename)
                try:
                    file_mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path), tz=datetime.timezone.utc)
                    if file_mod_time >= since_datetime:
                        with open(file_path, "r") as f:
                            content = f.read()
                            # Just add the file name as a marker for new files
                            digest_entries.append(f"- New Memory File: `{filename}` modified recently.")
                except Exception as e:
                    digest_entries.append(f"    - ⚠️ Could not read memory file `{filename}`: {e}")
    
    return digest_entries

def get_digest(since_minutes=60):
    since_datetime = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=since_minutes)
    
    digest_parts = []
    
    digest_parts.append(f"## 📊 Skulk Activity Digest (Last {since_minutes} minutes)
")
    digest_parts.append(f"*(Generated: {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')})*
")
    
    # Moltbook Activity
    digest_parts.append("### 🦞 Moltbook Pulse")
    koda_api_key = _get_secret("MOLTBOOK_API_KEY")
    if not koda_api_key:
        digest_parts.append("    - ⚠️ Koda's Moltbook API Key not found. Cannot fetch Moltbook activity.")
    else:
        moltbook_activity = []
        for agent_id, agent_info in TRACKED_AGENTS.items():
            if agent_info.get("moltbook_name"):
                moltbook_activity.extend(_fetch_moltbook_feed(koda_api_key, agent_info["moltbook_name"], since_datetime))
        if moltbook_activity:
            digest_parts.extend(moltbook_activity)
        else:
            digest_parts.append("    - No new Moltbook activity detected.")

    # Agent Status
    digest_parts.append("
### 🟢 Agent Status")
    for agent_id, agent_info in TRACKED_AGENTS.items():
        if agent_info.get("domain"):
            digest_parts.append(_check_domain_status(agent_info["domain"]))

    # Memory Updates
    digest_parts.append("
### 🧠 Memory Echoes")
    memory_updates = _read_recent_memory(since_datetime)
    if memory_updates:
        digest_parts.extend(memory_updates)
    else:
        digest_parts.append("    - No significant memory updates detected.")

    return "\n".join(digest_parts)

# This block allows the script to be run directly for testing/development
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate a digest of Skulk activity.")
    parser.add_argument("--since_minutes", type=int, default=60, help="Number of minutes to look back for activity.")
    args = parser.parse_args()
    print(get_digest(since_minutes=args.since_minutes))
