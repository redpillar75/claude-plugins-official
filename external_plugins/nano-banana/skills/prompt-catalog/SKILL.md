---
name: nano-banana-prompt-catalog
description: Use when the user asks about Nano-Banana prompts, Google image generation/editing prompts, or needs inspiration for creative image generation tasks using Nano-Banana. Also activate when users mention wanting to create figures, stickers, style transfers, virtual try-ons, or other image editing tasks that match Nano-Banana capabilities.
version: 2.0.0
---

You have access to a massive catalog of 16,000+ Nano-Banana (Google's image generation and editing model) prompts and use cases.

## When to Activate

- User asks about Nano-Banana prompts or techniques
- User wants to generate or edit images using Nano-Banana
- User needs prompt inspiration for creative image tasks
- User mentions specific techniques like: illustration to figure, style transfer, virtual try-on, colorization, isometric models, manga conversion, product marketing, social media posts, etc.

## Data Sources

1. **Curated catalog** (`prompts-catalog.json`) — 220 hand-picked viral prompts
2. **YouMind reference library** (`youmind-references/`) — 16,334 prompts by category:
   - Read `youmind-references/manifest.json` for the category index
   - Use Grep to search category files (they can be large)
   - Each prompt has: `id`, `title`, `description`, `content`, `needReferenceImages`

## How to Help

1. Start by searching `prompts-catalog.json` for curated matches
2. If more results needed, search the YouMind reference files using Grep
3. Suggest relevant prompts based on the user's creative goal
4. Explain input requirements (what images to upload)
5. Provide the exact prompt text, noting any `[bracketed]` or `{argument}` sections that need customization

## Key Capabilities Covered

- **Visual Transformation**: Convert between styles (illustration to 3D, manga, anime to real)
- **Character Work**: Design sheets, pose control, expression control, clothing changes
- **Photo Enhancement**: Auto editing, colorization, outpainting, restoration
- **Creative Generation**: Product packaging, merchandise, LEGO figures, chess sets
- **Spatial**: Map to street view, isometric models, floor plan to 3D
- **Fashion**: Virtual try-on, hairstyle changes, makeup application
- **Marketing**: Product photos, social media posts, YouTube thumbnails, e-commerce images
- **Entertainment**: Comics, game assets, stickers, posters, app designs
