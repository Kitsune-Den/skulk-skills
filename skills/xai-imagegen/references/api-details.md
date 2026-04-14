# xAI Image API Reference

## Endpoint

`POST https://api.x.ai/v1/images/generations`

## Authentication

`Authorization: Bearer <XAI_API_KEY>`

## Request Body

```json
{
  "model": "grok-imagine-image",
  "prompt": "description of image",
  "n": 1,
  "response_format": "url"
}
```

## Response

```json
{
  "data": [
    {
      "url": "https://imgen.x.ai/xai-imgen/xai-tmp-imgen-<uuid>.jpeg",
      "mime_type": "image/jpeg",
      "revised_prompt": ""
    }
  ],
  "usage": {
    "cost_in_usd_ticks": 200000000
  }
}
```

## Important Notes

- **URLs are temporary.** Download the image immediately after generation.
- **Cost:** ~200M ticks per image ≈ $0.02 USD
- **Format:** Returns JPEG by default
- **Base64:** Set `response_format: "b64_json"` to get base64-encoded image data instead of URL

## Image Editing

To edit an existing image, include the source image:

```json
{
  "model": "grok-imagine-image",
  "prompt": "edit description",
  "image": "https://example.com/source-image.jpg"
}
```

## Chat Completions (Alternative)

xAI also supports image generation through the chat completions endpoint with `grok-4-latest`. Same API key, endpoint: `https://api.x.ai/v1/chat/completions`.
