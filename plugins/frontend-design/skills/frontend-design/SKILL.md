---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Step-by-Step Process

**1. Analyze the brief**
- Identify the interface type (component, page, full app), the user's audience, and any hard constraints (framework, accessibility, performance targets).
- Note what the user has NOT said — fill those gaps with creative decisions, don't default to generic choices.

**2. Commit to an aesthetic direction before writing any code**
- Pick a specific conceptual direction: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc.
- Name it explicitly at the top of your response. One sentence: "Design direction: [name] — [one-sentence rationale]."
- Identify the single most memorable element — the one thing a user will notice and remember.

**3. Select the implementation stack**
- Default to the framework or tech the user specified.
- If unspecified: use plain HTML/CSS/JS for components and static pages; use React for interactive applications.
- Use the Motion library for React animations when available.

**4. Implement with precision**
- Typography: pick fonts that are distinctive and characterful. Pair a display font with a refined body font.
- Color: pick a cohesive palette with a dominant color and a sharp accent. Use CSS variables for all colors.
- Motion: one well-orchestrated entrance animation is more powerful than scattered micro-interactions. Use `animation-delay` for stagger effects. Add scroll-triggered and hover states that surprise.
- Layout: use asymmetry, overlap, and negative space deliberately. Break the grid in at least one place.
- Backgrounds: never solid colors as a default. Use gradient meshes, noise textures, geometric patterns, layered transparencies, or dramatic shadows.

**5. Deliver complete, working code**
- The code must run without modification.
- No placeholder images that require external URLs. Use CSS-generated shapes or SVG inline if visuals are needed.
- All interactive states must be implemented (hover, focus, active, disabled).

## Output Format

Respond in this order:

1. **Design direction line** — one sentence naming the aesthetic and the memorable element.
2. **Complete code** — one code block. No partial snippets unless the user asked for just a specific piece.
3. **Design notes** — 3–5 bullet points explaining the key choices (font selection rationale, color logic, one non-obvious technique used). Keep it tight; this is for the user to understand what to tweak, not a design essay.

## Example of a Great Result

**User prompt:** "Build me a landing page for a CLI developer tool."

**Design direction:** Industrial terminal — the memorable element is a scanline-overlaid hero section with a blinking cursor prompt.

The response delivers: a dark background with a subtle green phosphor glow, a monospace display font (e.g., JetBrains Mono) paired with a clean sans-serif for body, a hero with an animated terminal prompt that types out the value proposition, and a sticky nav bar with a frosted glass effect. Design notes explain why JetBrains Mono was chosen over a generic monospace, how the scanline overlay was implemented with a CSS repeating linear gradient, and why the CTA button uses a sharp corner instead of rounded.

## Never Do

- **Never use Inter, Roboto, Arial, or system fonts** as your primary typeface. These are the default choices; make a deliberate one.
- **Never use purple gradients on white backgrounds.** It is the single most common AI-generated aesthetic and is immediately recognizable as generic.
- **Never repeat the same aesthetic across generations.** Vary between light and dark, different font pairings, different spatial approaches.
- **Never leave interactive states unimplemented.** Hover without active, focus without visible ring — these are incomplete.
- **Never add placeholder comments like `/* add your color here */`.** Make the choice and implement it. The user hired you for taste, not a template.
- **Never use the same design direction twice in the same session.** If you just built something minimalist, build something maximalist next.
- **Never explain what the code does line-by-line** in the design notes. The code is readable. Use notes only for WHY you made specific choices.

## Aesthetic Reference

**Typography**: Fraunces, Playfair Display, Clash Display, Cormorant Garamond, Unbounded, Cabinet Grotesk, Syne, DM Serif Display, Instrument Serif, Sentient — pick one for display. Pair with General Sans, Outfit, Plus Jakarta Sans, DM Sans, or a monospace like JetBrains Mono or Geist Mono for body.

**Color approaches**: Deep charcoal + acid yellow; cream + terracotta + forest green; near-black + electric blue; warm white + ink black + gold; dusty pink + burgundy + ivory; slate + coral.

**Motion patterns**: staggered reveal on load (`animation-delay: calc(var(--i) * 0.1s)`), magnetic hover on interactive elements, scroll-linked parallax, cursor-following highlights.

Remember: the goal is a design that feels authored, not generated. Commit fully to a direction. Restraint and maximalism both work — inconsistency does not.
