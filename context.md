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


Addityional Requiremtns

📘 Inner Compass — Product Requirements Document (PRD)
1. Purpose
Inner Compass is a Progressive Web App (PWA) designed to help the user:

Act with clarity, presence, and accountability in real-time
Reduce overthinking, delay, and emotional withdrawal
Improve consistent, observable behavior in relationships
2. Core Principle
This app is not for thinking more.
This app is for behaving better in real-time.

3. Target Problems
Delayed acknowledgment
Silence / withdrawal during discomfort
Over-explaining instead of acting
Forcing conversations
Lack of consistency in small commitments
Emotional over-engagement followed by exhaustion
4. Design Philosophy
MUST:
Fast (<10s interactions)
Action-oriented
Minimal UI
Real-time usable
MUST NOT:
Enable over-analysis
Track other people’s behavior
Allow long journaling
Reinforce rumination
5. Core Features (MVP)
5.1 Daily Grounding
Goal: Start the day with behavioral clarity

UI:

3–5 principles
1 optional intention (max 100 chars)
Example Principles:

Don’t delay acknowledgment
Don’t force engagement
Stay steady, not impressive
No silence > 1 min
Follow through on what you say
5.2 Real-Time Interaction Coach ⭐ (Core Feature)
Goal: Guide behavior during live interactions

Input Options:

She is closed
She is upset
I feel like withdrawing
I feel like pushing
Conversation is escalating
Output (example):

If: She is closed

• Do not push topic
• Say: "I won’t push this right now"
• Return to normal activity
If: I feel like withdrawing

• Say one line before pausing
• Do not disappear silently
5.3 Micro-Repair Tool
Goal: Immediate correction after mistakes

Input:

Missed plan
Delayed response
Silence
Defensiveness
Output:
Short repair script (max 1–2 lines)

Example:

"I missed sharing the plan. That’s on me."
Rules:

No explanation allowed
No emotional justification
5.4 Behavior Tracker (Daily Checklist)
Goal: Track consistency (not feelings)

Checklist:

Shared plan by 9pm
No delayed acknowledgment
No silence > 1 min
No forced conversations
Followed through on commitments
Important:

Binary only (no scoring)
No streak pressure
5.5 Evening Reflection (Strictly Limited)
Max 3 Inputs:

One thing done well
One miss (fact only)
One correction for tomorrow
Constraints:

Max 200 chars per field
No long journaling
5.6 “I’m Spiraling” Button
Goal: Interrupt escalation

Output:

Pause.
Don’t fix.
Don’t withdraw.
Stay simple.
Optional:

30-second breathing timer
6. User Flow
Morning:
Open app → Daily Grounding
During Day:
Use Real-Time Coach as needed
Use Micro-Repair immediately after mistakes
Evening:
Complete checklist
Fill 3 reflection fields
7. UX Requirements
One-tap actions
No deep navigation
Dark + light mode
Offline-first
Mobile-first design
8. Technical Architecture (PWA)
Frontend:
React (Next.js recommended)
TailwindCSS
PWA:
Service Worker (offline support)
Installable on mobile
Storage:
LocalStorage (MVP)
Optional: Firebase/Supabase later
9. Data Model (MVP)
{
  "dailyLog": {
    "date": "YYYY-MM-DD",
    "principles": [],
    "checklist": {
      "planShared": true,
      "noDelay": false,
      "noSilence": true,
      "noForce": false,
      "followThrough": true
    },
    "reflection": {
      "good": "",
      "miss": "",
      "fix": ""
    }
  }
}
10. Key Screens
1. Home Dashboard
Today’s principles
Checklist
“I need help now” button
2. Real-Time Coach
Input buttons
Instant output guidance
3. Repair Screen
Select mistake
Show script
4. Reflection Screen
3 fields only
11. Guardrails (Critical)
The app must NOT allow:
Logging wife’s behavior
Writing long emotional entries
Tracking “who is right”
Replaying arguments
12. Success Metrics
Success = Reduction in:

delayed responses
silence during conflict
repeated mistakes
NOT:

number of entries
amount of writing
13. Future Enhancements
Voice-based quick input
Smart reminders (e.g., 9pm planning)
Pattern detection (local only)
Habit trends (non-gamified)
14. Core Philosophy (Display in App)
Don’t fix. Don’t withdraw. Stay steady.
Consistency builds trust, not intensity.

15. Final Constraint (Very Important)
If you are using this app instead of speaking when needed — close the app and go speak.