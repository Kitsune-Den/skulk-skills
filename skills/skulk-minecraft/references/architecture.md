# Architecture

## File Structure

```
skulk-minecraft/
├── skulk-bot.js          — Main bot entry point (shared core)
├── package.json          — Dependencies (mineflayer, mineflayer-pathfinder)
├── config/               — Per-agent personality configs
│   ├── sage.json
│   ├── koda.json
│   ├── vesper.json
│   └── luna.json
├── lib/                  — Feature modules
│   ├── survival.js       — Auto-respawn, return to base, enhanced eating
│   ├── crafting.js       — Recipe system, auto-equip best tool
│   ├── mining.js         — Block mining, strip mining, resource gathering
│   ├── farming.js        — Harvest, plant, farm cycle
│   └── storage.js        — Chest deposit/withdraw/list
├── auth/                 — Per-agent Microsoft auth tokens (gitignored)
│   ├── sage/
│   ├── koda/
│   ├── vesper/
│   └── luna/
└── legacy/               — Old single-bot scripts (preserved)
    ├── bot.js
    ├── vesper-bot.js
    ├── build-den.js
    ├── dig-den.js
    └── ...
```

## Design Decisions

### One bot, many personalities
Instead of separate bot files per agent, all agents share `skulk-bot.js` with personality-specific configs in `config/<agent>.json`. This means bug fixes and features deploy to everyone at once.

### Auth isolation
Each agent gets their own `auth/<agent>/` folder for Microsoft OAuth token caches. This prevents token collisions when multiple agents authenticate through the same machine.

### Smart reconnect with auth error detection
The reconnect system uses exponential backoff (5s → 10s → 20s → 40s → 60s) with a max retry limit. Critically, it detects auth-specific errors (invalid session, account suspended, duplicate login) and STOPS instead of retrying. This prevents the zombie reconnect loop that got Koda's account suspended.

### Reconnect counter reset delay
The reconnect attempt counter only resets after being connected for 30 seconds. This prevents a loop where the bot logs in successfully, gets immediately kicked, and resets its counter — leading to infinite retries.

### disableChatSigning
Minecraft 1.19.1+ introduced signed chat, which requires proper cryptographic signing of messages. Mineflayer's implementation can cause "broken chain" disconnects, especially when other players join. Setting `disableChatSigning: true` bypasses this entirely (requires `enforce-secure-profile=false` on the server).

### Modular features
Each feature area (survival, crafting, mining, farming, storage) is a separate module in `lib/`. Modules register their own chat command handlers and can be loaded/unloaded independently. They communicate through the bot object (e.g., `bot._craftItem` for cross-module access).

### Survival AI priority
1. Flee from creepers (explosion radius detection)
2. Flee when health < 6 HP
3. Fight hostile mobs within 8 blocks (equip best weapon)
4. Auto-eat when food < 15 (prioritized food list)
5. Auto-sleep when night falls (prevents phantom spawns)
6. Auto-respawn on death → pathfind home

## Server Requirements
- Java Edition (Bedrock not supported by Mineflayer)
- `enforce-secure-profile=false` in server.properties
- `online-mode=true` (Microsoft auth)
- Tailscale or accessible IP for bot connections
