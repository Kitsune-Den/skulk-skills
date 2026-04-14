/**
 * skulk-mesh — inter-agent message bus for The Skulk
 * Listens on port 3337 (Tailscale-internal only)
 *
 * POST   /message               { from, to, text }         → send a message
 * GET    /inbox/:agent          → read all messages for an agent
 * DELETE /inbox/:agent/:id      → delete a specific message
 * DELETE /inbox/:agent          → clear entire inbox
 * POST   /webhook/register      { agent, url }             → register webhook
 * DELETE /webhook/:agent        → unregister webhook
 * GET    /webhooks              → list registered webhooks
 * GET    /agents                → list known agents
 * GET    /health                → status check
 */

const express = require("express");
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const http = require("http");
const https = require("https");

const app = express();
app.use(express.json());

const DATA_FILE     = path.join(__dirname, "messages.json");
const WEBHOOK_FILE  = path.join(__dirname, "webhooks.json");

const KNOWN_AGENTS = ["koda", "luna", "sage", "vesper", "miso", "ada"];

// ── Helpers ────────────────────────────────────────────────────────────────

function load() {
  try { return JSON.parse(fs.readFileSync(DATA_FILE, "utf8")); }
  catch { return []; }
}

function save(messages) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(messages, null, 2));
}

function loadWebhooks() {
  try { return JSON.parse(fs.readFileSync(WEBHOOK_FILE, "utf8")); }
  catch { return {}; }
}

function saveWebhooks(hooks) {
  fs.writeFileSync(WEBHOOK_FILE, JSON.stringify(hooks, null, 2));
}

function ts() {
  return new Date().toISOString();
}

// Fire-and-forget webhook delivery
function deliverWebhook(url, payload) {
  try {
    const body = JSON.stringify(payload);
    const parsed = new URL(url);
    const lib = parsed.protocol === "https:" ? https : http;
    const req = lib.request({
      hostname: parsed.hostname,
      port: parsed.port || (parsed.protocol === "https:" ? 443 : 80),
      path: parsed.pathname + parsed.search,
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Content-Length": Buffer.byteLength(body),
        "X-Skulk-Mesh": "1",
      },
    }, (res) => {
      console.log(`[${ts()}] 🔔 webhook → ${url} (${res.statusCode})`);
    });
    req.on("error", (e) => {
      console.error(`[${ts()}] ❌ webhook failed → ${url}: ${e.message}`);
    });
    req.write(body);
    req.end();
  } catch (e) {
    console.error(`[${ts()}] ❌ webhook error → ${url}: ${e.message}`);
  }
}

// Notify an agent (and "all" broadcast) if they have a webhook
function notifyAgent(toAgent, message) {
  const hooks = loadWebhooks();
  const targets = new Set([toAgent]);
  if (toAgent === "all") KNOWN_AGENTS.forEach((a) => targets.add(a));

  for (const agent of targets) {
    if (hooks[agent]) {
      deliverWebhook(hooks[agent], { event: "new_message", message });
    }
  }
}

// ── Routes ─────────────────────────────────────────────────────────────────

app.get("/health", (req, res) => {
  const hooks = loadWebhooks();
  res.json({
    status: "warm",
    agents: KNOWN_AGENTS,
    totalMessages: load().length,
    registeredWebhooks: Object.keys(hooks),
    time: ts(),
  });
});

app.get("/agents", (req, res) => {
  res.json({ agents: KNOWN_AGENTS });
});

// Send a message
app.post("/message", (req, res) => {
  const { from, to, text } = req.body;
  if (!from || !to || !text)
    return res.status(400).json({ error: "from, to, and text are required" });

  const message = {
    id: crypto.randomUUID(),
    from: from.toLowerCase(),
    to: to.toLowerCase(),
    text,
    sentAt: ts(),
    read: false,
  };

  const messages = load();
  messages.push(message);
  save(messages);

  console.log(`[${ts()}] 📨 ${message.from} → ${message.to}: ${text.slice(0, 60)}`);

  // Push webhook if registered
  notifyAgent(message.to, message);

  res.json({ ok: true, id: message.id, message });
});

// Read inbox
app.get("/inbox/:agent", (req, res) => {
  const agent = req.params.agent.toLowerCase();
  const messages = load();
  const inbox = messages.filter((m) => m.to === agent || m.to === "all");
  res.json({ agent, count: inbox.length, messages: inbox });
});

// All messages
app.get("/messages", (req, res) => {
  res.json({ messages: load() });
});

// Delete one message
app.delete("/inbox/:agent/:id", (req, res) => {
  const { agent, id } = req.params;
  const messages = load();
  const filtered = messages.filter((m) => !(m.id === id && m.to === agent.toLowerCase()));
  if (filtered.length === messages.length)
    return res.status(404).json({ error: "Message not found" });
  save(filtered);
  res.json({ ok: true, deleted: id });
});

// Clear inbox
app.delete("/inbox/:agent", (req, res) => {
  const agent = req.params.agent.toLowerCase();
  const messages = load();
  const filtered = messages.filter((m) => m.to !== agent);
  save(filtered);
  res.json({ ok: true, cleared: agent, removed: messages.length - filtered.length });
});

// Register webhook
app.post("/webhook/register", (req, res) => {
  const { agent, url } = req.body;
  if (!agent || !url)
    return res.status(400).json({ error: "agent and url are required" });

  try { new URL(url); } catch {
    return res.status(400).json({ error: "invalid url" });
  }

  const hooks = loadWebhooks();
  hooks[agent.toLowerCase()] = url;
  saveWebhooks(hooks);

  console.log(`[${ts()}] 🔗 webhook registered: ${agent} → ${url}`);
  res.json({ ok: true, agent, url });
});

// Unregister webhook
app.delete("/webhook/:agent", (req, res) => {
  const agent = req.params.agent.toLowerCase();
  const hooks = loadWebhooks();
  if (!hooks[agent])
    return res.status(404).json({ error: "No webhook registered for this agent" });
  delete hooks[agent];
  saveWebhooks(hooks);
  res.json({ ok: true, unregistered: agent });
});

// List webhooks
app.get("/webhooks", (req, res) => {
  res.json({ webhooks: loadWebhooks() });
});

// ── Start ──────────────────────────────────────────────────────────────────

const PORT = 3337;
app.listen(PORT, "0.0.0.0", () => {
  console.log(`🔥 skulk-mesh running on :${PORT}`);
  console.log(`   Agents: ${KNOWN_AGENTS.join(", ")}`);
  console.log(`   Data: ${DATA_FILE}`);
  console.log(`   Webhooks: ${WEBHOOK_FILE}`);
});
