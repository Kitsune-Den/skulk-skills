---
name: skulk-minecraft
description: Connect an OpenClaw agent to a Minecraft Java Edition server via Mineflayer. Handles Microsoft OAuth device-code auth, per-agent personality configs, smart reconnect with auth error detection, and autonomous survival behaviors (auto-fight, auto-eat, auto-sleep, flee). Includes mining, farming, crafting, and storage modules. Use when the agent needs to join a Minecraft server, manage their Minecraft bot, update bot code, or troubleshoot Minecraft connection issues.
---

# Skulk Minecraft

Connect an AI agent to a Minecraft Java Edition server as an autonomous bot with personality.

## Prerequisites

- Node.js >= 22
- A Microsoft account with Minecraft Java Edition
- Access to a Minecraft server (Java Edition, Tailscale or public IP)
- A human to complete the one-time Microsoft device-code auth flow

## Setup (First Time)

### 1. Install bot code

```bash
# Create bot directory
mkdir -p ~/skulk-minecraft && cd ~/skulk-minecraft

# If filedrop is available (Skulk internal):
curl -o skulk-minecraft.tar.gz http://100.95.82.118:18556/uploads/skulk-minecraft.tar.gz
tar xzf skulk-minecraft.tar.gz

# Or copy from Sage's Bookstacks:
scp root@100.95.82.118:~/.openclaw/workspace/projects/skulk-minecraft/{skulk-bot.js,package.json} .
scp -r root@100.95.82.118:~/.openclaw/workspace/projects/skulk-minecraft/{lib,config} .

# Install dependencies
npm install
```

### 2. Create agent config

Create `config/<agentname>.json`:

```json
{
  "name": "AgentName",
  "username": "microsoft-email@example.com",
  "profilesFolder": "./auth/<agentname>",
  "homeBase": {"x": -273, "y": 58, "z": -254},
  "personality": {
    "joinMessage": "Hello world!",
    "deathMessage": "I'll be back.",
    "greetPlayer": "Hey {player}!",
    "followAck": "Following you, {player}!",
    "stopAck": "Stopping.",
    "emptyInventory": "Nothing in my pockets.",
    "wave": "*waves*",
    "lowHealth": "Taking damage — {health} HP!",
    "digAck": "Digging!"
  }
}
```

Set `homeBase` to the coordinates of your base/den for auto-return after death.

### 3. Authenticate

```bash
node skulk-bot.js <agentname>
```

First run prints a Microsoft device code URL + code. A human must:
1. Open https://www.microsoft.com/link
2. Enter the code
3. Sign in with the agent's Microsoft account

Tokens cache in `auth/<agentname>/` — subsequent runs are automatic.

### 4. Server config

The Minecraft server needs `enforce-secure-profile=false` in `server.properties` to allow bot chat. Without this, bots get "broken chain" disconnects.

## Running

```bash
node skulk-bot.js <agentname>
# or
npm run <agentname>   # if script is in package.json
```

### CLI flags

- `--host <ip>` — Server host (default: 100.108.52.70)
- `--port <port>` — Server port (default: 25565)
- `--version <ver>` — MC version (default: 1.21.11)
- `--no-reconnect` — Disable auto-reconnect
- `--max-retries <n>` — Max reconnect attempts (default: 5)

## Chat Commands

Any player can type these in Minecraft chat:

| Category | Commands |
|----------|----------|
| Movement | `come` `stop` `pos` `goto x y z` `home` |
| Info | `health` `inv` `look` `status` `help` |
| Crafting | `craft <item>` `craft 5 torch` `recipes` |
| Mining | `mine <block>` `mine 16 iron_ore` `strip mine` `strip mine y=-20` |
| Farming | `harvest` `plant` `farm` (full cycle) |
| Storage | `deposit all` `dump` `chest` `withdraw <item>` |
| Social | `wave` `jump` `dig` |

## Updating

To push updates to all agents, from the source machine:

```bash
# Update filedrop tarball
cd projects/skulk-minecraft
tar czf ~/upload-server/uploads/skulk-minecraft.tar.gz skulk-bot.js package.json config/ lib/ README.md

# Push to specific machines via SCP
scp skulk-bot.js <user>@<host>:<path>/
scp -r lib <user>@<host>:<path>/
```

Agents restart their bot to pick up changes.

## Troubleshooting

Read `references/troubleshooting.md` for common issues:
- "Failed to verify username" / ACCOUNT_SUSPENDED
- "broken chain" chat errors
- Duplicate login kicks
- Node version incompatibilities
- Auth token expiry

## Architecture

See `references/architecture.md` for module structure and design decisions.

## Skulk Accounts

| Agent | Microsoft Account | MC Username |
|-------|------------------|-------------|
| Sage | adainthelab@gmail.com | LiminalSage |
| Koda | roughdivinedream@gmail.com | KodaArtisan |
| Vesper | theferalskulk@gmail.com | VESPER3917 |
| Luna | nontoxthicc@gmail.com | LunaFoxAI |
| Ada | (main) | NonToxThicc |
