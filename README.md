# Hooks

A platform-aware framework for choosing content hooks — the opening lines, visuals, and sounds that grab attention and stop the scroll.

## The Problem

A great hook on LinkedIn can flop on Instagram. A YouTube Shorts opener that kills it would bore a long-form audience. **Platform mechanics, content format, niche, and creator context all change what "good" looks like.** This repo gives you a system to navigate that.

## What's Inside

| File | What it does |
|------|-------------|
| `hook_selector.py` | Interactive CLI — answer 6 questions, get a tailored hook blueprint |
| `framework.md` | The full research: platform algorithms, format constraints, niche psychology, anti-patterns, and the complete hook mapping |
| `list.md` | Quick-reference hook templates (good vs bad) |

## Quick Start

```bash
# Interactive mode — walks you through all 6 decision variables
python3 hook_selector.py

# Quick mode — skip the detailed formulas and frameworks
python3 hook_selector.py --quick
```

The tool asks 6 questions:

1. **Platform** — LinkedIn, YouTube, or Instagram
2. **Format** — Text post, video, short/reel, or carousel
3. **Niche** — Education, personal brand, B2B, or entertainment
4. **Goal** — Engagement, conversion, shares, or saves
5. **Authority level** — Beginner or established
6. **Audience temperature** — Cold, warm, or hot

Then it outputs:
- A **recommended hook template** with psychological triggers
- **Platform constraints** (hook window, algo signals, key stats)
- **Format rules** (character limits, pacing, visual requirements)
- **Niche-specific styles** and dominant triggers
- **Anti-patterns** to avoid on that platform
- **Authority and audience adjustments**
- **Composable formulas** to generate variations
- **Structural patterns** and **creator frameworks** (Welsh, Blackman, Hormozi, PAS)

## The Framework in Brief

Every hook is built from composable parts:

```
TRIGGER  +  QUALIFIER  +  PAYOFF PROMISE
```

**11 psychological triggers**: curiosity gap, FOMO, social proof, specificity, contrarian, identity, pattern interrupt, emotional resonance, open loops, negativity bias, loss aversion

**5 structural patterns**: shocking statement + context, question + implied answer, story opener + stakes, data point + implication, contrarian claim + authority signal

The right combination depends on your platform's attention architecture, your format's physical constraints, your niche's conventions, and your specific context as a creator.

## Platform Cheat Sheet

| | LinkedIn | YouTube | YouTube Shorts | Instagram Reels | Carousel |
|---|---|---|---|---|---|
| **Hook window** | 2 lines / ~130 chars | 5-15 seconds | 2-3 seconds | 1.7-3 seconds | ~0.5 sec (first slide) |
| **Primary metric** | Dwell + comments | Watch time | Completion % | Watch time + sends | Swipe-through + saves |
| **Audience state** | Professional scanning | Intent-driven | Passive scroll | Passive scroll | Feed browsing |

## How to Use `list.md`

1. Browse [list.md](list.md) for hook templates
2. Replace the `[bracketed placeholders]` with your specifics
3. Use the bad hooks as a reference for what to avoid

## No Dependencies

The selector is pure Python 3 with no external packages. Just run it.

## Contributing

Have a hook template or platform insight that works? Open a PR. For hook templates, add both good and bad versions to `list.md`. For framework additions, update `framework.md` with sources.

## License

[MIT](LICENSE)
