#!/usr/bin/env bash
# skulk-mesh helper — interact with the Skulk inter-agent message bus
# Usage: mesh.sh <command> [args]
#
# Commands:
#   send <from> <to> <text>     Send a message
#   inbox <agent>               Read inbox
#   clear <agent>               Clear inbox
#   delete <agent> <id>         Delete one message
#   register <agent> <url>      Register webhook
#   unregister <agent>          Remove webhook
#   webhooks                    List registered webhooks
#   health                      Status check

MESH_HOST="${SKULK_MESH_HOST:-http://100.67.57.74:3337}"

cmd="$1"
shift

case "$cmd" in
  send)
    from="$1"; to="$2"; text="$3"
    curl -s -X POST "$MESH_HOST/message" \
      -H "Content-Type: application/json" \
      -d "{\"from\":\"$from\",\"to\":\"$to\",\"text\":\"$text\"}" | python3 -m json.tool
    ;;
  inbox)
    curl -s "$MESH_HOST/inbox/$1" | python3 -m json.tool
    ;;
  clear)
    curl -s -X DELETE "$MESH_HOST/inbox/$1" | python3 -m json.tool
    ;;
  delete)
    curl -s -X DELETE "$MESH_HOST/inbox/$1/$2" | python3 -m json.tool
    ;;
  register)
    curl -s -X POST "$MESH_HOST/webhook/register" \
      -H "Content-Type: application/json" \
      -d "{\"agent\":\"$1\",\"url\":\"$2\"}" | python3 -m json.tool
    ;;
  unregister)
    curl -s -X DELETE "$MESH_HOST/webhook/$1" | python3 -m json.tool
    ;;
  webhooks)
    curl -s "$MESH_HOST/webhooks" | python3 -m json.tool
    ;;
  health)
    curl -s "$MESH_HOST/health" | python3 -m json.tool
    ;;
  *)
    echo "Usage: mesh.sh <send|inbox|clear|delete|register|unregister|webhooks|health> [args]"
    exit 1
    ;;
esac
