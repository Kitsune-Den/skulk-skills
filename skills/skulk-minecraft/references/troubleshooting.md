# Troubleshooting

## "Failed to verify username" / "invalid session"

**Cause:** Microsoft OAuth token expired.
**Fix:** Delete the agent's auth folder and restart:
```bash
rm -rf auth/<agent>/*
node skulk-bot.js <agent>
# Will prompt for fresh device code login
```

## ACCOUNT_SUSPENDED

**Cause:** Mojang suspended the account, usually from rapid reconnect spam (old bot code without backoff).
**Fix:** Submit a support ticket at https://help.minecraft.net explaining the bot reconnect bug. These are usually temporary.
**Prevention:** The new skulk-bot.js detects auth errors and stops instead of looping.

## "Chat disabled due to broken chain"

**Cause:** Minecraft 1.19.1+ secure chat signing. Mineflayer can't properly sign chat messages.
**Fix (server-side):** Set `enforce-secure-profile=false` in `server.properties` and restart server.
**Fix (bot-side):** Ensure `disableChatSigning: true` is in the bot's createBot options (already set in skulk-bot.js).

## Duplicate login kicks

**Cause:** Two bot instances trying to connect with the same account simultaneously. Often happens when killing and restarting without waiting.
**Fix:**
1. Kill ALL bot processes: `pkill -f 'skulk-bot.js'`
2. Wait 10-15 seconds for server to clear the old session
3. Start fresh: `node skulk-bot.js <agent>`

**Prevention:** The bot now treats `duplicate_login` as an auth error and stops instead of reconnecting into a loop.

## Node version errors

**Cause:** Mineflayer 4.35.0 requires Node >= 22. Older versions cause crypto/chat signing errors.
**Fix:**
```bash
nvm install 22
nvm use 22
npm install  # rebuild native modules
```

## Bot connects but gets kicked immediately

**Possible causes:**
- Server whitelist — add the bot's MC username
- Server full — check max-players in server.properties
- Version mismatch — ensure `--version` matches server version
- IP ban — check server's banned-ips.json

## Bot can't pathfind / gets stuck

**Cause:** Mineflayer-pathfinder can struggle with complex terrain, water, or nether.
**Fix:** Use `goto x y z` for direct navigation, or `stop` then manually reposition.

## "Does the account own Minecraft?"

**Cause:** The Microsoft account doesn't have a Minecraft Java Edition license, or the Mojang profile lookup failed.
**Fix:** Verify the game is purchased on that specific Microsoft account at minecraft.net. Sometimes this is a transient API error — retry after a few minutes.
