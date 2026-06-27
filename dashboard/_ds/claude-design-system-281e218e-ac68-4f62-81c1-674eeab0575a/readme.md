# Claude Design System

A warm-canvas, editorial design system for **Anthropic's Claude** product surface. The system anchors on a tinted-cream canvas, slab-serif display headlines, a signature warm coral, and dark-navy product surfaces (code editors, model cards). Brand voltage comes from the **cream + coral** pairing — deliberately humanist where most AI brands run cool blue + slate.

> **Sources.** This system was authored from a written brand/style specification for the Claude marketing surface (claude.com). No codebase or Figma file was provided. Visual decisions trace to that spec; component recreations are cosmetic, not derived from Anthropic's production source. If you have the real codebase, Figma, or licensed font binaries, re-attach them and this system can be tightened against ground truth.

---

## How it's organized

| Path | What |
|---|---|
| `styles.css` | Global entry point — `@import`s every token + font file. Consumers link this one file. |
| `tokens/` | `fonts.css`, `colors.css`, `typography.css`, `spacing.css` — CSS custom properties. |
| `assets/` | Brand spike-mark glyph in ink / cream / coral. |
| `guidelines/` | Foundation specimen cards (Colors, Type, Spacing, Brand) shown in the Design System tab. |
| `components/` | Reusable React primitives — `buttons/`, `feedback/`, `forms/`, `surfaces/`, `navigation/`. |
| `ui_kits/marketing/` | High-fidelity Claude.com homepage recreation composed from the primitives. |
| `SKILL.md` | Agent-Skill manifest so this system is portable into Claude Code. |

### Components
`Button` · `IconButton` (buttons/) · `Badge` (feedback/) · `Input` (forms/) · `Card` (surfaces/) · `CategoryTabs` (navigation/). Each has a `.jsx`, a `.d.ts` props contract, a `.prompt.md` usage note, and a `@dsCard` showcase. Mount them via `const { Button } = window.ClaudeDesignSystem_281e21` after loading `_ds_bundle.js`.

### UI kits
`ui_kits/marketing/` — interactive homepage (nav, hero with code mockup, feature grid, dark model-comparison band, coral CTA, footer, signup modal, cookie bar).

---

## Content fundamentals

**Voice: warm, literary, plainspoken — a thinking partner, not a hype machine.** Copy reads like a considered magazine, not a SaaS template.

- **Person.** Speaks to *you* ("your most important work", "AI that partners with your best thinking"). Refers to the product as *Claude*, the company as *Anthropic*. First-person plural ("we") only for company voice (footer, policies).
- **Casing.** Sentence case everywhere — headlines, buttons, nav. Never Title Case Marketing Headlines. The only uppercase is the `caption-uppercase` micro-label (e.g. "NEW", section eyebrows) with 1.5px tracking.
- **Tone.** Calm, declarative, concrete. Names real capabilities ("Extended thinking", "Long context", "Claude Code") over abstract benefit-speak. Avoids exclamation marks, hype adjectives ("revolutionary", "game-changing"), and fear-based urgency.
- **Headlines.** Short, human, often a full sentence. "AI that partners with your best thinking." "Which problem are you up against?" Set in the display serif — the serif *is* the literary signal.
- **Buttons.** Verb-first and short: "Try Claude", "Talk to sales", "Compare all models", "Get API key". No "Click here", no trailing punctuation.
- **Emoji.** None. The brand never uses emoji on marketing surfaces. Iconography is line-art, not emoji.
- **Numbers & claims.** Sparse. The system resists data-slop — show a real capability or model name before inventing a stat.

**Examples to emulate:** "Claude is a thinking partner for your most important work — research, writing, analysis, and code." · "Start free. No credit card required." · "Opus for depth, Sonnet for balance, Haiku for speed."

---

## Visual foundations

**Canvas.** Every page floats on tinted cream `--canvas` #faf9f5 — warm, deliberately *not* pure white or cool gray. This is the single most defining brand choice; pure white reads as "any other AI tool."

**Color.** Three-surface trinity: cream (`--canvas` / `--surface-card`), dark navy (`--surface-dark` #181715), and the signature warm coral `--coral` #cc785c. Coral is **scarce** on individual elements (primary CTAs only) and **generous** only on full-bleed coral callout cards. Companion accents (teal #5db8a6, amber #e8a55a) appear only on product chrome and eyebrows. No fourth surface tone — never purple, never green sections.

**Type.** Editorial split. Display = slab serif (`--font-display`, Newsreader ≈ Copernicus) at **weight 400** with negative tracking (−0.3 to −1.5px) — never bold. Body/UI = humanist sans (`--font-body`, Inter ≈ StyreneB) at 400 (text) / 500 (labels). Code = JetBrains Mono. The serif/sans split is unbreakable; a sans display headline would make Claude feel generic.

**Backgrounds.** Flat color blocks, no gradients, no photographic hero, no repeating texture. "Imagery" is the product itself — dark code-window mockups, terminal output, model-comparison cards. Occasional minimal line-art (coral + navy strokes on cream). Never photorealistic, never AI-gradient mush.

**Spacing & layout.** 4px base. Section rhythm a uniform **96px** between bands. Card padding generous (32px; coral callouts 48px). Content caps at 1200px centered. Hero is a 6/6 grid that stacks on mobile.

**Corners.** Hierarchical: 8px buttons/inputs/tabs, 12px content & product cards, 16px hero container, pill for badges. Consistent and calm.

**Borders & elevation.** Color-block first, shadow rare. Depth comes from cream-vs-dark surface contrast, not shadows. Hairlines are `--hairline` #e6dfd8 (one elevation step, not ink lines). Shadows exist (`--shadow-soft`, `--shadow-card`) but are used sparingly on hover-lift / floating modals only. Cards: rounded, no border on cream feature cards, hairline border on bordered/pricing cards, no shadow.

**Motion.** Restrained. `--ease-standard` cubic-bezier(0.32,0.08,0.24,1), `--duration-fast` 120ms / `--duration-base` 200ms. Fades and small color shifts — no bounces, no infinite decorative loops.

**Hover / press.** Primary button *darkens* on press (`--coral` → `--coral-active`); nothing else changes — no scale, no glow. Nav links shift from `--body` to `--ink`. The system deliberately under-specifies hover; restraint is the rule.

**Transparency & blur.** Rare. Modal scrim is `rgba(20,20,19,0.45)`. Selection highlight is coral at ~22% alpha. No glassmorphism, no backdrop blur on marketing surfaces.

**Imagery vibe.** Warm-neutral. When photography appears (testimonials, rare), avatars crop to 40px circles. The dominant "imagery" is dark product chrome with syntax highlighting in muted coral/amber/teal/sage on navy.

---

## Iconography

- **Style.** Thin line-art, ~1.6px stroke, rounded caps and joins, 24px grid — a calm, humanist outline set (the kit uses Lucide-style geometry). Icons are monochrome, tinted `--coral` for feature accents or `--ink`/`--on-dark` inline. No filled/duotone icons, no emoji, no Unicode dingbats as icons.
- **In this system.** Feature-card icons are inline SVGs in `ui_kits/marketing/Features.jsx` (brain, code, doc, search, shield, zap). For new work, link **[Lucide](https://lucide.dev)** from CDN (`https://unpkg.com/lucide@latest`) — it matches the stroke weight and rounded-cap style. *(Substitution flagged: Anthropic's production icon set is not public; Lucide is the closest open match.)*
- **Brand mark.** The Anthropic spike-mark (a 6-spoke radial "burst" / asterisk) lives in `assets/anthropic-mark.svg` (ink), `-cream.svg` (on dark), `-coral.svg`. Used as the wordmark prefix and as an occasional content marker. Never invert the mark within the wordmark lockup itself. *(Reconstructed from the brand spec — replace with the official glyph if available.)*

---

## Do & don't (essentials)

**Do** — anchor on cream; use serif 400 for all display; keep coral scarce on elements / generous on callout cards; alternate cream ↔ dark bands; 96px section rhythm; sentence case copy.

**Don't** — no pure white/cool gray canvas; no bold serif display; no cool blue/cyan accent; no coral everywhere; no Inter for headlines; no two consecutive same-surface bands; no emoji; no invented stats.

---

## Known gaps & substitutions (please help)

- **Fonts.** Copernicus and StyreneB are licensed Anthropic faces, not public. Substituted **Newsreader** (serif) + **Inter** (sans) via Google Fonts. Swap in the real binaries (`@font-face` in `tokens/fonts.css`) when available.
- **Icons.** Production icon set not public — Lucide substituted and flagged.
- **Spike mark.** Reconstructed from description, not the official SVG.
- **Product surface.** This documents the marketing surface only; the claude.ai chat product (message bubbles, tools, sidebar) is out of scope.
