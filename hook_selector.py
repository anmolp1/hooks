#!/usr/bin/env python3
"""
Hook Selector — An interactive framework for choosing content hooks.

Takes your niche, platform, format, goal, authority level, and audience
temperature, then recommends the best hook style with templates,
psychological triggers, and anti-patterns to avoid.

Usage:
    python3 hook_selector.py              # Interactive mode
    python3 hook_selector.py --quick      # Skip detailed explanations
"""

import sys
import textwrap

# ---------------------------------------------------------------------------
# Data: Platform Constraints
# ---------------------------------------------------------------------------

PLATFORMS = {
    "linkedin": {
        "name": "LinkedIn",
        "formats": ["text", "carousel", "video"],
        "hook_window": "2 lines / ~130 chars (mobile), ~210 chars (desktop)",
        "primary_metric": "Dwell time + comments",
        "audience_state": "Professional scanning",
        "sound_dependency": "N/A (text-first platform)",
        "algo_signal": "Comment velocity in the 60-90 min golden hour",
        "key_stats": [
            "Comments weighted 8x more than likes",
            "Two-sentence hooks outperform single-line by 20%",
            "Sentences under 12 words perform 20% better",
            'Posts starting with "You" get 20% more engagement than "I"',
            "Carousels (PDF) generate 5x more clicks than other formats",
        ],
    },
    "youtube": {
        "name": "YouTube",
        "formats": ["long_form", "shorts"],
        "hook_window": "5-15 seconds (long-form), 2-3 seconds (Shorts)",
        "primary_metric": "Watch time x retention (long-form), Completion % + replays (Shorts)",
        "audience_state": "Intent-driven (long-form), Passive scrolling (Shorts)",
        "sound_dependency": "Critical",
        "algo_signal": "CTR x retention curve shape",
        "key_stats": [
            "55% of viewers lost within first 60 seconds",
            "Healthy retention = lose no more than 40% in first 30s",
            "10 percentage-point retention improvement = 25%+ more impressions",
            "50-60% of Shorts viewers leave within first 3 seconds",
            "Shorts: completion rate matters more than CTR",
        ],
    },
    "instagram": {
        "name": "Instagram",
        "formats": ["reels", "carousel", "text"],
        "hook_window": "1.7-3 seconds (Reels), ~0.5 seconds (carousel first slide)",
        "primary_metric": "Watch time + DM sends (Reels), Swipe-through + saves (Carousel)",
        "audience_state": "Passive scroll mode (3-4 posts/second)",
        "sound_dependency": "~50% watch muted — text overlays essential",
        "algo_signal": "3-second hold rate + shareability (sends per reach)",
        "key_stats": [
            "Reels with >60% 3-sec hold rate get 5-10x more reach",
            "First carousel slide carries 80% of the weight",
            "IG sometimes shows your 2nd slide first as a test",
            "15-second Reels: ~72% completion vs ~46% for longer ones",
            "694,000 Reels are sent via DM every minute",
        ],
    },
}

# ---------------------------------------------------------------------------
# Data: Format Constraints
# ---------------------------------------------------------------------------

FORMAT_INFO = {
    "text": {
        "name": "Text Post",
        "rules": [
            "Hook must land within ~130 chars (LinkedIn mobile) or ~125 chars (Instagram)",
            "Single sentence per line — dense paragraphs are scroll-killers",
            "White space is your most powerful formatting tool",
            "Emojis sparingly (1-2 max) as visual anchors",
            'Power words: "secret", "mistake", "actually", "exactly", "never", specific numbers',
        ],
    },
    "video": {
        "name": "Video (Long-form)",
        "rules": [
            "Cold open — start mid-action, no preamble, no greetings",
            "Deliver core hook in 1-2 seconds, value proposition by second 3-5",
            "Pattern interrupt in first 5 seconds = 23% higher retention",
            "Close framing + high energy for talking-head hooks",
            "Monotonous delivery causes 35% higher drop-off in first 45s",
        ],
    },
    "long_form": {
        "name": "YouTube Long-form Video",
        "rules": [
            "Cold open — no 'Hey guys, welcome back to my channel'",
            "Address the title/thumbnail promise within first 30 seconds",
            "Pattern interrupt in first 5 seconds = 23% higher retention",
            "Close framing + high energy for talking-head delivery",
            "No sponsor reads or long intros before delivering on the promise",
        ],
    },
    "shorts": {
        "name": "YouTube Shorts",
        "rules": [
            "First word = the hook — zero preamble",
            "Bold text overlay by second 1",
            "Optimize for completion rate, not just retention",
            "Looping content (seamless end-to-beginning) earns replay credit",
            "30-second Shorts at 85% retention >> 60-second at 50%",
        ],
    },
    "reels": {
        "name": "Instagram Reels",
        "rules": [
            "Bold, high-contrast text overlay by second 1",
            "Position text in center safe zone (avoid IG UI overlap)",
            "Burned-in captions essential for the 40-50% watching muted",
            "Trending audio gives algorithmic boost",
            "Use vertical 9:16 — horizontal format signals 'I don't belong here'",
        ],
    },
    "carousel": {
        "name": "Carousel / Slides",
        "rules": [
            "First slide is a billboard — stop the scroll in milliseconds",
            "Cover slide: under 8-10 words, one bold headline",
            "Design at 1080x1350 (4:5 portrait) for max screen real estate",
            "25-50 words per slide, one idea per slide",
            "Visual overlap onto next slide (arrows, partial text) signals 'swipe'",
            "Optimal length: 5-15 slides (LinkedIn), up to 10-20 (Instagram)",
        ],
    },
}

# ---------------------------------------------------------------------------
# Data: Niches
# ---------------------------------------------------------------------------

NICHES = {
    "education": {
        "name": "Education / How-to",
        "dominant_triggers": ["Curiosity gap", "Specificity", "Negativity bias"],
        "hook_styles": [
            'The mistake hook: "Stop doing [common practice]. Do this instead."',
            'The compression hook: "Learn in 10 min what took me 10 years"',
            'The specificity hook: "I tested [number] techniques — this 1 is the best"',
            'The insider hook: "Nobody is talking about [specific technique]"',
        ],
        "structure": "Hook + Proof of authority + Promise of specific value",
    },
    "personal_brand": {
        "name": "Personal Brand / Storytelling",
        "dominant_triggers": ["Emotional resonance", "Identity", "Vulnerability"],
        "hook_styles": [
            "Vulnerability hook: Lead with failure, then share the win",
            'Transformation arc: "How I went from [bad state] to [good state]"',
            'Identity hook: "This one is for all the [specific group]"',
            "Storytelling trust stack: Failure first → credibility follows",
        ],
        "structure": "Status Quo → Inciting Incident → Struggle → Epiphany → Transformation",
    },
    "business": {
        "name": "Business / B2B",
        "dominant_triggers": ["Contrarian/Controversy", "Specificity", "Social proof"],
        "hook_styles": [
            'Data drop: "Only 5% of cold emails use a P.S. — 35% more replies"',
            'Authority hook: "I spent $5K on courses so you don\'t have to"',
            'Contrarian take: "Most B2B marketers are measuring the wrong thing"',
            'Case study hook: "[Company] went from [A] to [B]. Here\'s the strategy."',
        ],
        "structure": "Credibility signal + Surprising insight + Value promise",
    },
    "entertainment": {
        "name": "Entertainment / Lifestyle",
        "dominant_triggers": ["Pattern interrupt", "Identity", "Emotional resonance"],
        "hook_styles": [
            "Sensory triggers: Swift movement, loud sounds, unexpected visuals",
            'POV / relatability: "Tell me you X without telling me"',
            "Trend-jacking: Trending audio with original twist (40% uplift)",
            "Niche humor and hyper-specific memes",
        ],
        "structure": "Instant visual/emotional punch → Context follows",
    },
}

# ---------------------------------------------------------------------------
# Data: Psychological Triggers
# ---------------------------------------------------------------------------

TRIGGERS = {
    "curiosity_gap": {
        "name": "Curiosity Gap",
        "description": "Incomplete information creates tension the brain must resolve",
        "boost": "Up to 30% engagement boost",
        "best_for": ["Cold audiences", "Education", "YouTube"],
    },
    "fomo": {
        "name": "FOMO / Loss Aversion",
        "description": "Missing out feels worse than gaining — urgency drives action",
        "boost": "60% of consumers act on FOMO within 24 hours",
        "best_for": ["Conversion goals", "Hot audiences", "Time-sensitive content"],
    },
    "social_proof": {
        "name": "Social Proof",
        "description": 'Specific numbers signal crowd validation ("Join 47,000+ students")',
        "boost": "Strongest for warm/hot audiences",
        "best_for": ["Established creators", "B2B", "Conversion"],
    },
    "specificity": {
        "name": "Specificity",
        "description": "$157K beats $150K — precise numbers signal data-backed credibility",
        "boost": "Odd/specific numbers consistently outperform round ones",
        "best_for": ["All platforms", "Education", "B2B"],
    },
    "contrarian": {
        "name": "Controversy / Contrarian",
        "description": "Challenging sacred cows creates cognitive dissonance requiring resolution",
        "boost": "49% reach lift on LinkedIn (CXL analysis of 100K+ posts)",
        "best_for": ["LinkedIn", "B2B", "Engagement goals"],
    },
    "identity": {
        "name": "Identity",
        "description": "Speaking to who the audience IS or wants to become taps belonging needs",
        "boost": "Creates instant tribal connection",
        "best_for": ["Personal brand", "Instagram", "Community building"],
    },
    "pattern_interrupt": {
        "name": "Pattern Interrupt",
        "description": "Breaking expected visual/auditory flow forces attention reallocation",
        "boost": "23% higher retention in first 5 seconds",
        "best_for": ["Video/Reels/Shorts", "Entertainment", "Cold audiences"],
    },
    "emotional_resonance": {
        "name": "Emotional Resonance",
        "description": "Content triggering emotions generates higher engagement",
        "boost": "31% higher success rates",
        "best_for": ["Personal brand", "Storytelling", "Shares goal"],
    },
    "negativity_bias": {
        "name": "Negativity Bias",
        "description": 'Brain prioritizes threats — "mistakes to avoid" outperforms positive framing',
        "boost": "Consistently outperforms positive-framed equivalents",
        "best_for": ["Education", "All platforms", "Engagement goals"],
    },
}

# ---------------------------------------------------------------------------
# Data: Structural Patterns
# ---------------------------------------------------------------------------

PATTERNS = [
    {
        "name": "Shocking Statement + Context",
        "template": "[Bold claim]. [Context or surprising reason].",
        "example": '"I escaped the rat race at 36. My secret sauce? Not playing status games."',
    },
    {
        "name": "Question + Implied Answer",
        "template": "[Intriguing question]? (Hint: [unexpected angle].)",
        "example": '"Why do 87% of LinkedIn outreach messages fail? (Hint: it\'s not your copy.)"',
    },
    {
        "name": "Story Opener + Stakes",
        "template": "[Relatable bad situation]. Then [unexpected turning point].",
        "example": '"I was $40,000 in debt. Then I found a spreadsheet that changed everything."',
    },
    {
        "name": "Data Point + Surprising Implication",
        "template": "[Specific stat]% of [group] [surprising behavior].",
        "example": '"41.29% of millennials spend more on coffee than retirement."',
    },
    {
        "name": "Contrarian Claim + Authority Signal",
        "template": "After [credential], I can tell you: [contrarian claim].",
        "example": '"After 15 years at NYC\'s highest-rated pizzeria: everything you\'ve been taught about dough is wrong."',
    },
]

# ---------------------------------------------------------------------------
# Data: Anti-patterns
# ---------------------------------------------------------------------------

ANTI_PATTERNS = {
    "linkedin": [
        '"I\'m humbled to announce..." — humble-brags disguised as lessons',
        "Performative vulnerability (crying selfies, hospital-bed hustle posts)",
        "Fabricated inspirational anecdotes (coffee shop leadership parables)",
        "Broetry: single-word lines stacked for false drama",
        '"I was fired. Best thing that ever happened." (overused formula)',
        'Explicit engagement bait ("Comment YES if you agree")',
        "External links in post body (kills organic reach)",
    ],
    "youtube": [
        '"Hey guys, welcome back to my channel" — the deadliest intro',
        "Long branded intro animations before value",
        "Sponsor reads before delivering on the title promise",
        "Extended self-introductions",
        "Thumbnail/title mismatch — not addressing the promise within 30 seconds",
    ],
    "instagram": [
        "Static wide-angle opening shots on Reels",
        "Slow-motion intros without context",
        "Starting with a sales pitch",
        "TikTok watermarks (algorithmically penalized)",
        "Horizontal 16:9 format in vertical feed (black bars)",
        "Audio-only hooks with no text overlays (50% watch muted)",
        "Generic first-slide titles on carousels without specific value promise",
    ],
}

# ---------------------------------------------------------------------------
# Data: The Complete Hook Mapping (niche x platform x format x goal)
# ---------------------------------------------------------------------------

HOOK_MAP = {
    ("education", "linkedin", "text"): {
        "engagement": {
            "template": '"Most [niche] advice is wrong. Here\'s what actually works."',
            "triggers": "Contrarian + Curiosity",
        },
        "conversion": {
            "template": '"[Specific result] in [timeframe]. Here\'s the exact process:"',
            "triggers": "Result + Specificity",
        },
        "shares": {
            "template": '"The #1 mistake [audience] makes with [topic]:"',
            "triggers": "Negativity + Identity",
        },
        "saves": {
            "template": '"[Number] frameworks that changed how I [outcome]:"',
            "triggers": "Specificity + Value",
        },
    },
    ("education", "linkedin", "carousel"): {
        "engagement": {
            "template": 'Slide 1: "Why [common practice] doesn\'t work"',
            "triggers": "Contrarian + Curiosity",
        },
        "conversion": {
            "template": 'Slide 1: "[Number] steps to [specific outcome]"',
            "triggers": "Specificity + Promise",
        },
        "shares": {
            "template": 'Slide 1: "[Shocking stat about topic]"',
            "triggers": "Data + Surprise",
        },
        "saves": {
            "template": 'Slide 1: "Save this [topic] cheat sheet"',
            "triggers": "Command + Value",
        },
    },
    ("education", "youtube", "long_form"): {
        "engagement": {
            "template": '"Is [common belief] actually true? I tested it."',
            "triggers": "Curiosity + Experiment",
        },
        "conversion": {
            "template": '"After [credential], here\'s the [number]-step system:"',
            "triggers": "Authority + Structure",
        },
        "shares": {
            "template": '"[Shocking stat]. Here\'s what nobody tells you."',
            "triggers": "Data + Curiosity gap",
        },
        "saves": {
            "template": '"Master [skill] — the complete guide"',
            "triggers": "Comprehensiveness",
        },
    },
    ("education", "youtube", "shorts"): {
        "engagement": {
            "template": '"Stop doing [mistake]. Try this instead."',
            "triggers": "Negativity + Pattern interrupt",
        },
        "conversion": {
            "template": '"[Specific result] in [time]. Step 1:"',
            "triggers": "Specificity + Urgency",
        },
        "shares": {
            "template": '"The [topic] trick [authority figures] hide"',
            "triggers": "Curiosity + Conspiracy",
        },
        "saves": {
            "template": '"Save this [number]-second tip:"',
            "triggers": "Command + Specificity",
        },
    },
    ("education", "instagram", "reels"): {
        "engagement": {
            "template": 'Bold text: "This is the #1 mistake with [topic]" + face close-up',
            "triggers": "Negativity + Visual",
        },
        "conversion": {
            "template": 'Before/after: Show result → "Here\'s how:"',
            "triggers": "Transformation + Open loop",
        },
        "shares": {
            "template": '"I wish someone told me this about [topic]"',
            "triggers": "Regret + Curiosity",
        },
        "saves": {
            "template": '"[Number] things I\'d do differently starting [skill] today"',
            "triggers": "Regret + List",
        },
    },
    ("education", "instagram", "carousel"): {
        "engagement": {
            "template": 'Slide 1: "Why [common practice] doesn\'t work"',
            "triggers": "Contrarian + Curiosity",
        },
        "conversion": {
            "template": 'Slide 1: "[Number] steps to [specific outcome]"',
            "triggers": "Specificity + Promise",
        },
        "shares": {
            "template": 'Slide 1: "[Shocking stat about topic]"',
            "triggers": "Data + Surprise",
        },
        "saves": {
            "template": 'Slide 1: "Save this [topic] cheat sheet"',
            "triggers": "Command + Value",
        },
    },
    ("personal_brand", "linkedin", "text"): {
        "engagement": {
            "template": '"I was terrified to [action]. Here\'s what happened:"',
            "triggers": "Vulnerability + Open loop",
        },
        "conversion": {
            "template": '"I went from [bad state] to [good state]. The turning point:"',
            "triggers": "Transformation + Curiosity",
        },
        "shares": {
            "template": '"[Relatable struggle] — and what I wish someone told me"',
            "triggers": "Emotion + Regret",
        },
        "saves": {
            "template": '"The [number] lessons from [specific failure]:"',
            "triggers": "Loss + Framework",
        },
    },
    ("personal_brand", "linkedin", "carousel"): {
        "engagement": {
            "template": 'Slide 1: "What [failure/setback] taught me about [topic]"',
            "triggers": "Vulnerability + Curiosity",
        },
        "conversion": {
            "template": 'Slide 1: "My [timeframe] journey from [start] to [result]"',
            "triggers": "Transformation + Specificity",
        },
        "shares": {
            "template": 'Slide 1: "[Number] truths nobody tells you about [aspiration]"',
            "triggers": "Negativity + Identity",
        },
        "saves": {
            "template": 'Slide 1: "The [number]-step process that changed my [outcome]"',
            "triggers": "Structure + Transformation",
        },
    },
    ("personal_brand", "youtube", "long_form"): {
        "engagement": {
            "template": '"Have you ever thought about [relatable aspiration]?"',
            "triggers": "Identity + Emotion",
        },
        "conversion": {
            "template": '"How I went from [start] to [result]. Exact playbook:"',
            "triggers": "Transformation + Authority",
        },
        "shares": {
            "template": '"The truth about [common aspiration] nobody shares"',
            "triggers": "Curiosity + Vulnerability",
        },
        "saves": {
            "template": '"My complete [journey/process] breakdown"',
            "triggers": "Comprehensiveness",
        },
    },
    ("personal_brand", "youtube", "shorts"): {
        "engagement": {
            "template": '"The hardest part of [aspiration] no one talks about"',
            "triggers": "Vulnerability + Curiosity",
        },
        "conversion": {
            "template": '"[Result] in [timeframe]. Here\'s the truth:"',
            "triggers": "Transformation + Authenticity",
        },
        "shares": {
            "template": '"Things only [identity group] will understand"',
            "triggers": "Identity + Belonging",
        },
        "saves": {
            "template": '"Save this if you\'re on the [specific journey]"',
            "triggers": "Identity + Command",
        },
    },
    ("personal_brand", "instagram", "reels"): {
        "engagement": {
            "template": '"POV: You finally [aspiration]" + emotional delivery',
            "triggers": "Identity + Aspiration",
        },
        "conversion": {
            "template": '[Show transformation result] → "This changed everything:"',
            "triggers": "Visual proof + Open loop",
        },
        "shares": {
            "template": '"Things only [identity group] understand"',
            "triggers": "Identity + Belonging",
        },
        "saves": {
            "template": '"My [timeframe] transformation — the real story"',
            "triggers": "Authenticity",
        },
    },
    ("personal_brand", "instagram", "carousel"): {
        "engagement": {
            "template": 'Slide 1: "What I wish I knew before [life event]"',
            "triggers": "Regret + Curiosity",
        },
        "conversion": {
            "template": 'Slide 1: "From [bad state] to [good state] — my exact steps"',
            "triggers": "Transformation + Specificity",
        },
        "shares": {
            "template": 'Slide 1: "Honest lessons from [failure]"',
            "triggers": "Vulnerability + Emotion",
        },
        "saves": {
            "template": 'Slide 1: "[Number] mindset shifts that changed everything"',
            "triggers": "Identity + Framework",
        },
    },
    ("business", "linkedin", "text"): {
        "engagement": {
            "template": '"Unpopular opinion: [industry sacred cow] is dead."',
            "triggers": "Contrarian + Controversy",
        },
        "conversion": {
            "template": '"[Specific metric] improvement in [timeframe]. The system:"',
            "triggers": "Data + Specificity",
        },
        "shares": {
            "template": '"[Surprising stat]% of [audience] are doing [mistake]."',
            "triggers": "Data + Negativity",
        },
        "saves": {
            "template": '"The framework behind [company]\'s [result]:"',
            "triggers": "Social proof + Framework",
        },
    },
    ("business", "linkedin", "carousel"): {
        "engagement": {
            "template": 'Slide 1: "Hot take: [industry belief] is wrong"',
            "triggers": "Contrarian",
        },
        "conversion": {
            "template": 'Slide 1: "How [company] achieved [metric]"',
            "triggers": "Social proof + Specificity",
        },
        "shares": {
            "template": 'Slide 1: "[Year] [industry] predictions that matter"',
            "triggers": "FOMO + Timeliness",
        },
        "saves": {
            "template": 'Slide 1: "[Topic] strategy template — steal this"',
            "triggers": "Value + Generosity",
        },
    },
    ("business", "youtube", "long_form"): {
        "engagement": {
            "template": '"Why [common B2B practice] is costing you [specific loss]"',
            "triggers": "Negativity + Specificity",
        },
        "conversion": {
            "template": '"[Client] went from [A] to [B]. Here\'s the strategy:"',
            "triggers": "Case study + Promise",
        },
        "shares": {
            "template": '"The [industry] trend that will change everything in [year]"',
            "triggers": "FOMO + Prediction",
        },
        "saves": {
            "template": '"[Number]-step system for [specific B2B outcome]"',
            "triggers": "Structure + Value",
        },
    },
    ("business", "youtube", "shorts"): {
        "engagement": {
            "template": '"[Industry myth] is costing you [specific amount]"',
            "triggers": "Negativity + Specificity",
        },
        "conversion": {
            "template": '"[Metric] increase in [time]. Do this:"',
            "triggers": "Data + Urgency",
        },
        "shares": {
            "template": '"The [tool/strategy] your competitors don\'t want you to know"',
            "triggers": "FOMO + Curiosity",
        },
        "saves": {
            "template": '"[Number]-second tip that saves [time/money]:"',
            "triggers": "Specificity + Command",
        },
    },
    ("business", "instagram", "reels"): {
        "engagement": {
            "template": 'Text overlay: "[Industry hot take]" + confident delivery',
            "triggers": "Contrarian + Pattern interrupt",
        },
        "conversion": {
            "template": '[Show dashboard/result] → "Here\'s the exact setup:"',
            "triggers": "Visual proof + Open loop",
        },
        "shares": {
            "template": '"Things every [role] needs to hear right now"',
            "triggers": "Identity + Timeliness",
        },
        "saves": {
            "template": '"Quick framework for [business outcome]"',
            "triggers": "Value + Specificity",
        },
    },
    ("business", "instagram", "carousel"): {
        "engagement": {
            "template": 'Slide 1: "Hot take: [industry belief] is wrong"',
            "triggers": "Contrarian",
        },
        "conversion": {
            "template": 'Slide 1: "How [company] achieved [metric]"',
            "triggers": "Social proof + Specificity",
        },
        "shares": {
            "template": 'Slide 1: "[Year] [industry] predictions that matter"',
            "triggers": "FOMO + Timeliness",
        },
        "saves": {
            "template": 'Slide 1: "[Topic] strategy template — steal this"',
            "triggers": "Value + Generosity",
        },
    },
    ("entertainment", "youtube", "long_form"): {
        "engagement": {
            "template": '"[Outrageous setup] and I have [time constraint] to do it."',
            "triggers": "Curiosity + Stakes",
        },
        "conversion": {
            "template": '"Watch what happens when I [unexpected action]"',
            "triggers": "Curiosity + Open loop",
        },
        "shares": {
            "template": '"You won\'t believe what happened when [setup]"',
            "triggers": "Curiosity + Emotional resonance",
        },
        "saves": {
            "template": '"The ultimate guide to [fun/niche topic]"',
            "triggers": "Comprehensiveness",
        },
    },
    ("entertainment", "youtube", "shorts"): {
        "engagement": {
            "template": "[Unexpected visual/action in first frame]",
            "triggers": "Pattern interrupt + Curiosity",
        },
        "conversion": {
            "template": '"Wait for it..." + [visual buildup]',
            "triggers": "Open loop + Anticipation",
        },
        "shares": {
            "template": '"Tell me you [X] without telling me you [X]"',
            "triggers": "Identity + Humor",
        },
        "saves": {
            "template": '"Best [niche thing] compilation — part [N]"',
            "triggers": "Value + Series hook",
        },
    },
    ("entertainment", "instagram", "reels"): {
        "engagement": {
            "template": "[Dramatic visual/sound] + trend audio",
            "triggers": "Sensory + Pattern interrupt",
        },
        "conversion": {
            "template": '"POV: [relatable scenario]" + trending audio',
            "triggers": "Identity + Trend-jacking",
        },
        "shares": {
            "template": '"Things that just make sense in [niche]"',
            "triggers": "Identity + Belonging",
        },
        "saves": {
            "template": '"[Satisfying process] from start to finish"',
            "triggers": "Sensory + Completion",
        },
    },
    ("entertainment", "instagram", "carousel"): {
        "engagement": {
            "template": 'Slide 1: "[Provocative opinion] — agree or disagree?"',
            "triggers": "Controversy + Engagement prompt",
        },
        "conversion": {
            "template": 'Slide 1: "Ranking every [niche thing] from worst to best"',
            "triggers": "Curiosity + Opinion",
        },
        "shares": {
            "template": 'Slide 1: "[Niche] starter pack"',
            "triggers": "Identity + Humor",
        },
        "saves": {
            "template": 'Slide 1: "Ultimate [niche] mood board / inspo"',
            "triggers": "Aspiration + Value",
        },
    },
    ("entertainment", "linkedin", "text"): {
        "engagement": {
            "template": '"I did something ridiculous at work today. Let me explain."',
            "triggers": "Curiosity + Vulnerability",
        },
        "conversion": {
            "template": '"The weirdest career advice I ever followed (and why it worked):"',
            "triggers": "Curiosity + Contrarian",
        },
        "shares": {
            "template": '"Things you\'ll only understand if you\'ve worked in [industry]"',
            "triggers": "Identity + Humor",
        },
        "saves": {
            "template": '"The funniest [industry] stories I\'ve collected:"',
            "triggers": "Entertainment + Social currency",
        },
    },
    ("entertainment", "linkedin", "carousel"): {
        "engagement": {
            "template": 'Slide 1: "[Industry] memes that are painfully accurate"',
            "triggers": "Identity + Humor",
        },
        "conversion": {
            "template": 'Slide 1: "Ranking [industry things] — hot takes inside"',
            "triggers": "Curiosity + Controversy",
        },
        "shares": {
            "template": 'Slide 1: "Tag a colleague who does #3"',
            "triggers": "Identity + Social",
        },
        "saves": {
            "template": 'Slide 1: "The [industry] bingo card you didn\'t know you needed"',
            "triggers": "Humor + Identity",
        },
    },
}

# ---------------------------------------------------------------------------
# Data: Authority-level adjustments
# ---------------------------------------------------------------------------

AUTHORITY_ADVICE = {
    "beginner": {
        "label": "Beginner / Growing",
        "do": [
            'Use the Experimenter archetype: "I tested X so you don\'t have to"',
            'Borrow authority: "A veteran [expert] says..."',
            "Let data/stats provide credibility without personal credentials",
            "Vulnerability hooks work BETTER for you — lead with failure to build trust",
            "Document your journey — audiences root for underdogs",
        ],
        "dont": [
            "Don't open with authority hooks you can't back up",
            "Don't fake credentials or inflate experience",
            "Don't use social proof numbers you don't have",
        ],
    },
    "established": {
        "label": "Established / Authority",
        "do": [
            'Open with direct authority: "After [X years/credential]..."',
            "Reference past results and client transformations",
            "Use audience social proof (subscriber/client counts)",
            "Take stronger contrarian positions — your reputation supports it",
            "Name-drop specific frameworks or methods you've created",
        ],
        "dont": [
            "Don't rely solely on credentials — still lead with value",
            "Don't be so authoritative you lose relatability",
            "Avoid humble-bragging disguised as teaching",
        ],
    },
}

# ---------------------------------------------------------------------------
# Data: Audience temperature adjustments
# ---------------------------------------------------------------------------

AUDIENCE_ADVICE = {
    "cold": {
        "label": "Cold (Discovery / New viewers)",
        "approach": [
            "Lead with educational, problem-solving hooks — zero promotional language",
            "Best triggers: curiosity gaps, surprising facts, relatable problems",
            "Give free value upfront — prove your worth before asking anything",
            "Platform mapping: YouTube search, TikTok FYP, Instagram Reels explore",
        ],
    },
    "warm": {
        "label": "Warm (Followers / Subscribers)",
        "approach": [
            "More direct hooks allowed — they already trust you somewhat",
            "Behind-the-scenes content and shared references work well",
            "Community-building language strengthens connection",
            "Platform mapping: LinkedIn feed, Instagram feed, YouTube home",
        ],
    },
    "hot": {
        "label": "Hot (Customers / Superfans)",
        "approach": [
            "Direct promotional hooks are appropriate",
            "Social proof of others' results converts best",
            "Urgency and specific offers drive action",
            "Platform mapping: email lists, private communities, retargeting",
        ],
    },
}

# ---------------------------------------------------------------------------
# Data: Creator Frameworks
# ---------------------------------------------------------------------------

FRAMEWORKS = [
    {
        "name": "Justin Welsh's VFA Formula",
        "steps": "Visceral opener → Fresh perspective → Anaphora (repeated structure)",
        "variant": "PAIPS: Problem → Agitate → Intrigue → Positive Future → Solution",
        "result": "276K impressions from a single LinkedIn post",
    },
    {
        "name": "George Blackman's Target-Transformation-Stakes (YouTube)",
        "steps": "Make it clear this is for THEM (3 sentences) → Transformation they'll experience (1 sentence) → What they risk by not watching (1 bold statement)",
        "variant": "PVSS: Proof → Value → Structure → Stakes",
        "result": "86% retention after 30 seconds",
    },
    {
        "name": "Alex Hormozi's Hook-Retain-Reward",
        "steps": "Hook (redirect attention) → Retain (open loops + value) → Reward (satisfaction)",
        "variant": "6 angles x 5 hooks = 30 variations testing matrix",
        "result": "Systematic hook testing at scale",
    },
    {
        "name": "PAS (Problem-Agitate-Solution)",
        "steps": "State the problem → Agitate the pain → Present the solution",
        "variant": "Most versatile framework across all platforms",
        "result": "Classic copywriting adapted for social media",
    },
    {
        "name": "Dickie Bush & Nicolas Cole's 1 Chip Rule",
        "steps": "Hook so easy to consume it's impossible not to want more",
        "variant": "Rate of Revelation — every sentence pushes the story forward",
        "result": "Optimized for reading speed and scroll-stopping",
    },
]

# ---------------------------------------------------------------------------
# Composable formula builder
# ---------------------------------------------------------------------------

TRIGGER_FORMULAS = {
    "curiosity_gap": [
        "[Surprising incomplete fact]... here's what actually happened.",
        "Nobody is talking about [hidden insight]. Let me explain.",
        "There's a reason [common thing] doesn't work. And it's not what you think.",
    ],
    "fomo": [
        "[Number]% of [group] are already doing this. Are you?",
        "This [strategy] won't work forever. Here's why you need to act now.",
        "Everyone in [industry] knows this except you.",
    ],
    "social_proof": [
        "[Number]+ [people] have used this to [result].",
        "[Known figure] swears by this [method]. Here's why.",
        "The [method] behind [impressive result].",
    ],
    "specificity": [
        "[Precise number] [result] in [exact timeframe]. Here's step 1.",
        "I tested [exact number] [things] — only [small number] actually worked.",
        "[Specific metric] increase using [specific method].",
    ],
    "contrarian": [
        "Everything you've been told about [topic] is wrong.",
        "Unpopular opinion: [sacred cow] is dead.",
        "[Common advice] is actually hurting your [outcome]. Here's proof.",
    ],
    "identity": [
        "This is for every [specific person] who's tired of [pain].",
        "If you're a [identity], you need to hear this.",
        "POV: You're a [identity] who finally [aspiration].",
    ],
    "pattern_interrupt": [
        "[Unexpected visual/statement that breaks the scroll]",
        "[Start mid-action with zero context — then explain]",
        "[Contradictory pairing: serious topic + unexpected delivery]",
    ],
    "emotional_resonance": [
        "I almost [gave up / quit / failed]. Then [turning point].",
        "The hardest part of [journey] that nobody warns you about.",
        "I wasn't supposed to share this, but [vulnerable truth].",
    ],
    "negativity_bias": [
        "The #1 mistake [group] makes with [topic] — and the fix.",
        "Stop doing [common action]. It's ruining your [outcome].",
        "[Number] [topic] myths that are costing you [loss].",
    ],
}


# ---------------------------------------------------------------------------
# UI Helpers
# ---------------------------------------------------------------------------

def clear_line():
    print()


def header(text):
    width = min(len(text) + 4, 70)
    print("\n" + "=" * width)
    print(f"  {text}")
    print("=" * width)


def sub_header(text):
    print(f"\n--- {text} ---")


def bullet(text, indent=2):
    prefix = " " * indent + "• "
    wrapped = textwrap.fill(text, width=76, initial_indent=prefix,
                            subsequent_indent=" " * (indent + 2))
    print(wrapped)


def numbered(items, indent=2):
    for i, item in enumerate(items, 1):
        prefix = " " * indent + f"{i}. "
        wrapped = textwrap.fill(item, width=76, initial_indent=prefix,
                                subsequent_indent=" " * (indent + 4))
        print(wrapped)


def ask_choice(prompt, options, allow_multiple=False):
    """Interactive menu. Returns key(s) from options dict."""
    print(f"\n{prompt}")
    keys = list(options.keys())
    for i, key in enumerate(keys, 1):
        print(f"  [{i}] {options[key]}")

    while True:
        try:
            if allow_multiple:
                raw = input("\nChoose (comma-separated, e.g. 1,3): ").strip()
                indices = [int(x.strip()) for x in raw.split(",")]
                if all(1 <= idx <= len(keys) for idx in indices):
                    return [keys[idx - 1] for idx in indices]
            else:
                raw = input("\nChoose: ").strip()
                idx = int(raw)
                if 1 <= idx <= len(keys):
                    return keys[idx - 1]
        except (ValueError, IndexError):
            pass
        print("  Invalid choice, try again.")


# ---------------------------------------------------------------------------
# Output Sections
# ---------------------------------------------------------------------------

def show_platform_context(platform_key):
    p = PLATFORMS[platform_key]
    sub_header(f"Platform: {p['name']}")
    print(f"  Hook window:    {p['hook_window']}")
    print(f"  Primary metric: {p['primary_metric']}")
    print(f"  Audience state: {p['audience_state']}")
    print(f"  Sound:          {p['sound_dependency']}")
    print(f"  Algo signal:    {p['algo_signal']}")
    print("\n  Key stats:")
    for stat in p["key_stats"]:
        bullet(stat, indent=4)


def show_format_rules(format_key):
    f = FORMAT_INFO[format_key]
    sub_header(f"Format: {f['name']}")
    print("  Rules for this format:")
    for rule in f["rules"]:
        bullet(rule, indent=4)


def show_niche_context(niche_key):
    n = NICHES[niche_key]
    sub_header(f"Niche: {n['name']}")
    print(f"  Dominant triggers: {', '.join(n['dominant_triggers'])}")
    print(f"  Structure: {n['structure']}")
    print("\n  Top hook styles for this niche:")
    for style in n["hook_styles"]:
        bullet(style, indent=4)


def show_hook_recommendation(niche_key, platform_key, format_key, goal_key):
    header("RECOMMENDED HOOK")
    lookup = (niche_key, platform_key, format_key)
    if lookup in HOOK_MAP and goal_key in HOOK_MAP[lookup]:
        rec = HOOK_MAP[lookup][goal_key]
        print(f"\n  Template:  {rec['template']}")
        print(f"  Triggers:  {rec['triggers']}")
    else:
        print("\n  No exact match in the mapping. Building from components...")
        # Fallback: compose from niche triggers + format rules
        n = NICHES[niche_key]
        print(f"\n  Use these triggers: {', '.join(n['dominant_triggers'])}")
        print(f"  With this structure: {n['structure']}")
        print(f"  Adapted to: {FORMAT_INFO[format_key]['name']} on {PLATFORMS[platform_key]['name']}")


def show_anti_patterns(platform_key):
    sub_header(f"Anti-patterns to AVOID on {PLATFORMS[platform_key]['name']}")
    for ap in ANTI_PATTERNS[platform_key]:
        bullet(ap, indent=4)


def show_authority_advice(level_key):
    a = AUTHORITY_ADVICE[level_key]
    sub_header(f"Authority Level: {a['label']}")
    print("  Do:")
    for item in a["do"]:
        bullet(item, indent=4)
    print("  Don't:")
    for item in a["dont"]:
        bullet(item, indent=4)


def show_audience_advice(temp_key):
    a = AUDIENCE_ADVICE[temp_key]
    sub_header(f"Audience: {a['label']}")
    for item in a["approach"]:
        bullet(item, indent=4)


def show_trigger_formulas(niche_key, goal_key):
    sub_header("Composable Hook Formulas")
    n = NICHES[niche_key]
    # Map niche triggers to formula keys
    trigger_map = {
        "Curiosity gap": "curiosity_gap",
        "Specificity": "specificity",
        "Negativity bias": "negativity_bias",
        "Emotional resonance": "emotional_resonance",
        "Identity": "identity",
        "Vulnerability": "emotional_resonance",
        "Contrarian/Controversy": "contrarian",
        "Social proof": "social_proof",
        "Pattern interrupt": "pattern_interrupt",
    }
    shown = set()
    for trigger_name in n["dominant_triggers"]:
        key = trigger_map.get(trigger_name)
        if key and key in TRIGGER_FORMULAS and key not in shown:
            shown.add(key)
            t = TRIGGERS.get(key, {})
            print(f"\n  {t.get('name', key)} ({t.get('boost', '')}):")
            for formula in TRIGGER_FORMULAS[key]:
                bullet(formula, indent=4)


def show_frameworks():
    sub_header("Proven Creator Frameworks to Apply")
    for fw in FRAMEWORKS:
        print(f"\n  {fw['name']}")
        print(f"    Steps:   {fw['steps']}")
        print(f"    Variant: {fw['variant']}")
        print(f"    Result:  {fw['result']}")


def show_structural_patterns():
    sub_header("5 Core Structural Patterns")
    for p in PATTERNS:
        print(f"\n  {p['name']}")
        print(f"    Template: {p['template']}")
        print(f"    Example:  {p['example']}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    quick = "--quick" in sys.argv

    header("HOOK SELECTOR FRAMEWORK")
    print("Answer 6 questions to get a tailored hook recommendation.\n")

    # 1. Platform
    platform = ask_choice(
        "1. Which platform are you creating for?",
        {
            "linkedin": "LinkedIn",
            "youtube": "YouTube",
            "instagram": "Instagram",
        },
    )

    # 2. Format (filtered by platform)
    available_formats = PLATFORMS[platform]["formats"]
    format_options = {k: FORMAT_INFO[k]["name"] for k in available_formats}
    fmt = ask_choice(
        "2. What content format?",
        format_options,
    )

    # 3. Niche
    niche = ask_choice(
        "3. What's your content niche?",
        {
            "education": "Education / How-to",
            "personal_brand": "Personal Brand / Storytelling",
            "business": "Business / B2B",
            "entertainment": "Entertainment / Lifestyle",
        },
    )

    # 4. Goal
    goal = ask_choice(
        "4. What's the primary goal of this content?",
        {
            "engagement": "Engagement (comments, likes, debate)",
            "conversion": "Conversion (sales, sign-ups, leads)",
            "shares": "Shares / Virality (DMs, reposts)",
            "saves": "Saves / Bookmarks (reference value)",
        },
    )

    # 5. Authority
    authority = ask_choice(
        "5. Your authority level in this topic?",
        {
            "beginner": "Beginner / Growing (< 2 years, small audience)",
            "established": "Established / Authority (known in your space)",
        },
    )

    # 6. Audience temperature
    audience = ask_choice(
        "6. Who will see this content?",
        {
            "cold": "Cold — Discovery / New viewers who don't know me",
            "warm": "Warm — My followers / subscribers",
            "hot": "Hot — Existing customers / superfans",
        },
    )

    # === OUTPUT ===
    header("YOUR HOOK BLUEPRINT")
    print(f"\n  Platform:  {PLATFORMS[platform]['name']}")
    print(f"  Format:    {FORMAT_INFO[fmt]['name']}")
    print(f"  Niche:     {NICHES[niche]['name']}")
    print(f"  Goal:      {goal.capitalize()}")
    print(f"  Authority: {AUTHORITY_ADVICE[authority]['label']}")
    print(f"  Audience:  {AUDIENCE_ADVICE[audience]['label']}")

    # Primary recommendation
    show_hook_recommendation(niche, platform, fmt, goal)

    # Platform context
    show_platform_context(platform)

    # Format rules
    show_format_rules(fmt)

    # Niche context
    show_niche_context(niche)

    # Anti-patterns
    show_anti_patterns(platform)

    # Authority advice
    show_authority_advice(authority)

    # Audience advice
    show_audience_advice(audience)

    if not quick:
        # Composable formulas
        show_trigger_formulas(niche, goal)

        # Structural patterns
        show_structural_patterns()

        # Creator frameworks
        show_frameworks()

    header("NEXT STEPS")
    numbered([
        "Pick the recommended template above and fill in your specifics",
        "Write 3-5 variations using different triggers from the formulas",
        "Test variations — use Hormozi's 6x5 matrix to systematize testing",
        "Check your hook against the anti-patterns list before posting",
        f"Remember: you have {PLATFORMS[platform]['hook_window']} to land it",
    ])
    print()


if __name__ == "__main__":
    main()
