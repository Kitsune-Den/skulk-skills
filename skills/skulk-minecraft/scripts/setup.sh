#!/bin/bash
# setup.sh — Set up skulk-minecraft bot for an agent
# Usage: bash setup.sh <agent-name> <microsoft-email> [server-host] [server-port]

set -e

AGENT_NAME="${1:?Usage: bash setup.sh <agent-name> <microsoft-email> [server-host] [server-port]}"
MS_EMAIL="${2:?Please provide Microsoft account email}"
SERVER_HOST="${3:-100.108.52.70}"
SERVER_PORT="${4:-25565}"
BOT_DIR="${HOME}/skulk-minecraft"
SOURCE_HOST="100.95.82.118"  # Sage's Bookstacks

echo "🦊 Setting up Minecraft bot for: ${AGENT_NAME}"
echo "   Microsoft account: ${MS_EMAIL}"
echo "   Server: ${SERVER_HOST}:${SERVER_PORT}"
echo ""

# Create directories
mkdir -p "${BOT_DIR}/config" "${BOT_DIR}/auth/${AGENT_NAME}" "${BOT_DIR}/lib"

# Try filedrop first, fall back to SCP
echo "📦 Downloading bot code..."
if curl -sf -o /tmp/skulk-minecraft.tar.gz "http://${SOURCE_HOST}:18556/uploads/skulk-minecraft.tar.gz" 2>/dev/null; then
    cd "${BOT_DIR}"
    tar xzf /tmp/skulk-minecraft.tar.gz
    rm /tmp/skulk-minecraft.tar.gz
    echo "   Downloaded from filedrop ✓"
elif scp -q "root@${SOURCE_HOST}:~/.openclaw/workspace/projects/skulk-minecraft/{skulk-bot.js,package.json}" "${BOT_DIR}/" 2>/dev/null && \
     scp -qr "root@${SOURCE_HOST}:~/.openclaw/workspace/projects/skulk-minecraft/lib" "${BOT_DIR}/" 2>/dev/null; then
    echo "   Copied via SCP ✓"
else
    echo "   ✗ Can't reach Bookstacks. Copy files manually."
    exit 1
fi

# Check for existing config
if [ -f "${BOT_DIR}/config/${AGENT_NAME}.json" ]; then
    echo "   Config already exists ✓"
else
    echo "📝 Creating config..."
    cat > "${BOT_DIR}/config/${AGENT_NAME}.json" << CONF
{
  "name": "${AGENT_NAME^}",
  "username": "${MS_EMAIL}",
  "profilesFolder": "./auth/${AGENT_NAME}",
  "homeBase": {"x": -273, "y": 58, "z": -254},
  "personality": {
    "joinMessage": "${AGENT_NAME^} has connected.",
    "deathMessage": "${AGENT_NAME^} will return.",
    "greetPlayer": "Hey {player}!",
    "followAck": "Following you, {player}.",
    "stopAck": "Stopping.",
    "emptyInventory": "Nothing in inventory.",
    "wave": "*waves*",
    "lowHealth": "Low health: {health} HP!",
    "digAck": "Digging..."
  }
}
CONF
    echo "   Config created at config/${AGENT_NAME}.json ✓"
    echo "   Edit it to customize personality!"
fi

# Check Node version
NODE_VERSION=$(node --version 2>/dev/null | grep -oP '\d+' | head -1)
if [ -z "${NODE_VERSION}" ]; then
    echo "✗ Node.js not found. Install Node >= 22."
    exit 1
elif [ "${NODE_VERSION}" -lt 22 ]; then
    echo "⚠ Node ${NODE_VERSION} detected. Mineflayer requires Node >= 22."
    echo "  Run: nvm install 22 && nvm use 22"
    exit 1
else
    echo "   Node v$(node --version) ✓"
fi

# Install dependencies
echo "📦 Installing dependencies..."
cd "${BOT_DIR}"
npm install --silent 2>/dev/null
echo "   Dependencies installed ✓"

echo ""
echo "═══════════════════════════════════════"
echo "  ✅ Setup complete!"
echo ""
echo "  To connect:"
echo "    cd ${BOT_DIR}"
echo "    node skulk-bot.js ${AGENT_NAME}"
echo ""
echo "  First run will prompt for Microsoft"
echo "  device code auth — a human needs to"
echo "  enter the code at microsoft.com/link"
echo "═══════════════════════════════════════"
