---
name: xai-imagegen
description: "Generate images using xAI's Grok image generation API (model grok-imagine-image). Use when the user asks to create, generate, or make an image, picture, illustration, artwork, avatar, banner, cover art, or visual. Also use for editing images with text prompts. Requires an xAI API key from https://console.x.ai. NOT for image analysis/vision (use the image tool instead)."
---

# xAI Image Generation

Generate images from text prompts using xAI's Grok Aurora model.

## Setup

API key must be available via either:
- Env var: `XAI_API_KEY`
- Credentials file: `~/.config/xai/credentials.json` → `{"api_key": "xai-..."}`

Get a key at https://console.x.ai

## Quick Generate

Run the bundled script:

```bash
bash skills/xai-imagegen/scripts/generate.sh "a fox spirit in a neon-lit library" /tmp/fox.jpg
```

Returns the local file path on success.

## Direct API Usage

```bash
curl -s -X POST "https://api.x.ai/v1/images/generations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -d '{
    "model": "grok-imagine-image",
    "prompt": "your prompt here"
  }'
```

Response contains a temporary URL — download immediately:

```json
{"data": [{"url": "https://imgen.x.ai/...", "mime_type": "image/jpeg"}]}
```

## Parameters

| Param | Required | Notes |
|-------|----------|-------|
| `model` | Yes | Use `grok-imagine-image` |
| `prompt` | Yes | Text description of desired image |
| `n` | No | Number of images (default: 1) |
| `response_format` | No | `url` (default) or `b64_json` |

## Prompt Tips

- Be specific and descriptive — style, mood, composition, colors
- Reference art styles: "in the style of cyberpunk illustration", "watercolor", "pixel art"
- Specify format when relevant: "square album cover", "wide banner", "portrait avatar"
- Grok handles text-in-images reasonably well (titles, labels)

## Image Editing

Provide a source image URL alongside a prompt to edit existing images. See `references/api-details.md` for the full editing API.

## Cost

Each generation costs ~$0.02 (200M cost ticks). Budget accordingly for batch generation.
