---
name: nano-banana-prompt-catalog
description: This skill should be used when the user asks about "Nano-Banana prompts", "image generation prompts", "image editing prompts", "Nano-Banana techniques", or needs inspiration for creative image tasks. Also activate when the user mentions "style transfer", "virtual try-on", "illustration to figure", "manga conversion", "product photography prompts", "social media image prompts", "character design prompts", "sticker generation", "isometric models", "colorization", or any other Nano-Banana image generation and editing use case.
version: 3.0.0
---

# Nano-Banana Prompt Catalog

A searchable catalog of 16,500+ prompts for Google's Nano-Banana image generation and editing model, combining 220 hand-picked curated prompts with 16,334 full-length prompts from the YouMind Pro reference library spanning 11 use-case categories.

## Search Workflow

Follow this two-tier search strategy. Start with the curated catalog for high-quality matches, then expand to the YouMind reference library for broader coverage.

### Tier 1: Search the Curated Catalog

Search `prompts-catalog.json` first. This file contains 220 concise, proven prompts with metadata.

Search by keyword:

```
Grep pattern="style transfer" path="prompts-catalog.json" output_mode="content" -C=3
```

Search by category:

```
Grep pattern="\"category\": \"Character Design\"" path="prompts-catalog.json" output_mode="content" -A=6
```

**Curated catalog fields:** `case` (ID), `title`, `author`, `category`, `input` (what images to upload), `prompt` (exact prompt text), `notes` (customization guidance, may be null).

### Tier 2: Search the YouMind Reference Library

When the curated catalog has insufficient matches or the user needs more variety, search YouMind reference files directly. Use the category-to-file mapping table below instead of reading `manifest.json` at runtime.

Search a specific category file:

```
Grep pattern="watercolor" path="youmind-references/profile-avatar.json" output_mode="content" -C=2
```

Search across all YouMind files:

```
Grep pattern="isometric" path="youmind-references/" output_mode="content" -C=2 glob="*.json"
```

Search titles only for quick scanning:

```
Grep pattern="\"title\":.*manga" path="youmind-references/comic-storyboard.json" output_mode="content" -i=true
```

**YouMind entry fields:** `id`, `title`, `description` (brief summary), `content` (full prompt text, often multi-paragraph), `needReferenceImages` (boolean).

**Important:** YouMind category files can be very large (social-media-post.json is 16 MB). Never read entire files. Always use Grep with targeted patterns.

## Category-to-File Quick Reference

### Curated Catalog (`prompts-catalog.json`) -- 220 prompts

| Category | Count | Typical Use Cases |
|---|---|---|
| Visual Transformation | 11 | Illustration to 3D figure, manga conversion, anime to cosplay |
| Character Design | 8 | Design sheets, pose control, expression sheets, line art coloring |
| Photo Editing | 8 | Auto enhancement, colorization, outpainting, restoration |
| Fashion & Beauty | 6 | Virtual try-on, hairstyle grids, makeup application |
| Spatial & Geographic | 7 | Map to street view, isometric models, floor plan to 3D |
| Creative Design | 19 | Product packaging, merchandise, jewelry, chess sets |
| Food & Cooking | 5 | Recipe from ingredients, food photography, calorie annotation |
| Entertainment | 16 | Comics, stickers, LEGO figures, action figures, game UI |
| Education & Science | 8 | Infographics, model annotations, math reasoning diagrams |
| AR & Annotation | 3 | Real-world AR overlays, red pen annotations, watermarks |
| YouMind Pro | 129 | Featured selections from all YouMind categories |

### YouMind Reference Library (`youmind-references/`) -- 16,334 prompts

| Category | File | Count |
|---|---|---|
| Profile / Avatar | `profile-avatar.json` | 1,200 |
| Social Media Post | `social-media-post.json` | 7,226 |
| Infographic / Edu Visual | `infographic-edu-visual.json` | 493 |
| YouTube Thumbnail | `youtube-thumbnail.json` | 189 |
| Comic / Storyboard | `comic-storyboard.json` | 327 |
| Product Marketing | `product-marketing.json` | 4,245 |
| E-commerce Main Image | `ecommerce-main-image.json` | 462 |
| Game Asset | `game-asset.json` | 458 |
| Poster / Flyer | `poster-flyer.json` | 556 |
| App / Web Design | `app-web-design.json` | 180 |
| Uncategorized | `others.json` | 998 |

### Category Selection Guide

Map user intent to the best file to search:

- **Avatars, profile pictures, character portraits** --> `profile-avatar.json`
- **Instagram, Twitter/X, quote cards, carousels** --> `social-media-post.json`
- **Diagrams, explainers, data viz, educational** --> `infographic-edu-visual.json`
- **YouTube thumbnails, video covers** --> `youtube-thumbnail.json`
- **Manga, webtoons, comic panels, storyboards** --> `comic-storyboard.json`
- **Product ads, brand visuals, campaign creatives** --> `product-marketing.json`
- **E-commerce listings, product shots, mockups** --> `ecommerce-main-image.json`
- **Game characters, items, UI elements, environments** --> `game-asset.json`
- **Event posters, movie posters, flyers** --> `poster-flyer.json`
- **UI mockups, landing pages, app screenshots** --> `app-web-design.json`
- **Anything else or uncertain** --> `others.json`, then broaden to curated catalog

## Output Format

Present each matching prompt using this structure.

**For curated catalog results:**

```
### [Title] (by [Author])
**Category:** [Category]
**Input required:** [Input field value]

**Prompt:**
> [Exact prompt text in blockquote]

**Notes:** [Notes if present, otherwise omit]
```

**For YouMind reference results:**

```
### [Title]
**Category:** [Category file name, human-readable]
**Reference images required:** [Yes/No based on needReferenceImages]

**Prompt:**
> [Content field in blockquote]

**Description:** [Description field]
```

**General rules:**
- Show 3-5 best matches unless the user asks for more
- Present the most relevant match first
- When multiple categories match, show one or two from each relevant category
- Always include the exact prompt text so the user can copy it directly
- For very long prompts (common in YouMind entries), show the first paragraph and note the full length

## Placeholder Customization

Many prompts contain placeholders that require customization before use. Identify and explain all placeholders when presenting a prompt.

### Square Bracket Placeholders `[text]`

Simple replacement markers. Replace the bracketed text with user-specific values.

Examples from the catalog:
- `[1970]` --> Replace with desired era
- `[Building Only]` --> Replace with target subject
- `[point of interest]` --> Replace with specific landmark or object to annotate
- `[long curly]` --> Replace with desired hairstyle description

When presenting prompts with `[brackets]`, list each placeholder with its purpose and suggest 2-3 concrete replacement values based on the user's stated goal.

### Argument Syntax Placeholders `{argument name="..." default="..."}`

Structured format with parameter name and default value, common in YouMind Pro prompts.

Examples:
- `{argument name="famous_quote" default="Stay Hungry, Stay Foolish"}`
- `{argument name="ethnicity" default="Japanese"}`
- `{argument name="modern scene" default="a busy Shibuya scramble crossing"}`

When presenting prompts with `{argument}` tags, extract each argument and present as a fill-in table:

| Parameter | Default Value | Replace With |
|---|---|---|
| `famous_quote` | "Stay Hungry, Stay Foolish" | _User's desired quote_ |
| `author` | "Steve Jobs" | _Name of the quoted person_ |

Instruct the user to replace the entire `{argument ...}` tag with their desired text.

### Input Requirements

The `input` field (curated catalog) and `needReferenceImages` field (YouMind) indicate whether images must be uploaded. Common patterns:

- **"No specific input required"** -- Pure generation; no image upload needed
- **"Need to upload a reference image"** -- Upload one source image for transformation
- **"Need to upload a character reference image"** -- Upload character art or photo
- **"Need to upload multiple reference images"** -- Upload several images; prompt describes ordering (e.g., "Figure 1", "Figure 2")

Always state image requirements clearly when presenting a prompt.

## Handling Ambiguous Requests

When the user's request is vague or matches multiple categories:

1. **Ask one clarifying question** to narrow intent (e.g., "Looking for social media post templates or product marketing visuals?")
2. **Show a sampler** -- present one prompt from each of the 2-3 most likely categories and ask which direction to explore
3. **Default to the curated catalog** for general "show me cool prompts" requests, since these are the most proven and concise
4. **For technique-oriented requests** (e.g., "style transfer"), search across all files since techniques span categories

Never return empty results without offering an alternative search path or related category.

## Best Practices

- Prefer curated catalog for beginners -- shorter, proven prompts with clear input requirements
- Use YouMind library for advanced users -- detailed multi-paragraph prompts with structured scene/subject/style breakdowns
- Suggest combining elements from multiple prompts when the user's goal spans techniques
- Note multi-image prompts that reference "Figure 1", "Figure 2", etc. -- the user must upload images in that specific order
- Preserve prompt structure -- YouMind prompts often use markdown headings (### Scene, ### Subject, ### Style); keep this formatting intact

## Additional Resources

### Data Files

- **`prompts-catalog.json`** -- 220 curated prompts with `case`, `title`, `author`, `category`, `input`, `prompt`, `notes`. Primary search target for all queries.
- **`youmind-references/manifest.json`** -- Category index with slug, title, file, and count. Not needed at runtime (use tables above), but available for validation.
- **`youmind-references/*.json`** -- 11 category files, 16,334 total prompts. Each entry: `id`, `title`, `description`, `content`, `needReferenceImages`. Search with Grep; never load entire files.

### Related Plugin Resources

- **`/nano-banana-prompts [query]`** -- Companion slash command for direct prompt browsing using the same data files and search strategy.
