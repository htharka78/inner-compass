I want to create a PWA for improving myself, learn self-reflection as a skill, become more empathetic, be a good human being and a good, caring, responsible husband.

Include daily (within the day nudges) for self-reflection, self-discpline activities - exercise,  walking, maintaining core boundaries, journal (short and to the point instead of meandering). I want to use this PWA on my phone and my macbook. I want daily exercises (new ones everyday) as well.

weekly and quarterly summary ✓ (built into Journal tab)

Starter:

Inner Compass — a PWA designed around the kind of person you want to become. Here's what's inside:
Today — A daily mood check-in, habit tracker (with a 7-day dot grid), and a gratitude prompt. Small, grounding rituals for starting the day with intention.
Reflect — Rotating prompts drawn from self-awareness, empathy, relationships, and integrity. Write freely, save reflections, and capture what each day taught you.
Empathy — Four scenario-based exercises (colleagues, your partner, strangers, loved ones making mistakes) that ask you to genuinely inhabit another person's perspective. This is the muscle that makes you kinder.
Partner — A dedicated space for relationship care: micro-habit tracking (undivided attention, asking how they really are, expressing appreciation), plus prompts for appreciation, honest self-assessment, and a loving intention for tomorrow.
Journal — A growing archive of your reflections with a streak counter to celebrate consistency.

---
## Built — Inner Compass PWA

**Location:** `/Users/htharka/dev/sandbox/self_dev/`
**Run locally:** `python3 -m http.server 8765` → `http://localhost:8765`
**Mobile (same WiFi):** `http://192.168.1.66:8765`
**Install on iPhone:** Safari → Share → Add to Home Screen

### Tabs
1. **Today** — Nudge card (time-based), mood check-in (😔–🌟), 7-day dot grid, Today's Practice (48 rotating daily exercises: physical/mindfulness/empathy/discipline), gratitude prompt (120 chars), habit checklist (walk · exercise · reflected · partner moment)
2. **Reflect** — 48 rotating prompts across 4 categories (self-awareness, empathy, relationships, integrity). 280-char limit. Save marks "reflected" habit.
3. **Empathy** — 8 rotating scenarios (colleague ×2, partner ×2, stranger ×2, loved one ×2). Two writes each: inhabit their perspective + what shifted.
4. **Partner** — 4 micro-habit checkboxes + appreciation (150 chars) + 5-emoji self-assessment + tomorrow's intention (120 chars). Auto-checks partner habit when ≥2 micro-habits done.
5. **Journal** — Streak/stats pills, **Weekly Summary** (Mon–Sun grid + habit %, avg mood, reflect count), **Quarterly Summary** (last 90 days: completion, longest streak, avg mood, partner %), **Reflection Archive** (last 30 entries, expandable).

### Stack
Pure HTML/CSS/JS · no build step · no backend · localStorage (`innercompass_v2`) · offline via service worker · dark mode · notifications opt-in (8am/1pm/8pm)